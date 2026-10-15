"""Build deterministic, asset-free IMB download archives using Python's standard library."""
from pathlib import Path
import argparse, hashlib, json, re, zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = ('core/', 'companion/', 'experimental-sdk/', 'resources-authored/',
            'resource-tools/', 'tests/', 'platforms/', 'installer/', 'tools/', 'research/')
ROOT_FILES = {'README.md', 'LICENSE', 'LICENSE-SCOPE.md', 'CONTRIBUTING.md', 'CONTRIBUTORS.md',
              'ROADMAP.md', 'INSTALL.md', 'CREDITS.md', 'CHANGELOG.md', 'VERSION', 'VERSIONING.md',
              '.gitignore', 'Install.cmd', 'Uninstall.cmd', 'DEPENDENCIES-AND-COMPATIBILITY.md', 'source-manifest.json', 'release-content.json', 'DOWNLOADS.md'}
ALLOWED = {'.py', '.lua', '.md', '.json', '.txt', '.cs', '.xml', '.cjs', '.js', '.html', '.cmd', '.bsdiff'}
GENERATED = {'source-manifest.json', 'release-content.json', 'installer/package-manifest.json'}
IGNORED = {'.git', '__pycache__', 'private-builds', 'build', 'dist'}
# Gameplay showcase recordings are documented separately, never installed or relicensed as code.
SHOWCASE_PREFIX = 'media/showcase/'
DOCS = ['README.md', 'INSTALL.md', 'CREDITS.md', 'CONTRIBUTORS.md', 'LICENSE', 'LICENSE-SCOPE.md',
        'VERSION', 'VERSIONING.md', 'CHANGELOG.md', 'DOWNLOADS.md', 'CONTRIBUTING.md', 'ROADMAP.md',
        'source-manifest.json', 'release-content.json', 'DEPENDENCIES-AND-COMPATIBILITY.md']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if any(x in IGNORED for x in path.relative_to(root).parts) or not path.is_file():
            continue
        if rel.startswith(SHOWCASE_PREFIX):
            continue
        if not (rel in ROOT_FILES or rel.startswith(PREFIXES)):
            raise ValueError('Unreviewed public file: ' + rel)
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Linked/escaped source: ' + rel)
        if path.suffix not in ALLOWED and rel not in ROOT_FILES and path.name not in ('LICENSE', '.gitignore'):
            raise ValueError('Unsupported or game-derived payload: ' + rel)
        if path.name in ('config.local.json', 'imb-life-save.lua', 'imb-native-ranks.lua'):
            raise ValueError('Private runtime data: ' + rel)
        data = path.read_bytes()
        if path.suffix != '.bsdiff':
            text = data.decode('utf-8-sig')
            if re.search(r'[A-Z]:[\\/](?:Users[\\/]|MGSV Modding[\\/]|SteamLibrary[\\/])', text):
                raise ValueError('Machine-specific path: ' + rel)
            if re.search(r'gh[pousr]_[A-Za-z0-9]{25,}|sk-[A-Za-z0-9]{32,}|github_pat_[A-Za-z0-9_]{25,}', text):
                raise ValueError('Potential credential: ' + rel)
        result[rel] = data
    return result


def archive(out, top, files):
    if out.exists():
        raise ValueError('Refusing to overwrite released archive: ' + str(out))
    with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(top + '/' + name, date_time=(2026, 10, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC verification failed')
        actual = {i.filename: z.read(i.filename) for i in z.infolist()}
        if actual != {top + '/' + k: v for k, v in files.items()}:
            raise ValueError('ZIP byte inventory mismatch')
    return dict(name=out.name, bytes=out.stat().st_size, sha256=sha(out.read_bytes()), files=len(files))


def build(output):
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?', version):
        raise ValueError('Invalid VERSION')
    menu = (ROOT / 'core/GameDir/mod/modules/ImmersiveMotherBase.lua').read_text(encoding='utf-8')
    if 'VERSION="' + version + '"' not in menu:
        raise ValueError('Installed menu VERSION does not match central VERSION')
    if not (ROOT / 'installer/install.py').is_file():
        raise ValueError('Missing installer')
    files = inventory(ROOT)
    source = {p: {'sha256': sha(b), 'bytes': len(b)} for p, b in files.items() if p not in GENERATED}
    digest = sha(json.dumps(source, sort_keys=True, separators=(',', ':')).encode('utf-8'))
    core = []
    for p, b in files.items():
        if p.startswith('core/GameDir/mod/') and p.endswith('.lua'):
            core.append({'source': p, 'target': p.removeprefix('core/GameDir/'), 'sha256': sha(b), 'size': len(b)})
    if len(core) != 20:
        raise ValueError('Unexpected core Lua inventory')
    metadata = dict(schemaVersion=1, product='Immersive Mother Base', version=version,
        license='GPL-3.0-only', nativeAcceptance=False, sourceCommit=None,
        sourceTag='v' + version, sourceTreeSha256=digest,
        supportedFeatures=['regular Soldier2 observation and persistent needs/identity',
            'rank-limited hierarchy, bounded updates and native patrol dispatch',
            'one owned IH menu, diagnostics and action recorder',
            'optional local companion; no extra IH actor adoption'],
        unavailableFeatures=['clean-resource-dependent muster and gatherings',
            'CQC, shower, rest/sleep and measured native service routines',
            'full platform navigation, completed interiors and dynamic specialist actors'], files=core)
    dump(ROOT / 'installer/package-manifest.json', metadata)
    prior = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
    prior.update(version=version, nativeAcceptance=False, sourceTag='v' + version, sourceTreeSha256=digest)
    prior['coreLua'] = {e['source'].removeprefix('core/'): {'candidateSha256': e['sha256']} for e in core}
    dump(ROOT / 'source-manifest.json', prior)
    dump(ROOT / 'release-content.json', dict(schema=1, version=version, sourceTag='v'+version,
        sourceTreeSha256=digest, excludes=sorted(GENERATED)+['dist/'], files=source))
    files = inventory(ROOT)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    docs = {p: files[p] for p in DOCS}
    prefix = 'Immersive-Mother-Base-' + version
    packages = []
    groups = [('core', dict(docs, **{p:b for p,b in files.items() if p.startswith(('core/', 'installer/')) or p in ('Install.cmd','Uninstall.cmd')})),
              ('companion', dict(docs, **{p:b for p,b in files.items() if p.startswith('companion/')})),
              ('command-platform-1-history', dict(docs, **{p:b for p,b in files.items() if p.startswith('platforms/')})),
              ('source', files)]
    for kind, payload in groups:
        packages.append(archive(output / (prefix+'-'+kind+'.zip'), prefix+'-'+kind, payload))
    receipt = dict(schema=1, version=version, sourceTag='v'+version, sourceTreeSha256=digest,
        nativeAcceptance=False, assetsRedistributed=False, packages=packages)
    dump(output / 'release-manifest.json', receipt)
    (output / 'SHA256SUMS.txt').write_text(''.join(e['sha256']+'  '+e['name']+'\n' for e in packages), encoding='utf-8')
    print(json.dumps(receipt, indent=2))
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist'/((ROOT/'VERSION').read_text(encoding='utf-8').strip()))
    build(parser.parse_args().output)
