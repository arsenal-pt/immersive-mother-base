#!/usr/bin/env python3
"""Generate the single-table static library from reviewed public metadata only.
GPL-3.0-only. No media is opened, changed or copied. No network or Git writes.
"""
from __future__ import annotations
import argparse,hashlib,json,math,re
from collections import Counter
from pathlib import Path,PurePosixPath

def raw_json(value):
    return (json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def safe_path(value):
    if not isinstance(value,str) or not value or '\\' in value or ':' in value or PurePosixPath(value).is_absolute() or '..' in PurePosixPath(value).parts:raise ValueError('Unsafe public path')
    return value

def full_metadata_search(record, browsing_values):
    """Index every original key/scalar without repeating the same search text.

    Search uses AND across whitespace terms and substring matching within this
    string. Omitting a token already inside a longer token preserves that match.
    JSON objects/lists remain unchanged in the separate original-record shards.
    """
    tokens=set()
    def add(value):
        if isinstance(value,str):text=value
        else:text=json.dumps(value,ensure_ascii=False,separators=(',',':'))
        tokens.update(text.lower().split())
        if type(value) in (int,float):
            tokens.add(re.sub(r'e([+-])0+(\d+)',r'e\1\2',text.lower()))
            if isinstance(value,float) and value.is_integer():tokens.add(str(int(value)))
    def walk(value):
        if isinstance(value,dict):
            for key,item in value.items():add(key);walk(item)
        elif isinstance(value,list):
            for item in value:walk(item)
        else:add(value)
    walk(record)
    for value in browsing_values:
        if value is not None:add(value)
    kept=[]
    for token in sorted(tokens,key=lambda value:(-len(value),value)):
        if not any(token in existing for existing in kept):kept.append(token)
    return ' '.join(sorted(kept))

def row_for(e):
    source=e['source'];loc=e['locations'];ev=e['evidence']
    path=loc.get('ganiVirtualPath') or source.get('path') or e['shortIdentifier']
    filename=PurePosixPath(path).name
    status='Per-clip visual review pending' if ev.get('perClipVisualReviewPending') is True else ('Sampled visual review' if ev.get('sampledRootVisualAcceptance') is True else 'Offline preview; review scope in details')
    # Origin labels in this catalogue are source-family interpretations, not native actor proof.
    # Never use referenceCharacter, tags, directory tokens or filename to populate character/moveset.
    row={'id':e['id'],'name':e['title'],'filename':filename,'description':e['description']['text'],
         'category':e['category']['label'],'source':source['archive'],'sourceDirectory':loc.get('ganiDirectory'),
         'sourcePath':path,'frames':e['rawFrameCount'],'duration':e['previewDurationMilliseconds'],
         'tags':e['tags'],'character':'Unknown','moveset':'Unknown','status':status,'detailPage':safe_path(e['detailPage']),
         'still':e['media']['stillThumbnail'],'gif':e['media']['fullGif'],
         'shard':'records-'+hashlib.sha256(e['id'].encode()).hexdigest()[0]+'.json'}
    searchable=[row[k] for k in ('id','name','filename','description','category','source','sourceDirectory','sourcePath','character','moveset','status')]
    searchable+=e['tags']+[e['shortIdentifier'],source.get('hashId'),source.get('payloadSha256')]+[str(v) for v in loc.values() if isinstance(v,(str,int,float))]
    row['search']=full_metadata_search(e,searchable)
    return row

def validate_entry(e):
    if not isinstance(e.get('id'),str) or not re.fullmatch(r'[A-Za-z0-9_-]+',e['id']):raise ValueError('Invalid stable ID')
    for k in ['title','shortIdentifier']:
        if not isinstance(e[k],str) or not e[k]:raise ValueError('Missing display field')
    if not isinstance(e['description']['text'],str) or not isinstance(e['tags'],list):raise ValueError('Invalid description/tags')
    for k in ['rawFrameCount','previewDurationMilliseconds']:
        v=e[k]
        if v is not None and (type(v) not in (int,float) or not math.isfinite(v) or v<0):raise ValueError('Invalid timing/frame field')
    for k in ['fullGif','animatedThumbnail','stillThumbnail']:
        m=e['media'][k];safe_path(m['path'])
        if not m['path'].startswith('media/animation-previews/') or not re.fullmatch(r'[a-f0-9]{64}',m['sha256']) or type(m['bytes']) is not int or m['bytes']<=0:raise ValueError('Invalid original media reference')
    safe_path(e['detailPage'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogue',type=Path,required=True)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True,help='New absent output directory; no source overwrite')
    parser.add_argument('--web',type=Path,default=Path(__file__).with_name('web'))
    args=parser.parse_args();config=json.loads(args.config.read_text(encoding='utf-8-sig'))
    if args.output.exists():raise SystemExit('Output directory already exists; use a new review directory')
    if args.catalogue.is_symlink() or not args.catalogue.is_file():raise SystemExit('Catalogue missing or symlinked')
    if args.catalogue.stat().st_size!=config['catalogueBytes']:raise SystemExit('Pinned catalogue size changed; review config')
    raw=args.catalogue.read_bytes()
    if sha(raw)!=config['catalogueSha256']:raise SystemExit('Pinned catalogue SHA256 changed; review config')
    gitblob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if gitblob!=config['catalogueGitBlob']:raise SystemExit('Pinned catalogue Git blob changed')
    c=json.loads(raw);entries=c['entries'];ids=[e['id'] for e in entries]
    if len(entries)!=config['expectedEntryCount'] or c['entryCount']!=len(entries) or len(set(ids))!=len(ids):raise SystemExit('Catalogue identity/count mismatch')
    if not re.fullmatch(r'[a-f0-9]{40}',config['sourceCommit']):raise SystemExit('Source commit must be immutable')
    shards={};rows=[];media_refs={}
    for e in entries:
        validate_entry(e);r=row_for(e);rows.append(r);shards.setdefault(r['shard'],{})[e['id']]=e
        for key,m in e['media'].items():
            if not isinstance(m,dict) or 'path' not in m:continue
            if m['path'] in media_refs and media_refs[m['path']]!={k:m[k] for k in ['sha256','bytes']}:raise ValueError('Conflicting original media reference')
            media_refs[m['path']]={k:m[k] for k in ['sha256','bytes']}
    header={k:v for k,v in c.items() if k!='entries'}
    search_dictionary=sorted({token for row in rows for token in row['search'].split()})
    search_ids={token:i for i,token in enumerate(search_dictionary)}
    for row in rows:row['searchTokens']=[search_ids[token] for token in row.pop('search').split()]
    index={'schemaVersion':2,'entryCount':len(rows),'repository':config['repository'],'sourceCommit':config['sourceCommit'],
           'catalogueSha256':sha(raw),'searchDictionary':search_dictionary,'metadataHeader':'catalogue-metadata.json','characterPolicy':config['characterPolicy'],'movesetPolicy':config['movesetPolicy'],'rows':rows}
    outputs={'data/index.json':raw_json(index),'data/catalogue-metadata.json':raw_json(header)}
    for name,records in sorted(shards.items()):outputs['data/'+name]=raw_json({'schemaVersion':1,'entries':records})
    for name in ['index.html','style.css','app.mjs','core.mjs']:
        p=args.web/name
        if p.is_symlink() or not p.is_file():raise ValueError('Missing or linked authored web input')
        outputs[name]=p.read_bytes()
    outputs['.nojekyll']=b''
    # Verify generated serialization recovers every original field/value, including catalogue-level provenance.
    recovered={}
    for name,body in outputs.items():
        if name.startswith('data/records-'):recovered.update(json.loads(body)['entries'])
    assert set(recovered)==set(ids) and all(recovered[e['id']]==e for e in entries)
    assert json.loads(outputs['data/catalogue-metadata.json'])==header
    assert {r['id'] for r in json.loads(outputs['data/index.json'])['rows']}==set(ids)
    report={'schemaVersion':1,'result':'PASS','input':{'path':str(args.catalogue),'bytes':len(raw),'sha256':sha(raw),'gitBlob':gitblob},
            'sourceCommit':config['sourceCommit'],'entryCount':len(entries),'oneToOneIds':True,'allOriginalEntryFieldsRetained':True,'allCatalogueHeaderFieldsRetained':True,
            'mediaReferenceCount':len(media_refs),'mediaReferences':media_refs,'mediaReadOrChanged':False,'nativeProofAdded':False,
            'searchCoverage':'all original entry field names and scalar values; shared dictionary of de-duplicated substring-preserving tokens','searchDictionaryTokens':len(search_dictionary),'indexBytes':len(outputs['data/index.json']),'detailShardCount':len(shards),'statusCounts':dict(Counter(r['status'] for r in rows)),
            'characterCounts':dict(Counter(r['character'] for r in rows)),'movesetCounts':dict(Counter(r['moveset'] for r in rows)),
            'outputs':[{'path':name,'bytes':len(body),'sha256':sha(body)} for name,body in sorted(outputs.items())]}
    args.output.mkdir(parents=True)
    for name,body in outputs.items():
        path=args.output/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(body)
    (args.output/'BUILD-REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['mediaReferences','outputs']},sort_keys=True))
if __name__=='__main__':main()
