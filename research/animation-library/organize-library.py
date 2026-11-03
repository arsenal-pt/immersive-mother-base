"""Build bounded browsing navigation from the published catalogue, without reading media.

GPL-3.0-only. This is a metadata-only postprocessor; catalogue, CSV, clip pages,
legacy tables, credits and rendered media remain byte-for-byte inputs.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath
import posixpath
import re

LIB = 'research/animation-library'
CATALOGUE = LIB + '/catalogue.json'
CSV = LIB + '/catalogue.csv'
README = LIB + '/README.md'
MAX_TEXT = 64 * 1024 * 1024
MAX_PAGE_BYTES = 16 * 1024 * 1024
PAGE_SIZE = 4

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Invalid public repository path')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or ':' in value:
        raise ValueError('Non-relative public repository path')
    return value

def read(root, name, maximum=MAX_TEXT):
    path = root / safe_path(name)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > maximum:
        raise ValueError('Missing, linked or oversized input: ' + name)
    return path.read_bytes()

def link(current, target):
    return posixpath.relpath(safe_path(target), posixpath.dirname(current))

def cell(value):
    return html.escape(str(value if value is not None else 'Unverified'), quote=True).replace('|', '&#124;').replace('\n', ' ')

def code(value):
    return '<code>' + cell(value) + '</code>'

def validate(catalogue, csv_raw, expected_count):
    entries = catalogue['entries']
    if len(entries) != expected_count or catalogue['entryCount'] != expected_count:
        raise ValueError('Published entry count changed; review a new baseline')
    groups = {g['id']: g['title'] for g in catalogue['groups']}
    if len(groups) != len(catalogue['groups']):
        raise ValueError('Duplicate group')
    ids = []
    for e in entries:
        ids.append(e['id'])
        if not isinstance(e['id'], str) or not e['id'] or e['group'] not in groups:
            raise ValueError('Invalid entry identity or group')
        if not isinstance(e['shortIdentifier'], str) or not e['shortIdentifier']:
            raise ValueError('Missing exact clip label')
        safe_path(e['detailPage'])
        if not e['detailPage'].startswith(LIB + '/clips/'):
            raise ValueError('Detail path outside library')
        for name in ('fullGif', 'animatedThumbnail', 'stillThumbnail'):
            m = e['media'][name]
            safe_path(m['path'])
            if not m['path'].startswith('media/animation-previews/') or not re.fullmatch('[0-9a-f]{64}', m['sha256']):
                raise ValueError('Invalid existing media reference')
            if type(m['bytes']) is not int or m['bytes'] < 1:
                raise ValueError('Invalid media byte count')
        for name in ('animatedThumbnail', 'stillThumbnail'):
            for axis in ('width', 'height'):
                value = e['media'][name][axis]
                if type(value) not in (int, float) or not 0 < value < float('inf'):
                    raise ValueError('Invalid selected-media dimension')
        if not e['media']['animatedThumbnail']['path'].lower().endswith('.gif'):
            raise ValueError('Animated reference extension changed')
        if not e['media']['stillThumbnail']['path'].lower().endswith('.png'):
            raise ValueError('Still reference extension changed')
        if not isinstance(e['description']['text'], str) or not isinstance(e['tags'], list):
            raise ValueError('Missing authored browsing description/tags')
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate published ID')
    rows = list(csv.DictReader(io.StringIO(csv_raw.decode('utf-8'))))
    if len(rows) != expected_count or {r['id'] for r in rows} != set(ids):
        raise ValueError('CSV and JSON identities disagree')
    return entries, groups

def family(e):
    if e['group'] != 'stock-soldier':
        return '', ''
    directory = e['locations'].get('ganiDirectory')
    if not isinstance(directory, str) or not directory.startswith('/Assets/'):
        return 'Unrecorded source directory', 'unrecorded'
    directory = directory.rstrip('/')
    token = posixpath.basename(directory)
    slug = re.sub('[^a-z0-9]+', '-', token.lower()).strip('-') or 'source'
    return directory, slug + '-' + sha(directory.encode())[:8]

def pack(entries):
    pages, current, size = [], [], 0
    for e in sorted(entries, key=lambda x: (x['shortIdentifier'].casefold(), x['id'])):
        n = e['media']['animatedThumbnail']['bytes']
        if current and (len(current) == PAGE_SIZE or size + n > MAX_PAGE_BYTES):
            pages.append(current)
            current, size = [], 0
        current.append(e)
        size += n
    if current:
        pages.append(current)
    return pages

def table_row(e, current, stills):
    detail = link(current, e['detailPage'])
    media = e['media']['stillThumbnail' if stills else 'animatedThumbnail']
    dims = media
    height = round(dims['height'] * 160 / dims['width'])
    image = '<a href="' + detail + '"><img src="' + link(current, media['path']) + '" width="160" height="' + str(height) + '" alt="' + cell(e['title']) + '"></a>'
    loc = e['locations']
    gani = code(loc.get('ganiDirectory')) + '<br>' + code(posixpath.basename(loc.get('ganiVirtualPath') or e['shortIdentifier']))
    if e['group'] == 'stock-soldier':
        location = 'Retained MTAR: ' + code(loc.get('archiveFile')) + '<br>DAT / FPK membership unverified'
    else:
        location = 'MTAR: ' + code(loc.get('archiveVirtualPath') or loc.get('archiveFile')) + '<br>Outer DAT / FPK origins: historical; see full data'
    timing = str(e['rawFrameCount']) + ' raw<br>' + str(e['previewDurationMilliseconds'] / 1000) + ' s chosen; native rate unknown'
    fields = [image, '[' + cell(e['title']) + '](' + detail + ')<br>' + code(e['shortIdentifier']), cell(e['category']['label']), '<br>'.join(code(t) for t in e['tags']), gani, location, cell(e['description']['text']), timing + '<br>[Full data](' + detail + '#technical-data)']
    return '| ' + ' | '.join(fields) + ' |'

def render_page(page, stills):
    current = page['stills' if stills else 'animated']
    sibling = page['animated' if stills else 'stills']
    mode = 'Still images: no GIFs loaded' if stills else 'Animated references'
    image_bytes = sum(e['media']['stillThumbnail' if stills else 'animatedThumbnail']['bytes'] for e in page['entries'])
    lines = ['# ' + page['title'] + ' - page ' + str(page['number']), '', '[Library](../README.md) · [Grouped directory](../browse/README.md) · [This source family](' + link(current, page['familyIndex']) + ') · [Switch mode](' + link(current, sibling) + ')', '', '**' + mode + '** · ' + str(len(page['entries'])) + ' clips · ' + format(image_bytes / 1048576, '.2f') + ' MiB downloaded.', '', 'Images reuse existing files. A small display width does not reduce download size. ' + ('Animated previews use full existing GIFs where no separate thumbnail exists. ' if not stills else '') + 'Open one clip for its larger titled GIF and original technical data.', '', 'Source-family grouping uses only recorded virtual directories; it does not establish an action, weapon, actor, rig or native compatibility. Existing descriptions and tags below are unchanged. Per-clip visual review may be pending; chosen preview speed is separate from unmeasured native timing.', '', '| Preview | Animation | Category | Tags | Virtual GANI directory / file | MTAR / container location | Description | Frames / data |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
    lines += [table_row(e, current, stills) for e in page['entries']]
    lines += ['', '[Source descriptions, confidence and credits](../description-sources.md) · [Complete JSON](../catalogue.json) · [CSV](../catalogue.csv)', '']
    return '\n'.join(lines).encode()

def build(catalogue, csv_raw, readme_raw, expected_count):
    before = json_bytes(catalogue)
    entries, groups = validate(catalogue, csv_raw, expected_count)
    buckets = {}
    for e in entries:
        directory, slug = family(e)
        buckets.setdefault((e['group'], directory, slug), []).append(e)
    outputs, navigation, directory_rows, pages = {}, [], [], []
    for (group, directory, slug), selected in sorted(buckets.items()):
        key = group + ('-' + slug if slug else '')
        family_index = LIB + '/browse/' + key + '.md'
        title = groups[group] + (' / ' + directory if directory else '')
        chunks = pack(selected)
        rows = []
        for number, chunk in enumerate(chunks, 1):
            stem = LIB + '/tables/browse-' + key + '-' + str(number)
            page = {'title': title, 'entries': chunk, 'number': number, 'animated': stem + '.md', 'stills': stem + '-stills.md', 'familyIndex': family_index}
            pages.append(page)
            first, last = chunk[0]['shortIdentifier'], chunk[-1]['shortIdentifier']
            rows.append('| ' + str(number) + ' | ' + code(first) + (' to ' + code(last) if first != last else '') + ' | [Open ' + str(len(chunk)) + ' GIFs](' + link(family_index, page['animated']) + ') | [Open stills](' + link(family_index, page['stills']) + ') |')
            for e in chunk:
                navigation.append({'id': e['id'], 'group': group, 'recordedSourceDirectory': directory or None, 'shortIdentifier': e['shortIdentifier'], 'animatedTable': page['animated'], 'stillTable': page['stills'], 'detailPage': e['detailPage']})
        lines = ['# ' + title, '', '[Library](../README.md) · [All groups](README.md)', '', str(len(selected)) + ' published clips. Sorted by exact clip label, then stable ID. At most four GIFs per page, with a 16 MiB declared animated-media packing target. A single larger existing GIF is retained alone rather than skipped or changed.', '', '| Page | Exact clip range | Animated table | Still-image table |', '| --- | --- | --- | --- |'] + rows + ['', 'Grouping is derived from source-directory text, not a new semantic interpretation. Original details, tags, credits, media, source records and visual/native evidence limits are preserved.', '']
        outputs[family_index] = '\n'.join(lines).encode()
        directory_rows.append('| ' + cell(groups[group]) + ' | ' + code(directory or 'Original category') + ' | ' + str(len(selected)) + ' | ' + str(len(chunks)) + ' | [Browse](' + link(LIB + '/browse/README.md', family_index) + ') |')
    for page in pages:
        outputs[page['animated']] = render_page(page, False)
        outputs[page['stills']] = render_page(page, True)
    browse = ['# Animation library - grouped browsing', '', '[Library index](../README.md) · [Searchable ID/page map](navigation.json) · [CSV data](../catalogue.csv)', '', '**No preview images load on this directory.** Browse the original categories and recorded source directories. Family names are exact asset-directory tokens, not newly verified action or actor labels. Every published ID appears exactly once in the grouped tables. Legacy table and clip links remain available.', '', '| Category | Recorded source directory | Clips | Pages | Open |', '| --- | --- | --- | --- | --- |'] + directory_rows + ['', 'Descriptions, semantic tags and provenance remain in the original catalogue and clip details. Native timing, props/contact, arbitrary actor compatibility and continuous per-clip quality are not established by this reorganization.', '']
    outputs[LIB + '/browse/README.md'] = '\n'.join(browse).encode()
    outputs[LIB + '/browse/navigation.json'] = json_bytes({'schemaVersion': 1, 'entryCount': len(entries), 'groupingBasis': 'Original group; stock subgroup from recorded virtual GANI directory only', 'maxAnimatedPreviewsPerPage': PAGE_SIZE, 'declaredAnimatedPackingTargetBytes': MAX_PAGE_BYTES, 'entries': sorted(navigation, key=lambda x: x['id'])})
    readme = readme_raw.decode('utf-8')
    start, end = readme.find('## Browse by section\n'), readme.find('## Metadata columns\n')
    if start < 0 or end <= start:
        raise ValueError('README section contract changed')
    section = ['## Browse by section', '', '[**Open the grouped browsing directory**](browse/README.md) to choose a category and recorded source family. It contains **' + str(len(entries)) + ' published references** in **' + str(len(buckets)) + ' groups**, without loading images.', '', 'Each animated page has at most four previews, packed to a 16 MiB declared-media target when possible. Existing full GIFs are displayed small; their actual download size is shown. Still-image alternatives load no GIFs. All old per-clip and table URLs remain valid.', '', '| Original category | Published clips |', '| --- | --- |']
    counts = Counter(e['group'] for e in entries)
    section += ['| ' + cell(title) + ' | ' + str(counts[group]) + ' |' for group, title in groups.items()]
    section += ['', '[Find an exact ID / clip label / page](browse/navigation.json) · [Search the CSV](catalogue.csv)', '', '']
    readme = readme[:start] + '\n'.join(section) + readme[end:]
    readme = readme.replace('at most four small GIFs', 'at most four GIF previews')
    readme = readme.replace('Stop at the selected category boundary; do not add another category to fill a batch cap.', 'That ledger describes its historical LMG batch only. The standing goal is broader humanoid coverage; the whole-game denominator remains unknown, and milestones, empty queues or planned exclusions do not prove exhaustion.')
    marker = '## Credits and scope\n'
    addition = '## Metadata-only navigation maintenance\n\nAfter the existing reviewed builder, run `python research/animation-library/organize-library.py --root . --output <new-empty-directory> --config research/animation-library/organization-config.json`. This generates a reviewable navigation overlay; it reads catalogue/CSV/README only and never opens or rewrites media. The cloud workflow produces an artifact for review, without pushing repository changes. Catalogue and CSV input pins are intentionally fixed; a new publication baseline requires a reviewed configuration update.\n\n'
    if marker not in readme:
        raise ValueError('README credits boundary changed')
    readme = readme.replace(marker, addition + marker)
    outputs[README] = readme.encode()
    if before != json_bytes(catalogue) or len(navigation) != len(entries) or {n['id'] for n in navigation} != {e['id'] for e in entries}:
        raise ValueError('Source mutation or incomplete navigation')
    for path, raw in outputs.items():
        if path != README and not path.startswith((LIB + '/browse/', LIB + '/tables/browse-')):
            raise ValueError('Output outside authored navigation allowlist')
        if len(raw) > MAX_TEXT:
            raise ValueError('Oversized generated navigation')
        if path.endswith('-stills.md') and re.search(r'<img[^>]+src="[^"]+\.gif"', raw.decode(), re.I):
            raise ValueError('GIF loaded in still mode')
    return outputs, {'publishedEntries': len(entries), 'groupedFamilies': len(buckets), 'animatedPages': len(pages), 'maxPreviewsPerPage': max(len(p['entries']) for p in pages), 'maxDeclaredAnimatedPageBytes': max(sum(e['media']['animatedThumbnail']['bytes'] for e in p['entries']) for p in pages), 'catalogueDataChanged': False, 'csvDataChanged': False, 'legacyTablesChanged': False, 'clipDetailsChanged': False, 'mediaReadOrChanged': False, 'nativeProofAdded': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    if args.output.exists():
        raise SystemExit('Output must be a new, absent directory')
    config = json.loads(args.config.read_text(encoding='utf-8'))
    inputs = {name: read(root, name) for name in (CATALOGUE, CSV, README)}
    for name, raw in inputs.items():
        if git_blob(raw) != config['inputGitBlobs'][name]:
            raise SystemExit('Pinned public input changed: ' + name)
    outputs, report = build(json.loads(inputs[CATALOGUE]), inputs[CSV], inputs[README], config['expectedEntryCount'])
    report['inputBlobs'] = {name: {'gitBlob': git_blob(raw), 'sha256': sha(raw), 'bytes': len(raw)} for name, raw in inputs.items()}
    report['outputs'] = [{'path': name, 'sha256': sha(raw), 'bytes': len(raw)} for name, raw in sorted(outputs.items())]
    report['outputFiles'] = len(outputs)
    report['generatedBytes'] = sum(map(len, outputs.values()))
    args.output.mkdir(parents=True, exist_ok=False)
    for name, raw in outputs.items():
        destination = args.output / safe_path(name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
    (args.output / 'ORGANIZATION-REPORT.json').write_bytes(json_bytes(report))
    print(json.dumps({k: v for k, v in report.items() if k not in ('outputs', 'inputBlobs')}, sort_keys=True))

if __name__ == '__main__':
    main()
