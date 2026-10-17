"""Normalize reviewed installed-source references; no extraction or rendering.

Operational paths stay private. Original portable records are retained verbatim
in batch provenance by the staging caller. Existing accepted objects stay intact.
"""
import copy, hashlib, json, re
from pathlib import Path
import import_batch


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def reference_identity(record,policy):
    fields=('materialIndex','samplerName','samplerNameHash','nativePathHash','nativePath','sha256','familyId')
    textures=[{k:t.get(k) for k in fields} for t in record['baseTextures']]
    return digest({'model':record['modelSha256'],'lod':record['lod'],
                   'textures':sorted(textures,key=lambda t:(t['materialIndex'],t['sha256'])),
                   'renderPolicy':policy})


def normalize(record,result,media_prefix,verify=True):
    import_batch.portable(record);import_batch.portable(result['policy'])
    identifier=record['id']
    if not re.fullmatch(r'[A-Za-z0-9_-]+',identifier):raise ValueError('Unsafe portable asset ID')
    if not media_prefix.startswith('media/asset-previews/'):raise ValueError('Dedicated media prefix required')
    import_batch.safe_path(Path.cwd(),media_prefix)
    evidence=copy.deepcopy(record['sourceEvidence'])
    if evidence.get('contentSha256')!=record['modelSha256']:raise ValueError('Source evidence/hash mismatch')
    base=record['baseTextures'];levels=record['nativeLods']
    if not base or not levels or not any(v['nativeLod']==record['lod'] for v in levels):raise ValueError('Missing base textures or selected native LOD')
    by_name={}
    for artifact in result['artifact_files']:
        name=Path(artifact['file']).name
        if name in by_name and by_name[name]!=artifact:raise ValueError('Ambiguous artifact basename')
        by_name[name]=artifact
    paths={};media=[];copies=[]
    for field,key in [('still','still'),('turntable','gif'),('thumbnail','thumbnail')]:
        name=Path(record[key]).name;a=by_name[name];source=Path(a['file'])
        if verify:
            data=source.read_bytes()
            if len(data)!=a['bytes'] or hashlib.sha256(data).hexdigest()!=a['sha256']:raise ValueError('Artifact hash/size mismatch: '+name)
            import_batch.validate_media(source,field)
        target=media_prefix+'/'+name;paths[field]=target
        media.append({'path':target,'sha256':a['sha256'],'bytes':a['bytes']})
        copies.append((source,target,a['sha256'],a['bytes']))
    native=record['modelPath'];namespace=native.split('/object/',1)[1].split('/',1)[0] if '/object/' in native else 'Unknown (no object namespace)'
    most=max(v['triangles'] for v in levels);materials=[]
    for t in base:
        materials.append({'sampler':t.get('samplerName') or 'Unknown base sampler','materialIndex':t['materialIndex'],
            'nativePathHash':str(t['nativePathHash']) if t.get('nativePathHash') is not None else 'Unknown; see original binding',
            'nativeVirtualPath':t.get('nativePath'),'nativeBinding':copy.deepcopy(t),'ddsSha256':t['sha256'],
            'dimensions':[t['width'],t['height']],'mipCount':t['mipCount'],'nativeMipCountVerified':t['nativeMipCountVerified'],'connectedInPreview':True})
    identity=reference_identity(record,result['policy'])
    out={'id':identifier,'title':import_batch.plain(record['title'],identifier,180),
        'category':import_batch.plain(record['category'],'Discovered static models',80),'subcategory':'Installed-source static components',
        'tags':[import_batch.plain(t,limit=80) for t in record.get('tags',[])],
        'description':import_batch.plain(record['description']),
        'descriptionProvenance':'Sanitized native filename/pipeline evidence; no invented interaction or assembly claim',
        'sourceNamespace':namespace,'observedUse':'Selected as-installed source occurrence; placement/effective runtime priority unresolved',
        'referenceIdentitySha256':identity,
        'batchImport':{'schemaVersion':2,'sourceMode':'installed','provenance':'batch-provenance.json','sourceRecordSha256':digest(record),'upstreamPreparation':record['upstreamPreparation']},
        'source':{'nativePath':native,'nativeSha256':record['modelSha256'],'stableIdentity':native.lower()+'#'+record['modelSha256']+'#'+identity,
            'container':{'nativePath':record['containerPath'],'sha256':record['containerSha256'],'status':'Selected installed-source container/member chain captured by community reader'},
            'historicalDatOrigin':None,'sourceArchiveAtCapture':evidence.get('source_path'),
            'locationStatus':'Selected native member/content and captured installed-source chain; full archive SHA/runtime priority unresolved',
            'currentInstalledDatVerified':False,'selectedInstalledMemberVerified':True,'evidence':evidence},
        'geometry':{'lod':record['lod'],'triangles':record['triangles'],'originalGeometryAndUvsUnchanged':True},
        'materials':materials,
        'preview':{**paths,'stillDimensions':[768,768],'gifDimensions':[480,480],'thumbnailDimensions':[160,160],
            'gifFrames':48,'frameDelayMs':100,'durationMs':4800,'loop':0,'nativeAnimation':False,'nativeShaderEquivalent':False,
            'textureRendering':'Actual captured base textures/UVs; approximate studio shading','media':media},
        'quality':{'decodedIndicesHashDerivation':'SHA256 of canonical UTF-8 JSON decoded triangle indices grouped by mesh; not packed buffer bytes',
            'highestRetainedGeometricLod':min(v['nativeLod'] for v in levels if v['triangles']==most),
            'distinctNativeLods':len({v['indicesSha256'] for v in levels}),'baseTextureDimensions':[base[0]['width'],base[0]['height']],
            'baseTextureNativeMipCount':base[0]['mipCount'] if base[0]['nativeMipCountVerified'] else None,'largerRetainedBaseTextureFound':None,
            'nativeLods':copy.deepcopy(levels),'renderedNativeLods':[record['lod']],'baseTextureSummary':record['baseTextureSummary'],
            'highestDetailScope':'Triangle-count comparison within captured FMDL only'},
        'credits':{'gameModelAndTextures':'Konami','referenceOwner':'arsenal-pt','referenceImplementation':'OpenAI Codex, AI/LLM-authored','toolSources':'sources-and-credits.md'}}
    import_batch.portable(out)
    return out,copies


def merge(existing,records):
    merged=copy.deepcopy(existing);by_id={a['id']:a for a in merged['assets']}
    by_identity={a['referenceIdentitySha256']:a['id'] for a in merged['assets'] if 'referenceIdentitySha256' in a};aliases={}
    for a in records:
        if a['id'] in by_id:
            if a!=by_id[a['id']]:raise ValueError('Refusing differing accepted asset ID '+a['id'])
            continue
        identity=a['referenceIdentitySha256']
        if identity in by_identity:aliases[a['id']]=by_identity[identity];continue
        merged['assets'].append(copy.deepcopy(a));by_id[a['id']]=a;by_identity[identity]=a['id']
    return merged,aliases


def installed_detail(text,asset):
    text=text.replace('Retained container','Captured source container').replace('Actual retained base textures/UVs','Actual captured base textures/UVs')
    text=text.replace('Not verified; outer DAT unknown for this record','Captured as-installed chain; full archive SHA and effective runtime priority unresolved')
    rows=['## Captured base-texture locations','','| Material | Actual native texture path | Complete family identity |','|---|---|---|']
    for t in asset['materials']:
        rows.append('| '+str(t['materialIndex'])+' | `'+(t.get('nativeVirtualPath') or 'Unknown; native binding retained')+'` | `'+str(t['nativeBinding'].get('familyId','Unknown'))+'` |')
    return text+'\n'+'\n'.join(rows)+'\n'
