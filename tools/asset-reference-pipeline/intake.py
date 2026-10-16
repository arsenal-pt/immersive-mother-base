"""Deterministic next-unfinished intake from existing retained indexes; no AI/network."""
import json
from pathlib import Path
import sqlite3
import time
import uuid
import zlib
from runtime import ManualReview, WorkerLock, canonical, digest, inside, load, save, sha
from catalogue import export_catalogue

CATEGORIES = {
    'furniture':'Furniture', 'fixture':'Fixtures', 'industrial_prop':'Industrial equipment',
    'radio_and_control_equipment':'Radio and control equipment', 'document_or_sign':'Documents and signs',
    'shell_element':'Architecture sections', 'story_mechanical_display':'Story/mechanical displays',
    'unknown':'Unclassified'}
DEPENDENCIES = ('python','blender','render-preview.py','encode-previews.py','FmdlReader.py','Native-Materials.py','native.py')


def setup(store):
    store.db.executescript('''
    CREATE TABLE IF NOT EXISTS intake_sources(id TEXT PRIMARY KEY,fingerprint TEXT,entries INTEGER);
    CREATE TABLE IF NOT EXISTS intake(
      key TEXT PRIMARY KEY,source_id TEXT,position INTEGER,category TEXT,entry TEXT,
      signature TEXT,status TEXT,reason TEXT,job_id TEXT,attempts INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS batches(
      id TEXT PRIMARY KEY,source_id TEXT,category TEXT,allowance TEXT,status TEXT,
      attempted INTEGER,completed INTEGER,last_key TEXT,updated REAL);
    CREATE TABLE IF NOT EXISTS preferences(key TEXT PRIMARY KEY,value TEXT);
    ''')


def private_path(path, cfg):
    p = Path(path).resolve()
    if not any(inside(p, r) for r in cfg['sourceRoots']):
        raise ManualReview('Intake input outside configured private source roots: '+str(p))
    if not p.is_file():
        raise ManualReview('Required retained preparation is missing: '+str(p))
    return p


def bundle_paths(cfg):
    config = cfg.get('intake')
    if not config:
        raise ManualReview('Configure intake.sourceRoot/index once; no automatic game/DAT scan is performed')
    root = Path(config['sourceRoot']).resolve()
    defaults = {'index':'Special-Rooms/Editor/Curated-Asset-Index.json',
                'materials':['Material-Dependency-Manifest.json','Special-Rooms/Material-Dependency-Manifest.json'],
                'members':['Source-Manifest.json','Special-Rooms/Pack-Members.json']}
    paths = {'index':private_path(root/config.get('index',defaults['index']),cfg)}
    for key in ('materials','members'):
        paths[key] = [private_path(root/p,cfg) for p in config.get(key,defaults[key])]
    return root, paths


def build_entries(root, paths, cfg):
    """Join prepared metadata; selected native/DDS bytes are verified before use."""
    index = load(paths['index'])['assets']
    materials, members = {}, {}
    for p in paths['materials']:
        for value in load(p)['models'].values():
            for record in value if isinstance(value,list) else [value]:
                materials.setdefault(record['nativeSha256'],[]).append(record)
    for p in paths['members']:
        source = load(p)
        packs = source['packs'] if isinstance(source,dict) else source
        for pack in packs:
            if 'source' in pack:
                container, container_sha = pack['source']['path'],pack['source']['sha256']
            else:
                container, container_sha = pack['gamePath'],pack['sha256']
            for f in pack['files']:
                if f['gamePath'].endswith('.fmdl'):
                    members.setdefault(f['sha256'],[]).append(
                        {'path':f['gamePath'],'container':container,'containerSha256':container_sha})
    entries=[]
    seen=set()
    for position, asset in enumerate(index):
        identity = asset['sha256']
        if identity in seen:
            continue
        seen.add(identity)
        reasons=[]
        found=sorted((x for x in members.get(identity,[]) if
                      x['path'].casefold()==asset['nativeFmdlPath'].casefold()),
                     key=lambda x:(x['path'],x['container'],x['containerSha256']))
        if not found:
            reasons.append('Exact native member spelling unresolved; historical normalized path retained privately')
        cache_path=root/asset['cache']
        # Eligibility only reads existing cached metadata. No whole-index native decode/hash/render.
        try:
            cache=json.loads(zlib.decompress(private_path(cache_path,cfg).read_bytes()))
            if cache['sha256'] != identity:
                reasons.append('Retained decoded metadata identity differs')
            if cache['unsupportedAttributes'] or any(
                set(m['attributes'])-{'2','8','9','10','11','12','13','14'} for m in cache['meshes']):
                reasons.append('Unsupported static vertex layout; characters/skinning require preparation')
            if any(g['hidden'] for g in cache['meshGroups']):
                reasons.append('Hidden mesh groups need a reviewed assembly recipe')
            if any('8' not in m['attributes'] or '2' not in m['attributes'] for m in cache['meshes']):
                reasons.append('Missing explicit native UV0/normals')
        except (OSError,ValueError,KeyError,ManualReview):
            reasons.append('Required retained decoded metadata missing/invalid')
        records=materials.get(identity,[])
        bindings=[]
        if not records:
            reasons.append('No retained native-SHA material record')
        else:
            counts={len(r['materials']) for r in records}
            if len(counts)!=1:
                reasons.append('Conflicting retained material counts')
            else:
                for mi in range(next(iter(counts))):
                    bases=[]
                    for r in records:
                        bases.extend(t for t in r['materials'][mi]['textures']
                                     if t.get('samplerName') in ('Base_Tex_SRGB','Base_Tex_LIN'))
                    native_ids={(str(t.get('pathHash')),t.get('samplerName'),t.get('samplerNameHash')) for t in bases}
                    choices={d['sha256']:[] for t in bases for d in t.get('ddsChoices',[])}
                    for t in bases:
                        for d in t.get('ddsChoices',[]):
                            choices[d['sha256']].append(d)
                    if len(native_ids)!=1 or len(choices)!=1:
                        reasons.append('Material '+str(mi)+' has missing/ambiguous native base binding or DDS content')
                        continue
                    native_hash,sampler,sampler_hash=next(iter(native_ids))
                    if not native_hash.isdigit() or sampler_hash is None:
                        reasons.append('Material '+str(mi)+' hash-only sampler proof unavailable')
                        continue
                    candidates=sorted(next(iter(choices.values())),key=lambda d:d['dds'])
                    available=[d for d in candidates if (root/d['dds']).is_file()]
                    if not available:
                        reasons.append('Material '+str(mi)+' retained converted DDS missing')
                        continue
                    choice=available[0]
                    dds=root/choice['dds']
                    binding={'materialIndex':mi,'samplerName':sampler,'samplerNameHash':str(sampler_hash),
                             'nativePathHash':native_hash,'dds':{'file':str(dds),'sha256':choice['sha256']}}
                    if dds.with_suffix('.ftex').is_file():
                        binding['ftexHeader']={'file':str(dds.with_suffix('.ftex')),'sha256':sha(dds.with_suffix('.ftex'))}
                    bindings.append(binding)
        exact=found[0] if found else None
        stem=Path(asset['nativeFmdlPath']).stem
        folder=asset['nativeFmdlPath'].split('/')[-4]
        title=folder.replace('_',' ').capitalize()+(' component/variant' if folder=='shelf' else '')+' ('+stem+')'
        recipe={'id':'mgsv-tpp-'+stem+'-'+identity[:12],'stem':stem,'title':title,
                'description':'Static asset recorded in the '+folder+' folder; identifier '+stem+
                              '. One native model/version; complete assembly is not established. Offline reference using its retained base textures.',
                'category':CATEGORIES.get(asset['category'],asset['category']),'tags':[folder,stem,asset['category']],
                'adapter':'retained-static','staticOnly':True,'lods':[0],
                'model':{'file':str(root/asset['raw']),'sha256':identity,
                         'virtualPath':exact['path'] if exact else asset['nativeFmdlPath'],
                         'container':{'virtualPath':exact['container'],'sha256':exact['containerSha256']} if exact else {}},
                'baseTextures':bindings,
                'sourceEvidence':{'normalizedLookupKey':asset['nativeFmdlPath'].casefold(),
                                  'exactMemberRecord':bool(exact),'duplicateRetainedOccurrences':len(found),
                                  'memberEvidence':'Retained member record joined by native SHA/path; selected raw hash rechecked. Archive not freshly unpacked.',
                                  'upstreamPreparation':'Already extracted native FMDL and converted DDS; GzsTool/FtexTool not invoked for this entry.'}}
        entry={'key':identity+'-lod0','position':position,'category':asset['category'],'recipe':recipe,
               'reason':'; '.join(sorted(set(reasons)))}
        entry['signature']=digest({k:v for k,v in recipe.items() if k not in ('title','description','tags','category','sourceEvidence')})
        entries.append(entry)
    return entries


def import_index(store,cfg):
    setup(store)
    root,paths=bundle_paths(cfg)
    source_id=digest(str(paths['index']).casefold())[:24]
    fingerprints={str(p):sha(p) for p in [paths['index'],*paths['materials'],*paths['members']]}
    fingerprint=digest({'files':fingerprints,'metadataSchemaVersion':2})
    old=store.db.execute('SELECT fingerprint FROM intake_sources WHERE id=?',(source_id,)).fetchone()
    if old is None or old[0]!=fingerprint:
        entries=build_entries(root,paths,cfg)
        active=set()
        for e in entries:
            active.add(e['key'])
            previous=store.db.execute('SELECT signature,status,job_id,attempts FROM intake WHERE key=?',(e['key'],)).fetchone()
            same=previous is not None and previous['signature']==e['signature']
            status=previous['status'] if same else ('manual_review' if e['reason'] else 'pending')
            reason=e['reason'] if not same else store.db.execute('SELECT reason FROM intake WHERE key=?',(e['key'],)).fetchone()[0]
            store.db.execute('''INSERT OR REPLACE INTO intake
                (key,source_id,position,category,entry,signature,status,reason,job_id,attempts)
                VALUES(?,?,?,?,?,?,?,?,?,?)''',
                (e['key'],source_id,e['position'],e['category'],canonical(e),e['signature'],status,reason,
                 previous['job_id'] if same else None,previous['attempts'] if previous else 0))
        for row in store.db.execute('SELECT key FROM intake WHERE source_id=?',(source_id,)).fetchall():
            if row[0] not in active:
                store.db.execute("UPDATE intake SET status='out_of_scope' WHERE key=?",(row[0],))
        store.db.execute('INSERT OR REPLACE INTO intake_sources VALUES(?,?,?)',(source_id,fingerprint,len(entries)))
        store.db.commit()
    return source_id


def media_valid(store,job):
    try:
        row=store.job(job)
        if row['status']!='complete':
            return False
        result=json.loads(row['result'])
        return len(result['media'])==3 and all(inside(x['file'],store.root) and
                 Path(x['file']).is_file() and sha(x['file'])==x['sha256'] for x in result['media'])
    except (ValueError,KeyError,TypeError,OSError):
        return False


def content_matches(record,recipe):
    expected={(b['materialIndex'],str(b['nativePathHash']),b['dds']['sha256']) for b in recipe['baseTextures']}
    actual={(b['materialIndex'],str(b['nativePathHash']),b['sha256']) for b in record['baseTextures']}
    return record['modelSha256']==recipe['model']['sha256'] and record['lod']==0 and expected==actual


def compatible_completion(store,job,record,recipe,tools,settings):
    if not content_matches(record,recipe) or not media_valid(store,job):
        return False
    for name in DEPENDENCIES:
        expected={k:v for k,v in tools[name].items() if k!='path'}
        if record.get('tools',{}).get(name)!=expected:
            return False
    stage=store.db.execute("SELECT receipt FROM stages WHERE job_id=? AND name='render'",(job,)).fetchone()
    try:
        if stage is None:
            return False
        config=load(Path(stage[0]).parent/'render-config.json')
        return config['settings']==settings
    except (OSError,ValueError,KeyError):
        return False


def reconcile(store,source_id,cfg,tools,settings,verify):
    """Reuse proven output across adapter recipe shapes; preserve existing job recipe."""
    jobs=[]
    for row in store.db.execute('SELECT a.job_id,a.record FROM assets a JOIN jobs j ON j.id=a.job_id WHERE j.status="complete"'):
        jobs.append((row['job_id'],json.loads(row['record'])))
    for row in store.db.execute('SELECT * FROM intake WHERE source_id=? AND status!="out_of_scope"',(source_id,)).fetchall():
        e=json.loads(row['entry']);r=e['recipe']
        candidates=[(j,a) for j,a in jobs if content_matches(a,r)]
        if not candidates:
            if row['status']=='complete':
                store.db.execute("UPDATE intake SET status='pending',job_id=NULL,reason='Prior completion no longer matches current content' WHERE key=?",(row['key'],))
            continue
        # Source bytes and current material content must still match before skipping.
        try:
            verify(r,cfg)
        except (ManualReview,OSError,ValueError) as ex:
            store.db.execute("UPDATE intake SET status='manual_review',reason=? WHERE key=?",(str(ex),row['key']))
            continue
        valid=[(j,a) for j,a in candidates if compatible_completion(store,j,a,r,tools,settings)]
        if valid:
            job,record=valid[-1]
            for field in ('title','description','category','tags'):
                record[field]=r[field]
            store.db.execute('UPDATE assets SET record=? WHERE job_id=?',(canonical(record),job))
            store.db.execute("UPDATE intake SET status='complete',reason='',job_id=? WHERE key=?",(job,row['key']))
        else:
            # Reuse original compatible-source job for stage-specific invalidation (e.g. encode only).
            store.db.execute("UPDATE intake SET status='pending',reason='Prior output/tool fingerprint requires revalidation',job_id=? WHERE key=?",
                             (candidates[-1][0],row['key']))
    store.db.commit()


def counts(store,source_id,category='all'):
    sql='SELECT status,count(*) FROM intake WHERE source_id=? AND status!="out_of_scope"'
    args=[source_id]
    if category!='all':
        sql+=' AND category=?';args.append(category)
    return dict(store.db.execute(sql+' GROUP BY status',args).fetchall())


def next_entries(store,source_id,category,count):
    sql="SELECT * FROM intake WHERE source_id=? AND status IN ('pending','cancelled')"
    args=[source_id]
    if category!='all':
        sql+=' AND category=?';args.append(category)
    sql+=' ORDER BY position,key'
    rows=store.db.execute(sql,args).fetchall()
    return rows if count is None else rows[:count]


def allowance(value):
    if value.lower()=='all':
        return None
    try:
        count=int(value)
    except ValueError:
        raise ValueError('Enter a positive integer or all for all remaining in this category')
    if count<1:
        raise ValueError('Count must be at least1; use all explicitly for all remaining')
    return count


def prompt(store,source_id,cfg,category,count):
    available=[r[0] for r in store.db.execute('SELECT DISTINCT category FROM intake WHERE source_id=? ORDER BY category',(source_id,))]
    if category is None:
        previous=store.db.execute("SELECT value FROM preferences WHERE key='category'").fetchone()
        default=previous[0] if previous and previous[0] in available+['all'] else cfg['intake'].get('defaultCategory','furniture')
        print('Category choices (retained index only):',flush=True)
        choices=['all',*available]
        for i,c in enumerate(choices):
            print(str(i)+': '+('All retained categories' if c=='all' else CATEGORIES.get(c,c))+' '+canonical(counts(store,source_id,c)),flush=True)
        while True:
            selected=input('Category number/name ['+default+']: ').strip() or default
            if selected.isdigit() and int(selected)<len(choices):
                selected=choices[int(selected)]
            if selected in choices:
                category=selected;break
            print('Choose one listed category; unknown/unclassified is a real retained category.')
    if category not in available+['all']:
        raise ManualReview('Unknown category: '+str(category))
    if count is None:
        default=str(cfg['intake'].get('defaultCount',25))
        while True:
            value=input('Maximum unfinished unique assets this run ['+default+']; type all for ALL remaining: ').strip() or default
            try:
                count=allowance(value);break
            except ValueError as ex:
                print(str(ex))
    else:
        count=allowance(str(count))
    store.db.execute("INSERT OR REPLACE INTO preferences VALUES('category',?)",(category,))
    store.db.commit()
    return category,count


def recipe_content(recipe):
    return (recipe['model']['sha256'],tuple(sorted(
        (b['materialIndex'],str(b['nativePathHash']),b.get('ddsSha256') or b.get('dds',{}).get('sha256'))
        for b in recipe['baseTextures'])))


def execute_batch(store,source_id,category,count,cfg,tools,runner,verify=None):
    selected=next_entries(store,source_id,category,count)
    batch=uuid.uuid4().hex
    store.db.execute('INSERT INTO batches VALUES(?,?,?,?,?,?,?,?,?)',
                     (batch,source_id,category,'all' if count is None else str(count),'running',0,0,None,time.time()))
    store.db.commit()
    attempted=completed=attention=0
    active=job=None
    cancelled=False
    try:
        for row in selected:
            active=row['key'];e=json.loads(row['entry']);job=row['job_id']
            if job is not None:
                old=json.loads(store.job(job)['recipe'])
                reusable=recipe_content(old)==recipe_content(e['recipe'])
                if reusable and verify:
                    try:
                        verify(old,cfg)
                    except (ManualReview,OSError,ValueError,KeyError):
                        reusable=False
                if not reusable:
                    job=None
            if job is None:
                job=store.enqueue(e['recipe'],0)
            else:
                store.db.execute("UPDATE jobs SET status='queued',cancel=0 WHERE id=?",(job,))
            attempted+=1
            store.db.execute("UPDATE intake SET status='running',job_id=?,attempts=attempts+1 WHERE key=?",(job,active))
            store.db.execute('UPDATE batches SET attempted=?,last_key=?,updated=? WHERE id=?',
                             (attempted,active,time.time(),batch))
            store.db.commit()
            print('Asset '+str(attempted)+'/'+str(len(selected))+': '+e['recipe']['stem']+'; job '+job,flush=True)
            ok=runner(store,job,cfg,tools)
            status=store.job(job)['status']
            if ok:
                status='complete';completed+=1
                record=json.loads(store.db.execute('SELECT record FROM assets WHERE job_id=?',(job,)).fetchone()[0])
                for field in ('title','description','category','tags'):
                    record[field]=e['recipe'][field]
                store.db.execute('UPDATE assets SET record=? WHERE job_id=?',(canonical(record),job))
            if status not in ('complete','cancelled','manual_review','failed'):
                status='failed'
            if status in ('manual_review','failed'):
                attention+=1
            reason=store.job(job)['error'] or ''
            store.db.execute('UPDATE intake SET status=?,reason=? WHERE key=?',(status,reason,active))
            store.db.execute('UPDATE batches SET completed=?,status=?,updated=? WHERE id=?',
                             (completed,'cancelled' if status=='cancelled' else 'running',time.time(),batch))
            store.db.commit()
            active=None
            if status=='cancelled':
                cancelled=True;break
    except KeyboardInterrupt:
        cancelled=True
        if active is not None:
            if job is not None and store.job(job)['status']!='complete':
                store.status(job,'cancelled','Interrupted during batch claim/bookkeeping')
            store.db.execute("UPDATE intake SET status='cancelled',reason=? WHERE key=?",
                             ('Interrupted during batch claim/bookkeeping; safe to resume',active))
    finally:
        store.db.execute('UPDATE batches SET status=?,completed=?,updated=? WHERE id=?',
                         ('cancelled' if cancelled else 'complete',completed,time.time(),batch))
        store.db.commit()
    return {'batch':batch,'attemptedUniqueAssets':attempted,'newlyCompleted':completed,
            'needsAttention':attention,'cancelled':cancelled,'remainingCounts':counts(store,source_id,category)}


def aggregate_jobs(store):
    unique={}
    intake={r['key']:(r['status'],r['job_id']) for r in store.db.execute('SELECT key,status,job_id FROM intake WHERE status!="out_of_scope"')}
    for row in store.db.execute('SELECT a.job_id,a.record FROM assets a JOIN jobs j ON j.id=a.job_id WHERE j.status="complete" ORDER BY j.updated'):
        record=json.loads(row['record'])
        state=intake.get(record['modelSha256']+'-lod'+str(record['lod']))
        if state is not None and (state[0]!='complete' or state[1]!=row['job_id']):
            continue
        if media_valid(store,row['job_id']):
            unique[(record['modelSha256'],record['lod'])]=row['job_id']
    return sorted(unique.values())


def library(store,cfg,tools,settings,verify,runner,category=None,count=None,plan=False,retry=False):
    with WorkerLock(store.root):
        source_id=import_index(store,cfg)
        # A new worker owns the lock. Recover only intake bookkeeping; never kill/infer cleanup of old children.
        store.db.execute("UPDATE intake SET status='cancelled',reason='Interrupted prior batch bookkeeping; resume pending' WHERE status='running' AND job_id IN (SELECT id FROM jobs WHERE status IN ('queued','cancelled','complete'))")
        store.db.execute("UPDATE intake SET status='manual_review',reason='Prior running job needs owned-process inspection; hard-crash cleanup is manual' WHERE status='running'")
        store.db.execute("UPDATE batches SET status='interrupted' WHERE status='running'")
        store.db.commit()
        reconcile(store,source_id,cfg,tools,settings,verify)
        total=store.db.execute('SELECT entries FROM intake_sources WHERE id=?',(source_id,)).fetchone()[0]
        print('Scope: '+str(total)+' unique retained versions; not whole-game extraction.',flush=True)
        print('Candidates require per-entry native/source verification. Current totals: '+canonical(counts(store,source_id)),flush=True)
        category,count=prompt(store,source_id,cfg,category,count)
        if retry:
            if plan:
                raise ManualReview('Retry-review is an execution action; use a normal plan to inspect current pending entries')
            sql="UPDATE intake SET status='pending',reason='' WHERE source_id=? AND status IN ('manual_review','failed')"
            values=[source_id]
            if category!='all':
                sql+=' AND category=?';values.append(category)
            store.db.execute(sql,values);store.db.commit()
        if plan:
            preview=[{'key':r['key'],'stem':json.loads(r['entry'])['recipe']['stem'],'status':r['status']}
                     for r in next_entries(store,source_id,category,count)]
            print('NEXT_UNFINISHED '+canonical(preview),flush=True)
            return {'planned':preview,'counts':counts(store,source_id,category)}
        summary=execute_batch(store,source_id,category,count,cfg,tools,runner,verify)
        jobs=aggregate_jobs(store)
        if jobs:
            export_root=Path(cfg['exportRoot']).resolve()
            destination=export_root/(time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
            if any(inside(destination,r) or inside(r,destination) for r in cfg['sourceRoots']):
                raise ManualReview('Aggregate export must be outside source roots')
            summary['export']=export_catalogue(store,destination,jobs)
            summary['cataloguePath']=str(destination)
            print('CATALOGUE_EXPORT '+str(destination),flush=True)
        summary['globalCounts']=counts(store,source_id)
        print('BATCH_RESULT '+canonical(summary),flush=True)
        return summary
