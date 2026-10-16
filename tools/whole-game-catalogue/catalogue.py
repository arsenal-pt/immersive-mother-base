"""Deterministic as-installed catalogue using installed GzsTool.Core; no network."""
from __future__ import annotations
import argparse
import contextlib
import csv
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import struct
import subprocess
import sys
import time
import uuid

HERE = Path(__file__).resolve().parent
MIB = 1024 * 1024
KINDS = {"fpk": "fpk", "fpkd": "fpkd", "pftxs": "pftxs", "sbp": "sbp", "dat": "qar", "qar": "qar"}
PINS = {
 "GzsTool.exe": "1a9c5b11e2355383ff485aee7e86abc026f5c1fad729daf8c0fd15ee0aae1c10",
 "GzsTool.Core.dll": "9da447ae3c375cce2e46744eeff6af50f1591062afdf479d1a0b49edb47daaa3",
 "CityHash.dll": "def6c4506d461b65e4059b2936b2cbd5f852ba5d1d8a1a527f1c0e6dc7008c8f",
 "Zlib.Portable.dll": "fe84781ba35ca9cc5ff5f73fd08d2a66c59e5257b4573f5fe59743f30bf78e42",
 "qar_dictionary.txt": "1558c248ed0a4bb827888261563fbb91a2df4f03999682f85d637ff70d9d5fb2",
 "fpk_dictionary.txt": "b82f9a8d6c10a68ba9471eca9d815c21355a53b5e68753d8ad7db7fd01bf401d",
}
SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT);
CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,relative_path TEXT,snapshot TEXT,kind TEXT,scope TEXT,active INTEGER,bytes INTEGER,mtime_ns INTEGER,header_count INTEGER,content_sha256 TEXT);
CREATE INDEX IF NOT EXISTS source_active ON sources(active,kind);
CREATE TABLE IF NOT EXISTS containers(id TEXT PRIMARY KEY,source_id TEXT REFERENCES sources(id),parent_occurrence TEXT,kind TEXT,name TEXT,depth INTEGER,state TEXT,reason TEXT,input_path TEXT,content_sha256 TEXT,index_path TEXT,index_sha256 TEXT,member_count INTEGER DEFAULT 0,attempts INTEGER DEFAULT 0);
CREATE INDEX IF NOT EXISTS container_state ON containers(state,source_id);
CREATE TABLE IF NOT EXISTS occurrences(id TEXT PRIMARY KEY,container_id TEXT REFERENCES containers(id),ordinal INTEGER,name TEXT,name_origin TEXT,resolved INTEGER,path_hash TEXT,hash_hex TEXT,extension_id TEXT,extension TEXT,offset INTEGER,declared_size INTEGER,compressed_size INTEGER,content_sha256 TEXT,actual_size INTEGER,metadata TEXT,UNIQUE(container_id,ordinal));
CREATE INDEX IF NOT EXISTS member_type ON occurrences(extension);
CREATE TABLE IF NOT EXISTS refs(container_id TEXT,ordinal INTEGER,name TEXT,name_origin TEXT,PRIMARY KEY(container_id,ordinal));
CREATE TABLE IF NOT EXISTS blobs(sha256 TEXT PRIMARY KEY,path TEXT,bytes INTEGER,last_used REAL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,at REAL,command TEXT,container_id TEXT,state TEXT,detail TEXT);
-- Upstream0.5.3 Read property names are swapped relative to Write storage semantics.
CREATE VIEW IF NOT EXISTS member_sizes AS SELECT o.id,o.declared_size AS stored_size,
 CASE WHEN c.kind='qar' THEN o.compressed_size ELSE NULL END AS declared_decoded_size,
 o.actual_size FROM occurrences o JOIN containers c ON c.id=o.container_id;
"""
class CatalogueError(Exception):
    pass

def jdump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()

def digest_file(path, charge=None):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            amount = MIB
            if charge and isinstance(getattr(charge, "__self__", None), Budget):
                if charge.__self__.remaining <= 0: raise CatalogueError("io_budget")
                amount = min(amount, charge.__self__.remaining)
            chunk = stream.read(amount)
            if not chunk: break
            if charge: charge(len(chunk))
            h.update(chunk)
    return h.hexdigest()

def inside(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def count_arg(value):
    if str(value).lower() == "all": return None
    result = int(value)
    if result <= 0: raise argparse.ArgumentTypeError("count must be positive or all")
    return result

def snapshot(path, header):
    s = Path(path).stat(follow_symlinks=False)
    return {"bytes": s.st_size, "mtime_ns": s.st_mtime_ns, "device": s.st_dev,
            "file_id": s.st_ino, "header_sha256": digest_bytes(header)}

def classify(relative, header):
    parts = relative.replace("\\", "/").lower().split("/")
    name = parts[-1]
    if any(x in parts for x in (".git", ".codex", ".agents", "backup", "backups", "saves", "save", "logs")):
        return "excluded", "protected_private"
    if name.endswith((".original", ".bak", ".backup", ".old", ".tmp")):
        return "excluded", "backup"
    if header.startswith(b"SQAR"):
        return "qar", "archive"
    if header.startswith(bytes.fromhex("3026b2758e66cf11a6d900aa0062ce6c")):
        return "asf", "loose_media"
    if header.startswith(b"foxfpk"):
        return ("fpkd" if len(header) > 6 and header[6] == ord("d") else "fpk"), "archive"
    if header.startswith(b"SBPL"): return "sbp", "archive"
    if header.startswith(b"PFTX"): return "pftxs", "archive"
    if name.endswith((".exe", ".dll", ".pdb", ".asi", ".config", ".ini", ".log", ".dmp", ".sav", ".json", ".xml")):
        return "excluded", "runtime_config"
    return "loose", "loose_asset"

def source_is_private(relative):
    parts = relative.replace("\\", "/").lower().split("/")
    return any(x in parts for x in (".git", ".codex", ".agents", "backup", "backups", "saves", "save", "logs"))

class Budget:
    def __init__(self, limit):
        self.limit, self.used = int(limit), 0
    @property
    def remaining(self):
        return self.limit - self.used
    def charge(self, n):
        if n < 0 or n > self.remaining: raise CatalogueError("io_budget")
        self.used += n

class Catalogue:
    def __init__(self, config):
        self.config = dict(config)
        self.game = Path(config["gameRoot"]).resolve()
        self.tool = Path(config["toolRoot"]).resolve()
        self.runtime = Path(config["runtimeRoot"]).resolve()
        self.export_root = Path(config.get("exportRoot", self.runtime.parent / "exports")).resolve()
        public = HERE.parent.parent
        for target in (self.runtime, self.export_root):
            if inside(target, self.game) or inside(target, public) or inside(target, self.tool):
                raise CatalogueError("runtime/export must be outside game, tools and public checkout")
        if inside(self.export_root, self.runtime) or inside(self.runtime, self.export_root):
            raise CatalogueError("runtime and export roots must be separate")
        self.max_container = int(config.get("maxContainerBytes", 256 * MIB))
        self.cache_limit = int(config.get("cacheBytes", 1024 * MIB))
        self.reserve = int(config.get("reserveBytes", 2048 * MIB))
        self.timeout = float(config.get("timeoutSeconds", 180))
        self.memory_limit = int(config.get("memoryBytes", 1536 * MIB))
        self.max_members = int(config.get("maxMembers", 1000000))
        self.max_depth = int(config.get("maxDepth", 8))
        if min(self.max_container, self.cache_limit, self.reserve, self.memory_limit, self.max_members, self.max_depth) <= 0:
            raise CatalogueError("budgets must be positive")
        self.budget = Budget(config.get("ioBytesPerRun", 2048 * MIB))
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.runtime / "catalogue.sqlite", timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.db.commit()
        self.process = None
        self.processes = 0
        self.decoded = 0

    def close(self):
        self.db.close()

    def event(self, command, container, state, detail=None):
        self.db.execute("INSERT INTO events(at,command,container_id,state,detail) VALUES(?,?,?,?,?)",
                        (time.time(), command, container, state, jdump(detail)))
        self.db.commit()

    def getmeta(self, key):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def setmeta(self, key, value):
        self.db.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (key, str(value)))
        self.db.commit()

    @contextlib.contextmanager
    def lock(self):
        path = self.runtime / "worker.lock"
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise CatalogueError("worker lock exists; inspect owner PID before manual recovery")
        try:
            os.write(fd, jdump({"pid": os.getpid(), "at": time.time()}).encode())
            os.close(fd)
            self.setmeta("cancel", "0")
            yield
        finally:
            path.unlink(missing_ok=True)

    def cancelled(self):
        if self.getmeta("cancel") == "1": raise KeyboardInterrupt

    def free_space(self, needed=0):
        if shutil.disk_usage(self.runtime).free < self.reserve + needed:
            raise CatalogueError("free_space_reserve")

    def ensure_bridge(self):
        pins = {}
        for name, expected in PINS.items():
            path = self.tool / name
            actual = digest_file(path, self.budget.charge)
            if actual != expected: raise CatalogueError("installed tool/dictionary pin mismatch: " + name)
            pins[name] = actual
        bridge_sha = digest_file(HERE / "archive_bridge.cs", self.budget.charge)
        recipe = digest_bytes(jdump({"pins": pins, "bridge": bridge_sha, "schema": 1}).encode())
        previous = self.getmeta("recipe")
        if previous and previous != recipe:
            raise CatalogueError("helper/tool recipe changed; choose a new runtime to preserve previous catalogue")
        self.setmeta("recipe", recipe)
        build = self.runtime / "helper" / recipe[:16]
        build.mkdir(parents=True, exist_ok=True)
        exe = build / "archive_bridge.exe"
        if not exe.exists():
            compiler = Path(os.environ.get("WINDIR", "C:/Windows")) / "Microsoft.NET/Framework64/v4.0.30319/csc.exe"
            if not compiler.is_file(): raise CatalogueError("Windows .NET Framework csc missing")
            for name in ("GzsTool.Core.dll", "CityHash.dll", "Zlib.Portable.dll"):
                shutil.copyfile(self.tool / name, build / name)
            command = [str(compiler), "/nologo", "/optimize+", "/target:exe", "/platform:x64",
                       "/out:" + str(exe), "/reference:" + str(self.tool / "GzsTool.Core.dll"),
                       str(HERE / "archive_bridge.cs")]
            p = subprocess.run(command, capture_output=True, timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            (build / "compile.log").write_bytes(p.stdout + p.stderr)
            if p.returncode or not exe.exists(): raise CatalogueError("bridge compile failed: " + str(build / "compile.log"))
            (build / "build.json").write_text(jdump({"recipe": recipe, "exe_sha256": digest_file(exe), "pins": pins}), encoding="utf-8")
        receipt = read_json(build / "build.json")
        if digest_file(exe, self.budget.charge) != receipt["exe_sha256"]: raise CatalogueError("helper executable changed")
        for name in ("GzsTool.Core.dll", "CityHash.dll", "Zlib.Portable.dll"):
            if digest_file(build / name, self.budget.charge) != PINS[name]: raise CatalogueError("cached helper DLL changed")
        self.exe = exe
        return recipe

    def memory_bytes(self, process):
        if os.name != "nt": return 0
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                (x, ctypes.c_size_t) for x in ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
        c = Counters()
        c.cb = ctypes.sizeof(c)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        fn = psapi.GetProcessMemoryInfo
        fn.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        fn.restype = wintypes.BOOL
        if not fn(wintypes.HANDLE(int(process._handle)), ctypes.byref(c), c.cb):
            raise CatalogueError("cannot enforce child memory guard")
        return max(c.WorkingSetSize, c.PagefileUsage)

    def bridge(self, action, kind, source, output, name="", ordinal=-1):
        self.cancelled()
        self.free_space(self.max_container if action == "extract" else 32 * MIB)
        output = Path(output)
        if output.exists(): raise CatalogueError("helper output already exists")
        output.parent.mkdir(parents=True, exist_ok=True)
        args = [str(self.exe), action, kind, str(source), str(output), str(self.tool), str(ordinal),
                name or "container", str(self.max_container), str(self.budget.remaining), str(self.max_members)]
        logpath = output.with_suffix(output.suffix + ".log")
        started = time.monotonic()
        self.processes += 1
        with open(logpath, "wb") as log:
            p = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            self.process = p
            try:
                while p.poll() is None:
                    self.cancelled()
                    if time.monotonic() - started > self.timeout: raise CatalogueError("child_timeout")
                    if self.memory_bytes(p) > self.memory_limit: raise CatalogueError("child_memory_budget")
                    time.sleep(0.1)
                code = p.wait()
            except BaseException:
                if p.poll() is None: p.terminate()
                p.wait(timeout=15)
                # Incomplete child has no reliable final byte receipt. Conservatively exhaust this run.
                self.budget.charge(self.budget.remaining)
                raise
            finally:
                self.process = None
        receipt_path = Path(str(output) + ".receipt.json")
        if not receipt_path.is_file(): raise CatalogueError("missing_helper_receipt")
        receipt = read_json(receipt_path)
        self.budget.charge(int(receipt["read_bytes"]))
        if action == "extract": self.decoded += 1
        if code or not receipt["ok"]: raise CatalogueError(receipt.get("error", "helper_failed"))
        return receipt

    def census(self):
        if not self.game.is_dir(): raise CatalogueError("game root missing")
        self.db.execute("UPDATE sources SET active=0")
        counts, total, walk_errors = {}, 0, []
        # Directory symlinks/junctions are not followed. Protected directories are counted as exclusions.
        for base, dirs, files in os.walk(self.game, followlinks=False, onerror=lambda e: walk_errors.append(str(e))):
            dirs.sort(key=str.casefold)
            for directory in dirs[:]:
                child = Path(base) / directory
                if child.is_symlink() or getattr(child, "is_junction", lambda: False)() or not inside(child, self.game):
                    dirs.remove(directory)
                    counts["excluded:directory_link"] = counts.get("excluded:directory_link", 0) + 1
            files.sort(key=str.casefold)
            for name in files:
                self.cancelled()
                path = Path(base) / name
                relative = path.relative_to(self.game).as_posix()
                if path.is_symlink() or not inside(path, self.game):
                    kind, scope, header = "excluded", "external_link", b""
                elif source_is_private(relative) or name.lower().endswith((".original", ".bak", ".backup", ".old")):
                    kind, scope, header = "excluded", "protected_private" if source_is_private(relative) else "backup", b""
                elif classify(relative, b"")[0] == "excluded":
                    kind, scope = classify(relative, b"")
                    header = b""
                else:
                    self.budget.charge(32)
                    with path.open("rb") as stream: header = stream.read(32)
                    kind, scope = classify(relative, header)
                snap = snapshot(path, header)
                sid = digest_bytes(jdump({"path": relative, "snapshot": snap}).encode())
                count = struct.unpack_from("<I", header, 8)[0] ^ 0x11C22050 if kind == "qar" else None
                self.db.execute("INSERT INTO sources VALUES(?,?,?,?,?,?,?,?,?,NULL) ON CONFLICT(id) DO UPDATE SET active=1",
                                (sid, relative, jdump(snap), kind, scope, 1, snap["bytes"], snap["mtime_ns"], count))
                if kind in ("qar", "fpk", "fpkd", "sbp", "pftxs"):
                    cid = digest_bytes((sid + ":root").encode())
                    self.db.execute("INSERT OR IGNORE INTO containers(id,source_id,kind,name,depth,state,input_path) VALUES(?,?,?,?,0,'pending',?)",
                                    (cid, sid, kind, relative, str(path)))
                key = scope + ":" + kind
                counts[key] = counts.get(key, 0) + 1
                total += 1
        self.db.commit()
        result = {"files": total, "classes": counts, "read_bytes": self.budget.used, "payload_decodes": 0, "unreadable_directories": len(walk_errors), "complete_filesystem_walk": not walk_errors}
        self.setmeta("census_walk_errors", jdump(walk_errors))
        self.event("census", None, "complete", result)
        return result

    def validate_source(self, source_id):
        row = self.db.execute("SELECT * FROM sources WHERE id=?", (source_id,)).fetchone()
        path = self.game / row["relative_path"]
        self.budget.charge(32)
        with path.open("rb") as stream: header = stream.read(32)
        if snapshot(path, header) != json.loads(row["snapshot"]): raise CatalogueError("source_snapshot_changed; run census")
        return path

    def import_index(self, cid, output, receipt):
        row = self.db.execute("SELECT * FROM containers WHERE id=?", (cid,)).fetchone()
        member_count = 0
        with Path(output).open(encoding="utf-8") as index_stream:
            for line in index_stream:
                item = json.loads(line)
                if item["record"] == "reference":
                    self.db.execute("INSERT OR REPLACE INTO refs VALUES(?,?,?,?)",
                                    (cid, item["ordinal"], item["name"], item["name_origin"]))
                    continue
                member_count += 1
                oid = digest_bytes((cid + ":" + str(item["ordinal"])).encode())
                old = self.db.execute("SELECT content_sha256,actual_size,metadata FROM occurrences WHERE id=?", (oid,)).fetchone()
                if old and old["metadata"] != jdump(item):
                    raise CatalogueError("indexed_member_changed")
                prior_sha, prior_size = (old["content_sha256"], old["actual_size"]) if old else (None, None)
                self.db.execute("""INSERT OR REPLACE INTO occurrences VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (oid, cid, item["ordinal"], item.get("name"), item.get("name_origin"), int(item.get("resolved", False)),
                     item.get("path_hash"), item.get("hash"), item.get("extension_id"), item["extension"], item["offset"],
                     item["declared_size"], item.get("compressed_size"), prior_sha, prior_size, jdump(item)))
                kind = KINDS.get(item["extension"])
                if kind:
                    child = digest_bytes((oid + ":container").encode())
                    state, reason = ("pending", None) if row["depth"] < self.max_depth else ("deferred", "depth_limit")
                    if item["declared_size"] > self.max_container: state, reason = "deferred", "container_budget"
                    self.db.execute("""INSERT OR IGNORE INTO containers(id,source_id,parent_occurrence,kind,name,depth,state,reason)
                                    VALUES(?,?,?,?,?,?,?,?)""",
                                    (child, row["source_id"], oid, kind, item.get("name"), row["depth"] + 1, state, reason))
        if member_count != receipt["member_count"]: raise CatalogueError("helper_member_count_mismatch")
        source = self.db.execute("SELECT * FROM sources WHERE id=?", (row["source_id"],)).fetchone()
        if row["depth"] == 0 and row["kind"] == "qar" and member_count != source["header_count"]: raise CatalogueError("header_count_mismatch")
        index_sha = digest_file(output, self.budget.charge)
        self.db.execute("UPDATE containers SET state='indexed',reason=NULL,index_path=?,index_sha256=?,member_count=? WHERE id=?",
                        (str(output), index_sha, member_count, cid))
        self.db.commit()

    def index_one(self, row):
        cid = row["id"]
        self.validate_source(row["source_id"])
        if row["depth"] > 0 and row["content_sha256"]:
            prior = self.db.execute("SELECT * FROM containers WHERE id<>? AND content_sha256=? AND kind=? AND state='indexed' ORDER BY id LIMIT 1",
                                    (cid, row["content_sha256"], row["kind"])).fetchone()
            if prior and Path(prior["index_path"]).is_file() and digest_file(prior["index_path"], self.budget.charge) == prior["index_sha256"]:
                self.import_index(cid, prior["index_path"], {"member_count": prior["member_count"]})
                self.event("index", cid, "content_index_cache_hit")
                return {"cache_hit": True, "member_count": prior["member_count"], "payload_decode_requested": False}
        self.validate_source(row["source_id"])
        output = self.runtime / "indexes" / (cid[:16] + "-" + uuid.uuid4().hex[:8] + ".jsonl")
        self.db.execute("UPDATE containers SET state='running',attempts=attempts+1 WHERE id=?", (cid,))
        self.db.commit()
        try:
            receipt = self.bridge("index", row["kind"], row["input_path"], output, row["name"])
            self.validate_source(row["source_id"])
            with self.db: self.import_index(cid, output, receipt)
            self.event("index", cid, "indexed", receipt)
            return receipt
        except BaseException as e:
            self.db.rollback()
            state = "cancelled" if isinstance(e, KeyboardInterrupt) else "failed"
            self.db.execute("UPDATE containers SET state=?,reason=? WHERE id=?", (state, str(e)[:2000], cid))
            self.db.commit()
            self.event("index", cid, state, {"error": str(e)})
            raise

    def index(self):
        self.ensure_bridge()
        completed = self.db.execute("""SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id
                               WHERE s.active=1 AND c.depth=0 AND c.state='indexed'""").fetchall()
        for item in completed:
            self.validate_source(item["source_id"])
            if not Path(item["index_path"]).is_file() or digest_file(item["index_path"], self.budget.charge) != item["index_sha256"]:
                self.db.execute("UPDATE containers SET state='pending',reason='stale_index' WHERE id=?", (item["id"],))
        self.db.commit()
        rows = self.db.execute("""SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id
                               WHERE s.active=1 AND c.depth=0 AND c.state IN ('pending','cancelled') ORDER BY s.relative_path""").fetchall()
        done = 0
        for row in rows:
            self.cancelled()
            self.index_one(row)
            done += 1
            print(jdump({"indexed_archives": done, "remaining": len(rows) - done, "last": row["name"]}), flush=True)
        return {"indexed_this_run": done, "payload_decodes": self.decoded, "helper_processes": self.processes, "read_bytes": self.budget.used}

    def cache_bytes(self):
        return self.db.execute("SELECT COALESCE(SUM(bytes),0) FROM blobs").fetchone()[0]

    def cache_room(self, needed, protect=()):
        if needed + self.staged_bytes() > self.cache_limit: raise CatalogueError("cache_budget")
        for blob in self.db.execute("SELECT * FROM blobs ORDER BY last_used,sha256").fetchall():
            if self.cache_bytes() + self.staged_bytes() + needed <= self.cache_limit: break
            if blob["sha256"] in protect: continue
            path = Path(blob["path"])
            if not inside(path, self.runtime / "blobs"): raise CatalogueError("cache_path_invalid")
            path.unlink(missing_ok=True)
            self.db.execute("DELETE FROM blobs WHERE sha256=?", (blob["sha256"],))
            self.db.execute("UPDATE containers SET input_path=NULL WHERE content_sha256=?", (blob["sha256"],))
        self.db.commit()
        if self.cache_bytes() + self.staged_bytes() + needed > self.cache_limit: raise CatalogueError("cache_budget")

    def cached(self, sha):
        if not sha: return None
        blob = self.db.execute("SELECT * FROM blobs WHERE sha256=?", (sha,)).fetchone()
        if not blob: return None
        path = Path(blob["path"])
        if path.is_file() and path.stat().st_size == blob["bytes"] and digest_file(path, self.budget.charge) == sha:
            self.db.execute("UPDATE blobs SET last_used=? WHERE sha256=?", (time.time(), sha))
            self.db.commit()
            return path
        self.db.execute("DELETE FROM blobs WHERE sha256=?", (sha,))
        self.db.execute("UPDATE containers SET input_path=NULL WHERE content_sha256=?", (sha,))
        self.db.commit()
        return None

    def prepare_container(self, row):
        self.validate_source(row["source_id"])
        cached = self.cached(row["content_sha256"])
        if cached: return cached
        occurrence = self.db.execute("SELECT * FROM occurrences WHERE id=?", (row["parent_occurrence"],)).fetchone()
        parent = self.db.execute("SELECT * FROM containers WHERE id=?", (occurrence["container_id"],)).fetchone()
        if parent["depth"] == 0:
            input_path = self.validate_source(parent["source_id"])
        else:
            input_path = self.prepare_container(parent)
        self.cache_room(self.max_container, (parent["content_sha256"],))
        self.free_space(self.max_container)
        stage = self.runtime / "stages" / uuid.uuid4().hex[:16]
        stage.mkdir(parents=True)
        output = stage / "payload.bin"
        try:
            receipt = self.bridge("extract", parent["kind"], input_path, output, parent["name"], occurrence["ordinal"])
            self.validate_source(row["source_id"])
            actual = output.stat().st_size
            if actual > self.max_container: raise CatalogueError("container_budget")
            sha = digest_file(output, self.budget.charge)
            if occurrence["content_sha256"] and occurrence["content_sha256"] != sha:
                raise CatalogueError("source_payload_changed_without_snapshot")
            target = self.runtime / "blobs" / sha[:16] / "payload.bin"
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if digest_file(target, self.budget.charge) != sha: raise CatalogueError("short_cache_key_collision")
                output.unlink()
            else:
                os.replace(output, target)
            self.db.execute("INSERT OR REPLACE INTO blobs VALUES(?,?,?,?)", (sha, str(target), actual, time.time()))
            self.db.execute("UPDATE containers SET input_path=?,content_sha256=? WHERE id=?", (str(target), sha, row["id"]))
            self.db.execute("UPDATE occurrences SET content_sha256=?,actual_size=? WHERE id=?", (sha, actual, occurrence["id"]))
            self.db.commit()
            return target
        except BaseException:
            # Retain bounded partial files for diagnostics; counted against staging space below.
            raise

    def staged_bytes(self):
        return sum(p.stat().st_size for p in (self.runtime / "stages").glob("*/payload.bin")) if (self.runtime / "stages").exists() else 0

    def expand(self, count, selected=None, retry=False):
        self.ensure_bridge()
        if retry:
            self.db.execute("UPDATE containers SET state='pending',reason=NULL WHERE depth>0 AND state IN ('failed','deferred') AND (? IS NULL OR id=?)", (selected, selected))
            self.db.commit()
        if selected:
            prior = self.db.execute("SELECT * FROM containers WHERE id=? AND state='indexed'", (selected,)).fetchone()
            if prior:
                self.validate_source(prior["source_id"])
                if Path(prior["index_path"]).is_file() and digest_file(prior["index_path"], self.budget.charge) == prior["index_sha256"]:
                    return {"attempts": 0, "indexed": 0, "cache_hit": True, "needs_attention": 0,
                            "payload_decodes": 0, "helper_processes": 0, "read_bytes": self.budget.used}
                self.db.execute("UPDATE containers SET state='pending',reason='stale_index' WHERE id=?", (selected,))
                self.db.commit()
        rows = self.db.execute("""SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id
             WHERE s.active=1 AND c.depth>0 AND c.state IN ('pending','cancelled') AND (? IS NULL OR c.id=?)
             ORDER BY s.relative_path,c.depth,c.name,c.id""", (selected, selected)).fetchall()
        attempts, complete, errors = 0, 0, 0
        # Requery after each attempt: newly discovered nested children are included in this explicitly selected budget.
        while rows and (count is None or attempts < count):
            self.cancelled()
            row = rows[0]
            attempts += 1
            self.db.execute("UPDATE containers SET state='running',attempts=attempts+1 WHERE id=?", (row["id"],))
            self.db.commit()
            try:
                if row["depth"] > self.max_depth:
                    raise CatalogueError("depth_limit")
                path = self.prepare_container(row)
                current = dict(self.db.execute("SELECT * FROM containers WHERE id=?", (row["id"],)).fetchone())
                current["input_path"] = str(path)
                self.index_one(current)
                complete += 1
            except KeyboardInterrupt:
                self.db.execute("UPDATE containers SET state='cancelled',reason='cancelled' WHERE id=?", (row["id"],))
                self.db.commit()
                raise
            except Exception as e:
                self.db.execute("UPDATE containers SET state='deferred',reason=? WHERE id=?", (str(e)[:2000], row["id"]))
                self.db.commit()
                self.event("expand", row["id"], "deferred", {"error": str(e)})
                errors += 1
                if self.budget.remaining <= 0: break
            rows = self.db.execute("""SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id
                 WHERE s.active=1 AND c.depth>0 AND c.state IN ('pending','cancelled') AND (? IS NULL OR c.id=?)
                 ORDER BY s.relative_path,c.depth,c.name,c.id""", (selected, selected)).fetchall()
        result = {"attempts": attempts, "indexed": complete, "needs_attention": errors, "payload_decodes": self.decoded,
                  "helper_processes": self.processes, "read_bytes": self.budget.used}
        self.event("expand", selected, "complete" if not errors else "needs_attention", result)
        return result

    def status(self):
        classes = dict(self.db.execute("SELECT scope||':'||kind,COUNT(*) FROM sources WHERE active=1 GROUP BY scope,kind").fetchall())
        coverage = [dict(r) for r in self.db.execute("""SELECT CASE WHEN c.depth=0 THEN 'outer' ELSE 'nested' END AS layer,c.state,COUNT(*) AS containers,
                    SUM(c.member_count) AS members FROM containers c JOIN sources s ON s.id=c.source_id
                    WHERE s.active=1 GROUP BY c.depth=0,c.state""")]
        types = dict(self.db.execute("""SELECT o.extension,COUNT(*) FROM occurrences o JOIN containers c ON c.id=o.container_id
                                     JOIN sources s ON s.id=c.source_id WHERE s.active=1 GROUP BY o.extension ORDER BY o.extension""").fetchall())
        unknown = self.db.execute("""SELECT COUNT(*) FROM occurrences o JOIN containers c ON c.id=o.container_id
                                    JOIN sources s ON s.id=c.source_id WHERE s.active=1 AND o.resolved=0""").fetchone()[0]
        pending = [dict(r) for r in self.db.execute("""SELECT c.id,c.name,c.kind,c.depth,o.declared_size AS stored_size,CASE WHEN pc.kind='qar' THEN o.compressed_size ELSE NULL END AS declared_decoded_size FROM containers c
                   JOIN sources s ON s.id=c.source_id LEFT JOIN occurrences o ON o.id=c.parent_occurrence LEFT JOIN containers pc ON pc.id=o.container_id
                   WHERE s.active=1 AND c.depth>0 AND c.state IN ('pending','cancelled')
                   ORDER BY s.relative_path,c.depth,c.name,c.id LIMIT 10""")]
        scopes = [dict(r) for r in self.db.execute("""SELECT CASE WHEN s.relative_path LIKE 'master/%' THEN 'TPP-master'
                  WHEN s.relative_path LIKE 'mgo/%' THEN 'MGO' ELSE 'other-install' END AS asset_scope,
                  COUNT(*) AS archives,SUM(c.member_count) AS indexed_members,SUM(s.header_count) AS header_members
                  FROM sources s JOIN containers c ON c.source_id=s.id WHERE s.active=1 AND c.depth=0 AND s.kind='qar'
                  GROUP BY asset_scope""")]
        origins = dict(self.db.execute("""SELECT o.name_origin,COUNT(*) FROM occurrences o JOIN containers c ON c.id=o.container_id
                      JOIN sources s ON s.id=c.source_id WHERE s.active=1 GROUP BY o.name_origin""").fetchall())
        return {"scope": "as-installed occurrences; runtime priority unresolved", "filesystem_classes": classes,
                "archive_scopes": scopes, "name_origins": origins, "next_nested": pending,
                "next_cursor": pending[0]["id"] if pending else None,
                "container_coverage": coverage, "types": types, "unresolved_names": unknown,
                "dependency_resolved": 0, "previews": 0, "cache_bytes": self.cache_bytes(),
                "partial_stage_bytes": self.staged_bytes(), "full_archive_hashes_computed": 0,
                "unsupported_formats_remain_indexed": True, "filesystem_walk_errors": json.loads(self.getmeta("census_walk_errors") or "[]")}

    def export(self):
        self.export_root.mkdir(parents=True, exist_ok=True)
        dest = self.export_root / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
        dest.mkdir()
        out = sqlite3.connect(dest / "catalogue.sqlite")
        out.executescript("""CREATE TABLE sources(id TEXT,relative_path TEXT,kind TEXT,scope TEXT,bytes INTEGER,header_count INTEGER,full_sha256 TEXT);
          CREATE TABLE containers(id TEXT,source_id TEXT,parent_occurrence TEXT,kind TEXT,name TEXT,depth INTEGER,state TEXT,index_sha256 TEXT,member_count INTEGER,content_sha256 TEXT);
          CREATE TABLE occurrences(id TEXT,container_id TEXT,ordinal INTEGER,name TEXT,name_origin TEXT,resolved INTEGER,hash_hex TEXT,extension_id TEXT,extension TEXT,offset INTEGER,stored_size INTEGER,declared_decoded_size INTEGER,content_sha256 TEXT,actual_size INTEGER,metadata_json TEXT);
          CREATE TABLE refs(container_id TEXT,ordinal INTEGER,name TEXT,name_origin TEXT);""")
        tables = {
          "sources": "SELECT id,relative_path,kind,scope,bytes,header_count,content_sha256 FROM sources WHERE active=1",
          "containers": "SELECT c.id,c.source_id,c.parent_occurrence,c.kind,c.name,c.depth,c.state,c.index_sha256,c.member_count,c.content_sha256 FROM containers c JOIN sources s ON s.id=c.source_id WHERE s.active=1",
          "occurrences": "SELECT o.id,o.container_id,o.ordinal,o.name,o.name_origin,o.resolved,o.hash_hex,o.extension_id,o.extension,o.offset,o.declared_size AS stored_size,CASE WHEN c.kind='qar' THEN o.compressed_size ELSE NULL END AS declared_decoded_size,o.content_sha256,o.actual_size,o.metadata FROM occurrences o JOIN containers c ON c.id=o.container_id JOIN sources s ON s.id=c.source_id WHERE s.active=1",
          "refs": "SELECT r.* FROM refs r JOIN containers c ON c.id=r.container_id JOIN sources s ON s.id=c.source_id WHERE s.active=1",
        }
        for table, query in tables.items():
            cursor = self.db.execute(query)
            fields = [x[0] for x in cursor.description]
            with (dest / (table + ".csv")).open("w", encoding="utf-8", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(fields)
                for row in cursor:
                    values = tuple(row)
                    out.execute("INSERT INTO " + table + " VALUES(" + ",".join("?" for _ in values) + ")", values)
                    writer.writerow(values)
        out.commit()
        out.close()
        provenance = {"schema_version": 1, "scope": "as-installed source snapshots; unresolved runtime priority",
                      "external_reader": "Atvaark GzsTool.Core0.5.3",
                      "source_revision": "fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5",
                      "tool_and_dictionary_sha256": PINS, "index_recipe": self.getmeta("recipe"),
                      "bridge_source_sha256": digest_file(HERE / "archive_bridge.cs", self.budget.charge),
                      "orchestrator_source_sha256": digest_file(HERE / "catalogue.py", self.budget.charge),
                      "full_archive_sha256": None,
                      "size_semantics": "stored_size is on-disk member length; declared_decoded_size is the QAR header decoded-size field; actual_size is measured after selected decoding"}
        (dest / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
        exported_status = self.status()
        exported_status["filesystem_walk_errors"] = len(exported_status["filesystem_walk_errors"])
        (dest / "status.json").write_text(json.dumps(exported_status, indent=2), encoding="utf-8")
        (dest / "README.md").write_text("# As-installed asset metadata\n\nOuter archive indexes, nested container coverage, dependencies and previews are separate. Unknown names/types and all occurrences are retained. Content hashes are null until actual selected bytes were hashed; full archive hashes are unknown. No runtime override priority or universal rendering is claimed. Raw payloads, private paths and operational DB are excluded.\n", encoding="utf-8")
        return {"export": str(dest)}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", default=os.environ.get("MGSV_CATALOGUE_CONFIG", str(HERE / "config.local.json")))
    sub = p.add_subparsers(dest="command")
    for command in ("census", "index", "status", "cancel", "export", "menu"): sub.add_parser(command)
    ep = sub.add_parser("expand")
    ep.add_argument("--count", required=True, type=count_arg)
    ep.add_argument("--container")
    ep.add_argument("--retry-review", action="store_true")
    args = p.parse_args(argv)
    cat = None
    try:
        cat = Catalogue(read_json(args.config))
        command = args.command or "menu"
        if command == "cancel":
            cat.setmeta("cancel", "1")
            print(jdump({"cancel_requested": True}))
            return 0
        if command == "status":
            print(json.dumps(cat.status(), indent=2))
            return 0
        with cat.lock():
            if command == "census": result = cat.census()
            elif command == "index": result = cat.index()
            elif command == "expand": result = cat.expand(args.count, args.container, args.retry_review)
            elif command == "export": result = cat.export()
            else:
                print("As-installed MGSV catalogue: filesystem + outer index; nested expansion is separate.")
                print(jdump(cat.census()))
                print(jdump(cat.index()))
                print(json.dumps(cat.status(), indent=2))
                text = input("Nested containers to attempt [0 = index only; positive count or all]: ").strip() or "0"
                if text != "0":
                    amount = count_arg(text)
                    print(jdump(cat.expand(amount)))
                result = cat.export()
            print(json.dumps(result, indent=2))
            return 1 if result.get("needs_attention") else 0
    except KeyboardInterrupt:
        print("Cancelled; completed work retained. Restart to resume.", file=sys.stderr)
        return 130
    except Exception as e:
        print(type(e).__name__ + ": " + str(e), file=sys.stderr)
        return 2
    finally:
        if cat: cat.close()

if __name__ == "__main__":
    raise SystemExit(main())
