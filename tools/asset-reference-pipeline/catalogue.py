"""Portable public catalogue export. Never copy the private operational database."""
import csv
import json
from pathlib import Path
import re
import shutil
import sqlite3
from runtime import canonical, inside, save, sha, ManualReview

CREDITS = """# Sources and credits

Game models/textures: Konami, Metal Gear Solid V: The Phantom Pain. No original game payloads are included.
Community tools: [Atvaark GzsTool](https://github.com/Atvaark/GzsTool) and
[Atvaark FtexTool](https://github.com/Atvaark/FtexTool).
Format reference: [BobDoleOwndU FMDL Studio v2](https://github.com/BobDoleOwndU/FMDL-Studio-v2),
reader revision d580b94215cc007df6c38bdb0bfce6a0f30e4701.
Rendering/encoding: [Blender](https://www.blender.org/) and [Pillow](https://python-pillow.org/).
Project owner: arsenal-pt. Authored pipeline/research developed entirely using AI LLM assistance (OpenAI Codex).
Eligible authored code is GPL-3.0; game art and third-party tools retain their own ownership/licenses.
This is an offline reference: actual base texture/UVs, approximate studio shader, static camera orbit.
Native FOX shading, LOD thresholds, collisions and in-game behavior are not reproduced.
"""


def public_scan(value):
    text = canonical(value) if not isinstance(value, str) else value
    if re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\|/(?:Users|home|tmp|mnt|private)/', text, re.I):
        raise ManualReview('Public export contains an absolute machine/private path')


def cell(value):
    return str(value).replace('|', '/').replace('\n', ' ').replace('\r', ' ')


def export_catalogue(store, destination, jobs):
    destination = Path(destination).resolve()
    if inside(destination, store.root) or inside(store.root, destination):
        raise ManualReview('Publication export must be separate from private runtime')
    if destination.exists() and any(destination.iterdir()):
        raise ManualReview('Export destination must be empty/new')
    rows = []
    for key in jobs:
        row = store.job(key)
        if row['status'] != 'complete':
            raise ManualReview('Only completed jobs may be exported: ' + key)
        asset = store.db.execute('SELECT record FROM assets WHERE job_id=?', (key,)).fetchone()
        if asset is None:
            raise ManualReview('Completed asset record missing')
        rows.append(json.loads(asset[0]))
    rows.sort(key=lambda x: x['id'])
    if len({r['id'] for r in rows}) != len(rows):
        raise ManualReview('Duplicate variant IDs would collide in public media/detail names')
    public_scan(rows)
    destination.mkdir(parents=True, exist_ok=True)
    media = destination / 'media'
    media.mkdir()
    details = destination / 'details'
    details.mkdir()
    for key in jobs:
        result = json.loads(store.job(key)['result'])
        for item in result['media']:
            source = Path(item['file'])
            if not inside(source, store.root) or source.suffix.lower() not in ('.png', '.gif'):
                raise ManualReview('Only validated private runtime rendered PNG/GIF may be copied')
            if sha(source) != item['sha256']:
                raise ManualReview('Rendered output changed after job completion')
            shutil.copyfile(source, media / source.name)
    for record in rows:
        detail = [f"# {cell(record['title'])}", '', cell(record['description']), '',
                  f"![Full reference](../{record['still']})", '',
                  f"![Camera 360 reference](../{record['gif']})", '',
                  f"Quality: native LOD{record['lod']}, {record['triangles']} triangles. "
                  f"Base texture: {cell(record['baseTextureSummary'])}.", '',
                  'Retained native LODs are inventoried below; identical index content maps to one identity.',
                  '', '| Native LOD | Triangles | Native index content SHA256 |', '|---|---:|---|']
        detail += [f"| {q['nativeLod']} | {q['triangles']} | {q['indicesSha256']} |" for q in record['nativeLods']]
        fence = chr(96) * 3
        detail += ['', fence + 'json', json.dumps(record, indent=2, ensure_ascii=False), fence, '',
                   '[Sources, tool credits and limitations](../sources-and-credits.md)', '']
        (details / (record['id'] + '.md')).write_text('\n'.join(detail), encoding='utf-8', newline='\n')
    links = []
    for start in range(0, len(rows), 12):
        name = f'table-{start//12+1}.md'
        links.append(f'- [Selected references {start+1}-{min(start+12,len(rows))}]({name})')
        table = ['# Selected references', '',
                 '| Preview | Asset | Category | Tags | Description | Quality / LOD | Base texture | Model / container |',
                 '|---|---|---|---|---|---|---|---|']
        for r in rows[start:start+12]:
            link = f"details/{r['id']}.md"
            table.append(f"| [![{cell(r['title'])}]({r['thumbnail']})]({link}) | [{cell(r['title'])}]({link}) | "
                         f"{cell(r['category'])} | {cell(', '.join(r['tags']))} | {cell(r['description'])} | "
                         f"Native LOD{r['lod']}; {r['triangles']} triangles | {cell(r['baseTextureSummary'])} | "
                         f"{cell(r['modelPath'])}<br>{cell(r['containerPath'] or 'Prepared native file; container unknown')} |")
        (destination / name).write_text('\n'.join(table) + '\n', encoding='utf-8', newline='\n')
    (destination / 'README.md').write_text('# Selected asset reference export\n\n'
        'Index loads no images. Tables show at most twelve static thumbnails; open one detail for a larger still/GIF.\n\n'
        + '\n'.join(links) + '\n\n[Sources and limits](sources-and-credits.md)\n', encoding='utf-8', newline='\n')
    (destination / 'sources-and-credits.md').write_text(CREDITS, encoding='utf-8', newline='\n')
    save(destination / 'catalogue.json', {'schemaVersion': 1, 'assets': rows})
    fields = ['id','title','category','tags','description','modelPath','modelSha256','containerPath','containerSha256',
              'lod','triangles','baseTextureSummary','still','gif','thumbnail']
    with (destination / 'catalogue.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: ', '.join(r[k]) if k == 'tags' else r.get(k) for k in fields})
    # Fresh whitelist schema, not ATTACH/copy/backup of private jobs.sqlite.
    db = sqlite3.connect(destination / 'catalog.sqlite')
    db.executescript('''CREATE TABLE assets(id TEXT PRIMARY KEY,title TEXT,category TEXT,tags TEXT,description TEXT,
       model_path TEXT,model_sha256 TEXT,container_path TEXT,container_sha256 TEXT,
       lod INTEGER,triangles INTEGER,still TEXT,gif TEXT,thumbnail TEXT,provenance_json TEXT);
       CREATE TABLE lods(asset_id TEXT,native_lod INTEGER,triangles INTEGER,indices_sha256 TEXT,duplicate_of INTEGER);
       CREATE TABLE textures(asset_id TEXT,material_index INTEGER,native_path_hash TEXT,width INTEGER,height INTEGER,
       mip_count INTEGER,dds_sha256 TEXT);''')
    for r in rows:
        db.execute('INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   (r['id'],r['title'],r['category'],canonical(r['tags']),r['description'],r['modelPath'],r['modelSha256'],
                    r['containerPath'],r['containerSha256'],r['lod'],r['triangles'],r['still'],r['gif'],r['thumbnail'],canonical(r)))
        for q in r['nativeLods']:
            db.execute('INSERT INTO lods VALUES(?,?,?,?,?)',
                       (r['id'],q['nativeLod'],q['triangles'],q['indicesSha256'],q.get('duplicateOf')))
        for t in r['baseTextures']:
            db.execute('INSERT INTO textures VALUES(?,?,?,?,?,?,?)',
                       (r['id'],t['materialIndex'],str(t['nativePathHash']),t['width'],t['height'],t['mipCount'],t['sha256']))
    db.commit()
    for name in ('assets', 'lods', 'textures'):
        for row in db.execute('SELECT * FROM ' + name):
            public_scan(list(row))
    db.close()
    allowed = {'.json','.csv','.md','.png','.gif','.sqlite'}
    for p in destination.rglob('*'):
        if p.is_file():
            if p.suffix not in allowed or not inside(p, destination):
                raise ManualReview('Unexpected publication payload')
            if p.suffix in ('.json','.csv','.md'):
                public_scan(p.read_text(encoding='utf-8'))
    inventory = [{'path': p.relative_to(destination).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
                 for p in sorted(destination.rglob('*')) if p.is_file()]
    save(destination / 'manifest.json', {'schemaVersion': 1, 'files': inventory})
    return {'assets': len(rows), 'files': len(inventory) + 1, 'manifestSha256': sha(destination / 'manifest.json')}
