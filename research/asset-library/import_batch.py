"""Merge reviewed portable pipeline exports; never reads native game payloads."""
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
PAGE_SIZE = 12
LABELS = {
 'mtbs_lddr001_vrtn002': ('Ladder section', 'Architecture', 'Access components', ['ladder', 'access', 'metal', 'mother-base'], 'A vertical metal ladder section. This reference is one native model variant; placement, climbing and complete assembly are untested.'),
 'gntn_swtc001_vrtn001': ('Emergency-stop / control switch panel', 'Equipment', 'Controls and fixtures', ['switch', 'control-panel', 'emergency-stop', 'guantanamo-namespace'], 'A small control panel with a red emergency-stop style switch. The model namespace is guantanamo; its retained occurrence is on Mother Base. No working interaction is claimed.'),
 'mtbs_door006_door004': ('Door panel', 'Architecture', 'Access components', ['door', 'panel', 'mother-base', 'metal'], 'An individual industrial door panel with its surface fittings. This is the panel model, not a complete installed doorway or proven working door.'),
 'mtbs_gate001_vrtn001': ('Gate / shutter panel', 'Architecture', 'Access components', ['gate', 'shutter', 'panel', 'mother-base'], 'A large ribbed gate or shutter panel. The reference shows a native component; surrounding structure and opening behavior are not established.'),
 'mtbs_duct002_vrtn001': ('Duct section', 'Architecture', 'Utility components', ['duct', 'ventilation', 'metal', 'mother-base'], 'A metal duct section with bent connector geometry. This is a static native variant, not an assembled or functional ventilation system.'),
 'mtbs_shlf007_vrtn002': ('Shelf component / variant 002', 'Furniture', 'Storage components', ['shelf', 'storage', 'component', 'mother-base'], 'A native metal shelf component or variant. The full assembled storage unit and interaction are not established.'),
 'mtbs_shlf007_vrtn001': ('Shelf upright / frame component', 'Furniture', 'Storage components', ['shelf', 'upright', 'frame', 'storage', 'mother-base'], 'An individual shelf upright or frame component, rather than a complete assembled shelf.'),
}

def sha(data):
 return hashlib.sha256(data).hexdigest()

def plain(value, fallback='', limit=1200):
 text=str(value) if value is not None else fallback
 text=re.sub(r'[\x00-\x1f\x7f\[\]<>|`*\\]', ' ', text)
 return ' '.join(text.split())[:limit] or fallback

def private_path(value):
 # Shared metadata/path guard: native /Assets virtual names are allowed.
 if re.search(r'[A-Za-z]:[\\/]|file://',value):return True
 if value.startswith(('\\\\','//')):return True
 if value.casefold().startswith('/assets/') and not re.search(r'\s',value):return False
 return bool(re.search(r'(?<![A-Za-z0-9_:])/(?:home|Users|mnt|media|Volumes|tmp|var|run|private|proc|dev|etc|opt|usr|root)(?:/|$)',value,re.I))

def safe_path(base, relative):
 p=Path(relative)
 if private_path(relative) or p.is_absolute() or '..' in p.parts:
  raise ValueError('Unsafe export path: '+relative)
 result=(base/p).resolve()
 if not result.is_relative_to(base.resolve()):raise ValueError('Escaped export path')
 return result

def portable(value):
 if isinstance(value,dict):
  for k,v in value.items():portable(k);portable(v)
 elif isinstance(value,list):
  for v in value:portable(v)
 elif isinstance(value,str):
  if private_path(value) or re.search(r'github_pat_|gh[pousr]_[A-Za-z0-9]{25,}',value):
   raise ValueError('Private path or credential in export metadata')

def validate_media(path, field):
 expected=(480,480) if field=='turntable' else ((160,160) if field=='thumbnail' else (768,768))
 with Image.open(path) as im:
  if im.size!=expected or im.format!=('GIF' if field=='turntable' else 'PNG'):
   raise ValueError('Preview format/dimensions differ from contract: '+field)
  if field=='turntable':
   if im.n_frames!=48 or im.info.get('loop')!=0:raise ValueError('GIF frame/loop contract differs')
   for n in range(im.n_frames):
    im.seek(n)
    if im.info.get('duration')!=100:raise ValueError('GIF frame duration differs')
  else:im.verify()

def prepare(export, selected, media_prefix):
 export=Path(export); catalogue=json.loads((export/'catalogue.json').read_text(encoding='utf-8'))
 portable(catalogue)
 manifest=json.loads((export/'manifest.json').read_text(encoding='utf-8'))
 files={x['path']:x for x in manifest['files']}
 cat_bytes=(export/'catalogue.json').read_bytes()
 if files['catalogue.json']['sha256']!=sha(cat_bytes):raise ValueError('Catalogue hash mismatch')
 source={a['id']:a for a in catalogue['assets']}
 if len(source)!=len(catalogue['assets']):raise ValueError('Duplicate source IDs')
 records=[];copies=[]
 for identifier in selected:
  if not re.fullmatch(r'[A-Za-z0-9_-]+',identifier):raise ValueError('Unsafe portable asset ID')
  a=source[identifier];stem=a['modelPath'].rsplit('/',1)[-1].removesuffix('.fmdl')
  if stem in LABELS:title,category,subcategory,tags,description=LABELS[stem]
  else:
   title=plain(a.get('title'),plain(stem,'Unnamed model'),180)
   category=plain(a.get('category'),'Unclassified',80)
   subcategory=plain(a.get('subcategory'),'Selected model components',100)
   tags=[plain(x,limit=80) for x in a.get('tags',[]) if isinstance(x,str) and plain(x,limit=80)]
   description=plain(a.get('description'),'Selected native model reference. Assembly and interaction are not established.')
  evidence=a.get('sourceEvidence') or {}
  member_evidence=evidence.get('memberEvidence') or 'Portable job-export source identity; container membership was not independently verified by this importer.'
  namespace=a['modelPath'].split('/object/',1)[1].split('/',1)[0] if '/object/' in a['modelPath'] else 'Unknown (no object namespace in recorded native path)'
  paths={};media=[]
  for field,key in [('still','still'),('turntable','gif'),('thumbnail','thumbnail')]:
   rel=a[key];f=files[rel];src=safe_path(export,rel);data=src.read_bytes()
   if sha(data)!=f['sha256'] or len(data)!=f['bytes']:raise ValueError('Media hash mismatch: '+rel)
   suffix=src.suffix.lower()
   if suffix not in ('.png','.gif'):raise ValueError('Only preview PNG/GIF permitted')
   validate_media(src,field)
   dst=media_prefix+'/'+src.name;paths[field]=dst;copies.append((src,dst,f['sha256']))
   media.append({'path':dst,'sha256':f['sha256'],'bytes':f['bytes']})
  base=a['baseTextures'];selected_lod=next(x for x in a['nativeLods'] if x['nativeLod']==a['lod'])
  rec={'id':identifier,'title':title,'category':category,'subcategory':subcategory,'tags':tags,'description':description,
   'descriptionProvenance':'Authored summary from exact source identity and root-reviewed existing reference still; no interaction or complete assembly claim' if stem in LABELS else 'Sanitized pipeline-export description/labels; importer does not independently establish visual fidelity, assembly or interaction',
   'batchImport':{'schemaVersion':1,'provenance':'batch-provenance.json','exportCatalogueSha256':sha(cat_bytes),'upstreamPreparation':a['upstreamPreparation']},
   'sourceNamespace':namespace,
   'observedUse':'Retained Mother Base source/container occurrence; not exclusive original usage' if evidence.get('exactMemberRecord') and '/mtbs/' in a['containerPath'] else 'Selected source export; original placement and exclusive usage not established',
   'source':{'nativePath':a['modelPath'],'nativeSha256':a['modelSha256'],'stableIdentity':a['modelPath'].lower()+'#'+a['modelSha256'],
    'container':{'nativePath':a['containerPath'],'sha256':a['containerSha256'],'status':'Retained member/source metadata joined and selected source bytes checked during pipeline job; container not freshly unpacked' if evidence.get('exactMemberRecord') else 'Container identity supplied by portable export; membership not independently verified by importer'},
    'historicalDatOrigin':None,'locationStatus':member_evidence,'currentInstalledDatVerified':False,'evidence':evidence},
   'geometry':{'lod':a['lod'],'triangles':a['triangles'],'originalGeometryAndUvsUnchanged':True},
   'materials':[{'sampler':plain(t.get('samplerName') or t.get('sampler'),'Unknown sampler name (base binding)',100),'materialIndex':t['materialIndex'],'nativePathHash':t['nativePathHash'],'nativeVirtualPath':None,'ddsSha256':t['sha256'],'dimensions':[t['width'],t['height']],'mipCount':t['mipCount'],'nativeMipCountVerified':t['nativeMipCountVerified'],'connectedInPreview':True} for t in base],
   'preview':{**paths,'stillDimensions':[768,768],'gifDimensions':[480,480],'thumbnailDimensions':[160,160],'gifFrames':48,'frameDelayMs':100,'durationMs':4800,'loop':0,'nativeAnimation':False,'nativeShaderEquivalent':False,'textureRendering':'Actual retained base textures and UVs; approximate studio shading; other native shader channels not recreated','media':media},
   'quality':{'decodedIndicesHashDerivation':'SHA256 of UTF-8 canonical JSON for decoded triangle-index lists grouped by mesh: json.dumps(level_faces, sort_keys=True, separators=(comma, colon), ensure_ascii=False). This is not a hash of the original packed index-buffer bytes.','highestRetainedGeometricLod':min(x['nativeLod'] for x in a['nativeLods'] if x['triangles']==max(v['triangles'] for v in a['nativeLods'])),'distinctNativeLods':len({x['indicesSha256'] for x in a['nativeLods']}),'baseTextureDimensions':[base[0]['width'],base[0]['height']],'baseTextureNativeMipCount':base[0]['mipCount'] if base[0]['nativeMipCountVerified'] else None,'largerRetainedBaseTextureFound':None,'nativeLods':a['nativeLods'],'renderedNativeLods':[a['lod']],'baseTextureSummary':a['baseTextureSummary'],'highestDetailScope':'Triangle-count comparison within this selected retained FMDL only; no all-game maximum proof'},
   'credits':{'gameModelAndTextures':'Konami','referenceOwner':'arsenal-pt','referenceImplementation':'OpenAI Codex, AI/LLM-authored','toolSources':'sources-and-credits.md'}}
  portable(rec);records.append(rec)
 return records,copies

def merge(existing, records):
 result=json.loads(json.dumps(existing));by_id={a['id']:a for a in result['assets']};by_sha={a['source']['nativeSha256']:a['id'] for a in result['assets']}
 for a in records:
  if a['id'] in by_id:
   if by_id[a['id']]!=a:raise ValueError('Refusing to overwrite differing accepted entry '+a['id'])
   continue
  if a['source']['nativeSha256'] in by_sha:raise ValueError('Source already catalogued as '+by_sha[a['source']['nativeSha256']])
  result['assets'].append(a);by_id[a['id']]=a;by_sha[a['source']['nativeSha256']]=a['id']
 return result

def cell(value):return str(value).replace('|',r'\|').replace('\n',' ')
def table_slug(category):
 slug=re.sub(r'[^a-z0-9]+','-',category.casefold()).strip('-') or 'unclassified'
 canonical={'Architecture','Furniture','Equipment','Logistics','Vehicles','Characters','Environment and markings'}
 if category not in canonical:slug+='-'+sha(category.encode('utf-8'))[:8]
 return slug+'-batch'

def generated(records):
 outputs={};groups={}
 for a in records:groups.setdefault(a['category'],[]).append(a)
 for category,assets in groups.items():
  for start in range(0,len(assets),PAGE_SIZE):
   page=start//PAGE_SIZE+1;table=['# '+category+' references - imported batch page '+str(page),'','Static thumbnails only (at most12/page). Open one entry for its full still/360GIF. Native LOD inventory is separate from rendered coverage.','',
    '[Library](../README.md) | [Credits](../sources-and-credits.md) | [Batch provenance](../batch-provenance.json)','',
    '| Preview | Asset | Category | Tags | Description | Quality / LOD | Base texture | Model location | Container location |','|---|---|---|---|---|---|---|---|---|']
   for a in assets[start:start+PAGE_SIZE]:
    page_link='../assets/'+a['id']+'.md';q=a['quality'];s=a['source'];p=a['preview']
    table.append('| [!['+a['title']+'](../../../'+p['thumbnail']+')]('+page_link+') | ['+a['title']+']('+page_link+') | '+a['category']+' > '+a['subcategory']+' | '+', '.join(a['tags'])+' | '+cell(a['description'])+' | LOD'+str(a['geometry']['lod'])+'; '+str(a['geometry']['triangles'])+' triangles; '+str(len(q['nativeLods']))+' native levels inventoried; only selectedLOD rendered | '+cell(q['baseTextureSummary'])+' | `'+s['nativePath']+'` | `'+s['container']['nativePath']+'` (retained occurrence) |')
   table+=['','Pages: '+' | '.join('['+str(n)+']('+table_slug(category)+'-'+str(n)+'.md)' for n in range(1,(len(assets)+PAGE_SIZE-1)//PAGE_SIZE+1)),''];outputs['tables/'+table_slug(category)+'-'+str(page)+'.md']='\n'.join(table)
 for a in records:
  q=a['quality'];s=a['source'];p=a['preview'];detail=['# '+a['title'],'',a['description'],'',
   '['+a['category']+' table](../tables/'+table_slug(a['category'])+'-1.md) | [Library](../README.md) | [Credits](../sources-and-credits.md) | [Batch source data](../batch-provenance.json)','',
   '## Still reference','','!['+a['title']+'](../../../'+p['still']+')','',
   '## 360-degree reference','','!['+a['title']+' camera orbit](../../../'+p['turntable']+')','',
   'Static model;48camera views,100ms/frame,4.8-second loop. This is a reference-camera orbit, not native animation. Actual retained base textures/UVs use approximate studio lighting. FOX shader, collision, interactions and complete assembly are untested.','',
   '## Identity and source','','| Field | Value |','|---|---|',
   '| Category | '+a['category']+' > '+a['subcategory']+' |','| Tags | '+', '.join(a['tags'])+' |','| Native model | `'+s['nativePath']+'` |','| Native SHA256 | `'+s['nativeSha256']+'` |',
   '| Retained container | `'+s['container']['nativePath']+'` |','| Retained container SHA256 | `'+s['container']['sha256']+'` |','| Location evidence | '+s['locationStatus']+' |',
   '| Current installed DAT / priority | Not verified; outer DAT unknown for this record |','| Upstream preparation | '+a['batchImport']['upstreamPreparation']+' |','',
   'Source namespace is a path identity, not exclusive original use. Lowercased lookup keys are separate from the exact retained member spelling.','',
   '## Quality and native LOD inventory','','Texture pixels/mips, geometric detail and approximate studio shader fidelity are separate. OnlyLOD0was rendered for this imported batch. Other levels are inventoried, not newly previewed; identical decoded index sets map to their recorded counterpart. The decoded-indices hash uses UTF-8 canonical JSON of triangle-index lists grouped by mesh, not the original packed index-buffer bytes. No upscaling or invented geometry.','',
   '| Native LOD | Triangles | Decoded indices SHA256 | Duplicate mapping | Preview status |','|---|---:|---|---|---|']
  for v in q['nativeLods']:
   status='Rendered above' if v['nativeLod'] in q['renderedNativeLods'] else ('Same index set as LOD'+str(v['duplicateOf'])+'; no separate preview' if 'duplicateOf' in v else 'Not rendered')
   detail.append('| '+str(v['nativeLod'])+' | '+str(v['triangles'])+' | `'+v['indicesSha256']+'` | '+('LOD'+str(v['duplicateOf']) if 'duplicateOf' in v else 'Distinct within retained model')+' | '+status+' |')
  detail+=['','## Base textures','','| Material | Native sampler / path hash | Pixels | Mip levels | Retained DDS SHA256 |','|---|---|---|---|---|']
  for t in a['materials']:
   detail.append('| '+str(t['materialIndex'])+' | '+t['sampler']+' / `'+t['nativePathHash']+'` | '+str(t['dimensions'][0])+' x '+str(t['dimensions'][1])+' | '+str(t['mipCount'])+(' native/header verified' if t['nativeMipCountVerified'] else ' DDS only; native header not rechecked')+' | `'+t['ddsSha256']+'` |')
  detail+=['','Texture virtual filenames are unknown where only native hashes are available. Larger native textures elsewhere in the game were not searched. Only actual base-color maps are applied; normal/specular/packed shader channels are not recreated.','',
   '## Attribution and limits','','Game models/textures: Konami. Project owner: arsenal-pt. Authored importer/metadata/reference work: OpenAI Codex (AI/LLM). [Community tools and detailed credits](../sources-and-credits.md). No endorsement is implied. Game artwork is outside the original-code license.','',
   'Only rendered references and descriptive metadata are distributed. Raw assets, native files, textures, decoded geometry, Blender scenes, private source paths and clean frame caches remain private. [Catalogue](../catalogue.json) and [batch provenance](../batch-provenance.json) preserve identity and media hashes.','']
  outputs['assets/'+a['id']+'.md']='\n'.join(detail).replace('OnlyLOD0was','Only LOD0 was').replace('48camera','48 camera').replace('model;48','model; 48').replace(',100ms',', 100ms')
 # New installed-source text never changes old accepted detail pages.
 installed=[a for a in records if a.get('batchImport',{}).get('sourceMode')=='installed']
 if installed:
  from installed_import import installed_detail
  for a in installed:
   key='assets/'+a['id']+'.md';outputs[key]=installed_detail(outputs[key],a)
  for category in {a['category'] for a in installed}:
   if all(a.get('batchImport',{}).get('sourceMode')=='installed' for a in groups[category]):
    for key in list(outputs):
     if key.startswith('tables/'+table_slug(category)+'-'):
      outputs[key]=outputs[key].replace('(retained occurrence)','(captured source occurrence)')
 return outputs

def run():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('export',type=Path);ap.add_argument('--ids',nargs='+',required=True);ap.add_argument('--media-prefix',required=True);args=ap.parse_args()
 if not args.media_prefix.startswith('media/asset-previews/'):raise ValueError('Use the dedicated asset-preview media prefix')
 safe_path(ROOT.parents[1],args.media_prefix)
 records,copies=prepare(args.export,args.ids,args.media_prefix);catalogue_path=ROOT/'catalogue.json';existing=json.loads(catalogue_path.read_text(encoding='utf-8'));merged=merge(existing,records)
 for src,rel,digest in copies:
  dest=ROOT.parents[1]/rel
  if dest.exists() and sha(dest.read_bytes())!=digest:raise ValueError('Refusing to overwrite media '+rel)
 for src,rel,digest in copies:
  dest=ROOT.parents[1]/rel;dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():shutil.copyfile(src,dest)
 catalogue_path.write_text(json.dumps(merged,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
 provenance_path=ROOT/'batch-provenance.json'
 provenance=json.loads(provenance_path.read_text(encoding='utf-8')) if provenance_path.exists() else {}
 previous={a['id']:a for a in provenance.get('records',[])}
 provenance.update(schemaVersion=1,source='Portable local pipeline export; reviewed existing media; no source extraction or rendering by importer',catalogueSha256=sha((args.export/'catalogue.json').read_bytes()),records=[{**previous.get(a['id'],{}),**a} for a in merged['assets'] if 'batchImport' in a])
 (ROOT/'batch-provenance.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');print('Merged '+str(len(records))+' reviewed records; total '+str(len(merged['assets']))+' unique parents')

if __name__=='__main__':run()
