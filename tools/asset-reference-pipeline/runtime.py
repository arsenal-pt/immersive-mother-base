"""Private, local state and owned subprocess execution. No network or agent APIs."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import time


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(path)


class ManualReview(Exception):
    """Unsupported/ambiguous input; never guess success."""


class Cancelled(Exception):
    pass


def inside(path, parent):
    return Path(path).resolve().is_relative_to(Path(parent).resolve())


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root / 'jobs.sqlite', timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS jobs (
          id TEXT PRIMARY KEY, recipe TEXT NOT NULL, lod INTEGER NOT NULL,
          status TEXT NOT NULL, cancel INTEGER NOT NULL DEFAULT 0,
          error TEXT, result TEXT, updated REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS stages (
          job_id TEXT, name TEXT, fingerprint TEXT, status TEXT,
          receipt TEXT, updated REAL, PRIMARY KEY(job_id,name));
        CREATE TABLE IF NOT EXISTS events (
          sequence INTEGER PRIMARY KEY, job_id TEXT, stage TEXT,
          kind TEXT, detail TEXT, time REAL);
        CREATE TABLE IF NOT EXISTS assets (
          job_id TEXT PRIMARY KEY, record TEXT NOT NULL);
        ''')

    def enqueue(self, recipe, lod):
        # Friendly metadata changes never invalidate expensive content stages.
        identity = {k: v for k, v in recipe.items() if k not in ('title', 'description', 'tags', 'category')}
        key = digest({'recipe': identity, 'lod': lod})[:24]
        current = self.db.execute('SELECT status FROM jobs WHERE id=?', (key,)).fetchone()
        if current is not None and current['status'] == 'running':
            raise ManualReview('Job is running; wait or cancel before changing its selected recipe')
        self.db.execute('''INSERT INTO jobs(id,recipe,lod,status,updated) VALUES(?,?,?,'queued',?)
          ON CONFLICT(id) DO UPDATE SET recipe=excluded.recipe, status='queued', cancel=0, updated=excluded.updated''',
                        (key, canonical(recipe), lod, time.time()))
        self.db.commit()
        return key

    def event(self, job, stage, kind, detail=''):
        self.db.execute('INSERT INTO events(job_id,stage,kind,detail,time) VALUES(?,?,?,?,?)',
                        (job, stage, kind, canonical(detail), time.time()))
        self.db.commit()
        print(f'{job} {stage}: {kind}', flush=True)

    def job(self, key):
        row = self.db.execute('SELECT * FROM jobs WHERE id=?', (key,)).fetchone()
        if row is None:
            raise ValueError('Unknown job: ' + key)
        return row

    def status(self, job, status, error=None, result=None):
        self.db.execute('UPDATE jobs SET status=?,error=?,result=COALESCE(?,result),updated=? WHERE id=?',
                        (status, error, canonical(result) if result else None, time.time(), job))
        self.db.commit()

    def check_cancel(self, job):
        if self.job(job)['cancel']:
            raise Cancelled('Cancellation requested')

    def stage(self, job, name, fingerprint, callback):
        self.check_cancel(job)
        folder = self.root / 'cache' / name / fingerprint[:16]
        if folder.exists() and (folder/'fingerprint.json').exists():
            if load(folder/'fingerprint.json').get('fingerprint') != fingerprint:
                raise ManualReview('Short cache-key collision; full fingerprint differs')
        receipt_path = folder / 'stage.json'
        valid = False
        if receipt_path.exists():
            try:
                receipt = load(receipt_path)
                valid = receipt.get('fingerprint') == fingerprint and 'result' in receipt and bool(receipt['files']) and all(
                    inside(folder / item['path'], folder) and (folder / item['path']).is_file()
                    and sha(folder / item['path']) == item['sha256'] for item in receipt['files'])
            except (OSError, ValueError, KeyError, TypeError, AttributeError):
                valid = False
        self.db.execute('INSERT OR REPLACE INTO stages VALUES(?,?,?,?,?,?)',
                        (job, name, fingerprint, 'cached' if valid else 'running', str(receipt_path), time.time()))
        self.db.commit()
        if valid:
            self.event(job, name, 'cache_hit')
            return folder, receipt['result']
        if folder.exists():
            # Retain partial output as private failure evidence, never reuse incomplete frames.
            folder.rename(folder.with_name(fingerprint[:16] + '-incomplete-' + str(time.time_ns())))
        folder.mkdir(parents=True)
        save(folder/'fingerprint.json', {'fingerprint':fingerprint})
        self.event(job, name, 'started')
        try:
            result = callback(folder)
            self.check_cancel(job)
            files = [{'path': p.relative_to(folder).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
                     for p in sorted(folder.rglob('*')) if p.is_file()]
            save(receipt_path, {'fingerprint': fingerprint, 'result': result, 'files': files})
        except (Exception, KeyboardInterrupt) as ex:
            state = 'cancelled' if isinstance(ex, (Cancelled, KeyboardInterrupt)) else ('manual_review' if isinstance(ex, ManualReview) else 'failed')
            self.db.execute('UPDATE stages SET status=?,updated=? WHERE job_id=? AND name=?',
                            (state, time.time(), job, name))
            self.db.commit()
            self.event(job, name, state, str(ex))
            raise
        self.db.execute('UPDATE stages SET status=?,updated=? WHERE job_id=? AND name=?',
                        ('complete', time.time(), job, name))
        self.db.commit()
        self.event(job, name, 'complete')
        return folder, result

    def process(self, job, stage, argv, cwd, timeout=600):
        """Terminate only our Popen child, never shared tool processes."""
        cwd = Path(cwd)
        log = cwd / (stage + '-process.log')
        self.event(job, stage, 'process_launch', {'argv': list(map(str, argv)), 'cwd': str(cwd)})
        flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        started = time.monotonic()
        with log.open('wb') as output:
            child = subprocess.Popen(list(map(str, argv)), cwd=cwd, stdin=subprocess.PIPE,
                                     stdout=output, stderr=subprocess.STDOUT, creationflags=flags)
            self.event(job, stage, 'process_started', {'pid': child.pid})
            try:
                child.stdin.write(b'\n')
                child.stdin.close()
            except BrokenPipeError:
                pass
            try:
                while child.poll() is None:
                    self.check_cancel(job)
                    if time.monotonic() - started > timeout:
                        raise TimeoutError(stage + ' exceeded timeout')
                    time.sleep(.2)
                self.check_cancel(job)
                if child.returncode:
                    raise RuntimeError(f'{stage} exited {child.returncode}; see {log}')
            finally:
                if child.poll() is None:
                    child.terminate()
                    try:
                        child.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait(timeout=5)
        return log


class WorkerLock:
    """One worker per runtime. A crash lock needs explicit owned-process inspection."""
    def __init__(self, root):
        self.path = Path(root) / 'worker.lock'

    def __enter__(self):
        try:
            self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise ManualReview('worker.lock exists. Check its PID/owned child before removing a stale crash lock.')
        os.write(self.fd, str(os.getpid()).encode())
        return self

    def __exit__(self, *unused):
        os.close(self.fd)
        self.path.unlink()


def tool_info(path):
    path = Path(path).resolve()
    if not path.is_file():
        raise ManualReview('Configured tool is missing: ' + str(path))
    version = None
    if os.name == 'nt' and path.suffix.lower() == '.exe':
        size = ctypes.windll.version.GetFileVersionInfoSizeW(str(path), None)
        if size:
            data = ctypes.create_string_buffer(size)
            pointer, length = ctypes.c_void_p(), ctypes.c_uint()
            if ctypes.windll.version.GetFileVersionInfoW(str(path), 0, size, data):
                if ctypes.windll.version.VerQueryValueW(data, '\\', ctypes.byref(pointer), ctypes.byref(length)):
                    words = ctypes.cast(pointer, ctypes.POINTER(ctypes.c_uint32))
                    version = '.'.join(map(str, (words[2] >> 16, words[2] & 65535, words[3] >> 16, words[3] & 65535)))
    return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size, 'fileVersion': version}
