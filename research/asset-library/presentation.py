"""Pure asset-reference display views. Never edits records, media or processing identity."""
import copy, csv, hashlib, html, io, json, re
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent
PAGE_SIZE = 12

def load_registry(path=None):
    data = json.loads(Path(path or ROOT/'naming-registry.json').read_text(encoding='utf-8-sig'))
    if data.get('schemaVersion') != 1: raise ValueError('Unsupported naming registry')
    return data

def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', str(value).casefold()).strip('-') or 'unclassified'

def cell(value):
    return html.escape(str(value), quote=False).replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ').replace('[', '&#91;').replace(']', '&#93;').replace('`', '&#96;')

def href(value):
    value = str(value)
    if any(ord(c)<32 for c in value) or '\\' in value: raise ValueError('Unsafe display link')
    parsed = urlsplit(value)
    if parsed.scheme and parsed.scheme != 'https': raise ValueError('Unsupported display link scheme')
    if value.startswith('//'): raise ValueError('Network-path display link refused')
    return quote(value, safe='/:#?=&%+,_~.-')

def link(label, target):
    return '['+cell(label)+']('+href(target)+')'

def _native(record):
    source = record.get('source') or {}
    return source.get('nativePath') or record.get('modelPath') or ''

def _label(record, registry, native):
    exact = registry.get('overrides', {}).get(record['id'])
    if exact: return exact
    exact = registry.get('path_overrides', {}).get(native)
    if exact: return exact
    matches = []
    for order, rule in enumerate(registry.get('rules', [])):
        prefix = rule.get('native_path_prefix')
        component = rule.get('path_component')
        if prefix and native.startswith(prefix): matches.append((len(prefix),-order,rule))
        elif component and component in PurePosixPath(native).parts: matches.append((len(component),-order,rule))
    return max(matches,key=lambda x:x[:2])[2] if matches else {}

def present(record, registry):
    """Return a separate JSON-compatible view; accepted input records stay immutable."""
    identifier = record['id']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', identifier): raise ValueError('Unsafe Library ID')
    native = _native(record)
    filename = PurePosixPath(native).name if native else 'Unknown'
    stem = PurePosixPath(native).stem if native else identifier
    label = _label(record, registry, native)
    status = label.get('naming_status', 'unidentified')
    if status not in ('reviewed','path-derived','unidentified'): raise ValueError('Unknown naming status')
    category = label.get('category', 'Unclassified')
    geometry = record.get('geometry') or {}
    quality = copy.deepcopy(record.get('quality') or {})
    lod = geometry.get('lod',record.get('lod',0))
    source = copy.deepcopy(record.get('source') or {'nativePath':native,'nativeSha256':record.get('modelSha256'),
        'container':{'nativePath':record.get('containerPath'),'sha256':record.get('containerSha256')},
        'evidence':record.get('sourceEvidence')})
    if not quality: quality = {'nativeLods':copy.deepcopy(record.get('nativeLods',[])), 'baseTextureSummary':record.get('baseTextureSummary')}
    tokens = re.findall(r'(?:^|_)(vrtn_?\d+)(?=_|$)', stem, flags=re.I)
    raw_hash = hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    return {'id':identifier,'library_id':identifier,'display_name':label.get('display_name') or 'Unidentified model ('+stem+')',
        'native_filename':filename,'native_path':native,'variant':label.get('variant') or (', '.join(tokens) if tokens else 'No explicit variant token'),
        'lod':lod,'triangles':geometry.get('triangles',record.get('triangles')),
        'category':category,'subcategory':label.get('subcategory','Unclassified components'),'category_slug':slug(category),
        'tags':list(label.get('tags',[])),'description':label.get('description') or 'Native model reference; a readable object identification has not been reviewed.',
        'naming_status':status,'confidence':label.get('confidence','unknown'),'evidence':copy.deepcopy(label.get('evidence',{})),
        'metadata_review':status!='reviewed','source':source,'quality':quality,
        'materials':copy.deepcopy(record.get('materials',record.get('baseTextures',[]))),
        'raw_record_sha256':raw_hash}

def _nav(context):
    items=[]
    for label,key in [('Library','library_href'),('Category','category_href'),('Source / advanced data','raw_href'),('Credits','credits_href')]:
        if context.get(key): items.append(link(label,context[key]))
    return ' | '.join(items)

def render_table(views, context):
    if len(views)>PAGE_SIZE: raise ValueError('Category page exceeds twelve static thumbnails')
    lines=['# '+cell(context.get('title','Asset references')),'',_nav(context),'',
        'Static thumbnails only. Open a name or preview for its full still and 360-degree camera reference.','',
        '| Preview | Name | Game filename | Description | Tags | Variant / LOD |',
        '|---|---|---|---|---|---|']
    for v in views:
        paths=context['links'][v['id']]
        image='[!['+cell(v['display_name'])+']('+href(paths['thumbnail'])+')]('+href(paths['detail'])+')'
        name=link(v['display_name'],paths['detail'])
        if v['metadata_review']: name+=' ('+cell(v['naming_status'])+')'
        quality='Variant: '+v['variant']+'; LOD'+str(v['lod'])
        if v['triangles'] is not None: quality+='; '+str(v['triangles'])+' triangles'
        lines.append('| '+' | '.join([image,name,cell(v['native_filename']),cell(v['description']),cell(', '.join(v['tags'])),cell(quality)])+' |')
    return '\n'.join(lines)+'\n'

def render_detail(view, context):
    v=view;paths=context['links'][v['id']]
    lines=['# '+cell(v['display_name']),'',cell(v['description']),'',_nav(context),'',
        '**Game filename:** '+cell(v['native_filename'])+'  ',
        '**Category:** '+cell(v['category']+' > '+v['subcategory'])+'  ',
        '**Variant:** '+cell(v['variant'])+'; **LOD:** '+str(v['lod'])+'  ',
        '**Tags:** '+cell(', '.join(v['tags'])),'',
        '## Still reference','','!['+cell(v['display_name'])+']('+href(paths['still'])+')','',
        '## 360-degree reference','','!['+cell(v['display_name'])+' camera orbit]('+href(paths['turntable'])+')','',
        'The camera circles a static model. This is not a native animation. Source base textures and UVs use approximate studio shading; interaction, collision, complete assembly and FOX shader equivalence are not established.','',
        '## Identity and naming','','| Field | Value |','|---|---|',
        '| Library ID | '+cell(v['id'])+' |','| Naming status | '+cell(v['naming_status'])+' |',
        '| Naming confidence | '+cell(v['confidence'])+' |','| Naming evidence | '+cell(json.dumps(v['evidence'],ensure_ascii=False,sort_keys=True))+' |',
        '| Native model | '+cell(v['native_path'] or 'Unknown')+' |',
        '| Model SHA256 | '+cell(v['source'].get('nativeSha256') or 'Unknown')+' |',
        '| Container | '+cell((v['source'].get('container') or {}).get('nativePath') or 'Unknown')+' |',
        '| Container SHA256 | '+cell((v['source'].get('container') or {}).get('sha256') or 'Unknown')+' |',
        '| Captured source / location scope | '+cell(v['source'].get('locationStatus') or 'See original source data; no inferred runtime priority')+' |',
        '| Raw record SHA256 | '+v['raw_record_sha256']+' |','',
        'Naming review is descriptive metadata only. It does not change model completion or identify a working game interaction.','',
        '## Native LOD inventory','','| Native LOD | Triangles | Preview status | Decoded indices SHA256 |','|---|---:|---|---|']
    q=v['quality'];levels=q.get('nativeLods') or q.get('variants') or []
    for level in levels:
        index=level.get('nativeLod');rendered=q.get('renderedNativeLods')
        state=level.get('previewStatus') or ('rendered' if level.get('preview') or index==v['lod'] or (rendered and index in rendered) else 'not separately rendered')
        lines.append('| '+str(index)+' | '+str(level.get('triangles','Unknown'))+' | '+cell(state)+' | '+cell(level.get('indicesSha256',level.get('nativeIndicesSha256','Unknown')))+' |')
    lines+=['','Mesh detail and texture pixels/mips are separate. Index hashes describe decoded triangle arrays, not packed index-buffer bytes. Only source-recorded native levels are listed.','',
        '<details>','<summary>Texture, source and naming technical metadata</summary>','','```json',
        json.dumps({'source':v['source'],'materials':v['materials'],'quality':q},ensure_ascii=False,indent=2).replace('</','<\\/'),'```','','</details>','']
    if paths.get('technical'):lines += [link('Original source / advanced record',paths['technical']),'']
    return '\n'.join(lines)

def render_index(views, category_links, context):
    lines=['# '+cell(context.get('title','Asset reference library')),'',_nav(context),'',
        str(len(views))+' reference entries. This index loads no images. Category pages show at most twelve static thumbnails; open one reference for its full still and 360-degree view.','',
        '| Category | References | Browse |','|---|---:|---|']
    for item in category_links:lines.append('| '+cell(item.get('title',item['category']))+' | '+str(item['count'])+' | '+link('Browse',item['href'])+' |')
    return '\n'.join(lines)+'\n'

def display_exports(views):
    columns=['id','display_name','native_filename','category','subcategory','tags','description','variant','lod','triangles','naming_status','confidence','raw_record_sha256']
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=columns,lineterminator='\n');writer.writeheader()
    for v in views:writer.writerow({k:';'.join(v[k]) if k=='tags' else v[k] for k in columns})
    return {'display-catalogue.json':json.dumps({'schemaVersion':1,'description':'Presentation overlay only; catalogue.json retains immutable original records','assets':[{k:v[k] for k in columns+['native_path','evidence','metadata_review']} for v in views]},indent=2,ensure_ascii=False)+'\n','display-catalogue.csv':out.getvalue()}
