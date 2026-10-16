"""Generate bounded Markdown/CSV views from reference metadata; no asset reads."""
import argparse,csv,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def textrow(value):
 return str(value).replace('|','\\|').replace('\n',' ')

def generated(catalogue):
 records=catalogue['assets'];outputs={};table=['# Seating references - page1','',
  'Three selected examples. This is not complete category coverage. Static thumbnails only; open an asset for a larger still and its360-degree reference turntable.',
  '', '[Library index](../README.md) | [Plan](../RESEARCH-PLAN.md) | [JSON data](../catalogue.json) | [CSV data](../catalogue.csv)',
  '', '| Preview | Asset | Category | Tags | Description | Model location | Container location |',
  '|---|---|---|---|---|---|---|']
 for a in records:
  identifier=a['id'];thumb='../../../'+a['preview']['thumbnail'];page='../assets/'+identifier+'.md'
  table.append('| [!['+a['title']+']('+thumb+')]('+page+') | ['+a['title']+']('+page+') | '+a['category']+' > '+a['subcategory']+' | '+', '.join(a['tags'])+' | '+textrow(a['description'])+' | `'+a['source']['nativePath']+'` | `'+a['source']['container']['nativePath']+'` (retained bytes verified) |')
  p=a['preview'];s=a['source'];mat=a['materials'];detail=['# '+a['title'],'',a['description'],'',
   '[Seating table](../tables/seating-1.md) | [Library](../README.md) | [Credits and evidence rules](../sources-and-credits.md)',
   '', '## Still reference','', '!['+a['title']+' - clean textured still](../../../'+p['still']+')',
   '', '## 360-degree reference','', '!['+a['title']+' - full camera orbit](../../../'+p['turntable']+')',
   '', 'The camera circles a static model. This is not a native game animation. Actual retained base-color texture/UVs are shown with approximate studio materials and lighting; this is not proof of FOX shader or gameplay equivalence.',
   '', '## Identity and location','',
   '| Field | Value |','|---|---|',
   '| Category | '+a['category']+' > '+a['subcategory']+' |',
   '| Tags | '+', '.join(a['tags'])+' |',
   '| Source namespace | '+a['sourceNamespace']+'; this does not establish exclusive original use |',
   '| Observed retained use | '+a['observedUse']+' |',
   '| Native model | `'+s['nativePath']+'` |',
   '| Native SHA256 | `'+s['nativeSha256']+'` |',
   '| FPK | `'+s['container']['nativePath']+'` |',
   '| Retained FPK SHA256 | `'+s['container']['sha256']+'` |',
   '| Historical DAT origin | `'+s['historicalDatOrigin']+'`; current installed DAT unverified |',
   '| Location evidence | Retained indexed member identity plus unique byte-exact FMDL payload and indexed path string in retained FPK; no fresh extraction/current DAT check |',
   '| Selected geometry | LOD0; '+str(a['geometry']['triangles'])+' triangles; native geometry/UV inputs unchanged |',
   '| Native bounds | `'+json.dumps(a['geometry']['nativeBounds'])+'` (native coordinate units) |',
   '| Preview | Blender5.2.2;768px still;480px GIF;48angles/7.5degrees;100ms each;4.8seconds;160px static thumbnail |',
   '', '## Texture bindings','', 'Bindings below are source metadata. Only the actual base-color texture drives this approximate preview. Native texture virtual paths are unknown where stored by hash; the DDS hashes identify retained converted content, not fabricated game filenames.',
   '', '| Sampler | Native path hash | Native virtual path | Retained DDS SHA256 | Dimensions |', '|---|---|---|---|---|']
  for t in mat:
   detail.append('| '+t['sampler']+' | `'+t['nativePathHash']+'` | '+('`'+t['nativeVirtualPath']+'`' if t['nativeVirtualPath'] else 'Unknown; hash identity retained')+' | `'+t['ddsSha256']+'` | '+str(t['dimensions'][0])+'x'+str(t['dimensions'][1])+' |')
  detail += ['', '## Attribution and limits','',
   'Game model and textures: Konami. Reference preparation is AI/LLM-authored using the established community tool pipeline; see [central credits](../sources-and-credits.md). The repository owner is arsenal-pt. Game artwork is not covered by the original-code license.',
   '', 'Friendly labels and tags come from native folder identity, recorded scene use and reviewed preview appearance. Runtime interaction, folding/rolling/wheel movement, collisions, progression and native material response were not tested. A use tag is a search aid, not a promised mechanic.',
   '', 'No source FMDL, texture, archive, decoded geometry or blend is provided. The [catalogue](../catalogue.json) includes this entry and media hashes; clean frames and original sources remain private.', '']
  outputs['assets/'+identifier+'.md']='\n'.join(detail)
 outputs['tables/seating-1.md']='\n'.join(table)+'\n'
 columns=['id','title','category','subcategory','tags','description','sourceNamespace','observedUse','nativePath','nativeSha256','containerPath','containerSha256','historicalDatOrigin','locationStatus','currentDatVerified','lod','triangles','still','turntable','thumbnail','nativeRenderingEquivalent']
 sio=io.StringIO(newline='');writer=csv.DictWriter(sio,fieldnames=columns,lineterminator='\n');writer.writeheader()
 for a in records:
  s=a['source'];writer.writerow({'id':a['id'],'title':a['title'],'category':a['category'],'subcategory':a['subcategory'],'tags':';'.join(a['tags']),'description':a['description'],'sourceNamespace':a['sourceNamespace'],'observedUse':a['observedUse'],'nativePath':s['nativePath'],'nativeSha256':s['nativeSha256'],'containerPath':s['container']['nativePath'],'containerSha256':s['container']['sha256'],'historicalDatOrigin':s['historicalDatOrigin'],'locationStatus':s['locationStatus'],'currentDatVerified':False,'lod':0,'triangles':a['geometry']['triangles'],'still':a['preview']['still'],'turntable':a['preview']['turntable'],'thumbnail':a['preview']['thumbnail'],'nativeRenderingEquivalent':False})
 outputs['catalogue.csv']=sio.getvalue();return outputs

def run():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 o=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'))
 if len(o['assets'])!=3 or len({a['id'] for a in o['assets']})!=3:raise ValueError('This starter is exactly three unique entries')
 for a in o['assets']:
  if a['preview']['gifFrames']!=48 or a['preview']['frameDelayMs']!=100:raise ValueError('Visual budget differs')
 for rel,s in generated(o).items():
  p=ROOT/rel
  if args.check:
   if not p.exists() or p.read_text(encoding='utf-8')!=s:raise ValueError('Stale output '+rel)
  else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
 print('PASS: three records; one static-only category table; three detail pages; portable CSV;'+(' outputs current' if args.check else ' outputs generated'))
if __name__=='__main__':run()
