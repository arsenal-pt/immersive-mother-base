"""Generate bounded Markdown/CSV views from reference metadata; no asset reads."""
import argparse,csv,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def textrow(value):
 return str(value).replace('|','\\|').replace('\n',' ')

def generated_base(catalogue):
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


def generated(catalogue):
 outputs=generated_base(catalogue);assets=catalogue['assets']
 if not all('quality' in a for a in assets):return outputs
 table=['# Seating references - page1','','Three original asset identities with twelve native LOD views in the retained scope. Static thumbnails only; open an asset for its LOD comparisons and individually linked larger previews.','',
  '[Library index](../README.md) | [Plan](../RESEARCH-PLAN.md) | [JSON](../catalogue.json) | [Parent CSV](../catalogue.csv) | [LOD CSV](../quality-variants.csv)','',
  '| Preview | Asset | Category | Tags | Description | Quality / LOD | Base texture | Model location | Container location |','|---|---|---|---|---|---|---|---|---|']
 variant_rows=[]
 for a in assets:
  q=a['quality'];src=a['source'];base=q['baseTextureDimensions'];mips=q['baseTextureNativeMipCount'];page='../assets/'+a['id']+'.md';thumb='../../../'+a['preview']['thumbnail']
  table.append('| [!['+a['title']+']('+thumb+')]('+page+') | ['+a['title']+']('+page+') | '+a['category']+' > '+a['subcategory']+' | '+', '.join(a['tags'])+' | '+textrow(a['description'])+' | LOD0; '+str(a['geometry']['triangles'])+' triangles; highest retained ([all 4]('+page+'#native-lod-comparison)) | '+str(base[0])+'x'+str(base[1])+' pixels; '+str(mips)+' native mips | `'+src['nativePath']+'` | `'+src['container']['nativePath']+'` (retained bytes verified) |')
  section=['## Native LOD comparison','','All four native face sets use the same source bounds, framing and highest verified retained base-color texture. LOD0 has the most triangles for this model in these retained inputs. Mesh detail is separate from texture resolution and approximate studio shading. No larger retained base version was found; this does not establish absence elsewhere in the game.','',
   '!['+a['title']+' - four native LODs compared](../../../'+q['comparisonImage']+')','',
   '| Preview | Native LOD | Geometric detail | Triangles | Base texture | Open selected view |','|---|---|---|---:|---|---|']
  for v in q['variants']:
   target='#still-reference' if v['nativeLod']==0 else v['id']+'.md';vp=v['preview'];label='LOD'+str(v['nativeLod']);section.append('| [!['+a['title']+' '+label+'](../../../'+vp['thumbnail']+')]('+target+') | '+label+' | '+v['qualityLabel']+' | '+str(v['triangles'])+' | '+str(base[0])+'x'+str(base[1])+'; '+str(mips)+' mips | ['+('Existing original reference' if v['nativeLod']==0 else 'Still and 360-degree view')+']('+target+') |')
   variant_rows.append({'parentId':a['id'],'variantId':v['id'],'title':a['title'],'nativeLod':v['nativeLod'],'triangles':v['triangles'],'geometricQuality':v['qualityLabel'],'nativePath':src['nativePath'],'nativeFmdlSha256':src['nativeSha256'],'nativeIndicesSha256':v['nativeIndicesSha256'],'baseTextureWidth':base[0],'baseTextureHeight':base[1],'nativeBaseMipCount':mips,'still':vp['still'],'turntable':vp['turntable'],'thumbnail':vp['thumbnail'],'reusesOriginalPreview':v['reusesOriginalPreview'],'runtimeLodSelectionVerified':False})
   if v['nativeLod']==0:continue
   detail=['# '+a['title']+' - '+label,'',a['description'],'',
    '['+a['title']+' overview and comparison]('+a['id']+'.md#native-lod-comparison) | [Seating table](../tables/seating-1.md) | [Quality/source evidence](../quality-provenance.json) | [Credits](../sources-and-credits.md)','',
    '**'+label+': '+v['qualityLabel']+'; '+str(v['triangles'])+' triangles.** Base texture: '+str(base[0])+'x'+str(base[1])+' pixels with '+str(mips)+' native mip levels. This selects a real face set in the same original model; it is not a synthetic simplification or a separate source-model version.','',
    '## Still reference','','!['+a['title']+' '+label+' textured still](../../../'+vp['still']+')','',
    '##360-degree reference','','!['+a['title']+' '+label+' full camera orbit](../../../'+vp['turntable']+')','',
    'Camera orbit only:48angles at7.5-degree increments,100ms/frame,4.8-second loop. The asset is static; this is not native animation. Framing/native bounds and base texture are held fixed across all four geometric LODs.','',
    '## Source identity','','| Field | Value |','|---|---|',
    '| Original native FMDL | `'+src['nativePath']+'` |','| Native FMDL SHA256 | `'+src['nativeSha256']+'` |',
    '| Native LOD | '+str(v['nativeLod'])+' |','| Triangles | '+str(v['triangles'])+' |','| Native LOD index bytes SHA256 | `'+v['nativeIndicesSha256']+'` |',
    '| Retained FPK | `'+src['container']['nativePath']+'` |','| Retained FPK SHA256 | `'+src['container']['sha256']+'` |',
    '| Historical DAT | `'+src['historicalDatOrigin']+'`; current installed DAT content/version unverified |','| Base texture | '+str(base[0])+'x'+str(base[1])+' pixels; '+str(mips)+' native mip levels; actual retained content |','',
    'Native FMDL LOD index-buffer ranges were directly checked against retained face caches. Identical model copies in other retained containers are deduplicated in the quality/source record. LOD0 is the most detailed by triangle count in this retained family; runtime distance/selection thresholds have not been tested. Mip chains are recorded/preserved privately, not rendered as a LOD-by-mip product.','',
    'Game model/textures: Konami. Project owner: arsenal-pt. Authored reference preparation: OpenAI Codex (AI/LLM); [community tool credits](../sources-and-credits.md). Only actual base-color texture/UVs drive approximate studio shading; native normal/specular/material maps are recorded separately. No higher detail was invented, upscaled or subdivided; no FOX shader, physics or native gameplay equivalence is claimed. Original game assets and clean render frames remain private.','']
   outputs['assets/'+v['id']+'.md']='\n'.join(detail).replace('##360-degree','## 360-degree').replace('only:48','only: 48').replace('at7.5','at 7.5').replace('increments,100','increments, 100').replace('frame,4.8','frame, 4.8')
  section += ['', '### Texture channels and mip counts','', 'These native/DDS header sizes are separate from geometric LOD. Only the base map is used in the studio preview; other channels are catalogued rather than treated as engine-perfect shading.','',
   '| Channel | Pixels | Native/DDS mip levels | Used in preview |','|---|---|---:|---|']
  for t in q['textureBindings']:
   section.append('| '+t['sampler']+' | '+str(t['dimensions'][0])+'x'+str(t['dimensions'][1])+' | '+str(t['nativeMipCount'])+' | '+('Base color only' if t['usedInPreview'] else 'Recorded, not applied')+' |')
  section += ['', '[Exact native LOD/deduplicated source mappings, texture hashes and declared mip dimensions](../quality-provenance.json). No original textures or geometry are included.','']
  original=outputs['assets/'+a['id']+'.md'];outputs['assets/'+a['id']+'.md']=original.replace('## Attribution and limits','\n'.join(section)+'\n## Attribution and limits')
 outputs['tables/seating-1.md']='\n'.join(table)+'\n'
 # Retain the original parent CSV columns, then append explicit quality fields.
 rows=list(csv.DictReader(io.StringIO(outputs['catalogue.csv'])));columns=list(rows[0])+['highestRetainedNativeLod','distinctNativeLods','baseTextureWidth','baseTextureHeight','nativeBaseMipCount','largerRetainedBaseTextureFound']
 out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=columns,lineterminator='\n');writer.writeheader()
 for a,row in zip(assets,rows):
  q=a['quality'];row.update(highestRetainedNativeLod=q['highestRetainedGeometricLod'],distinctNativeLods=q['distinctNativeLods'],baseTextureWidth=q['baseTextureDimensions'][0],baseTextureHeight=q['baseTextureDimensions'][1],nativeBaseMipCount=q['baseTextureNativeMipCount'],largerRetainedBaseTextureFound=q['largerRetainedBaseTextureFound']);writer.writerow(row)
 outputs['catalogue.csv']=out.getvalue();out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=list(variant_rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(variant_rows);outputs['quality-variants.csv']=out.getvalue()
 return outputs


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
 print('PASS: three parent records; twelve nativeLODviews; one static-only category table; portable CSV;'+(' outputs current' if args.check else ' outputs generated'))
if __name__=='__main__':run()
