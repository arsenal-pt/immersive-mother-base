"""Synthetic queue/cursor contracts. No native source, converter or Blender run."""
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
from runtime import ManualReview, Store, canonical, save, sha
from intake import (DEPENDENCIES, aggregate_jobs, allowance, compatible_completion, content_matches,
                    counts, execute_batch, import_index, next_entries, prompt, reconcile, setup)

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='mgsv-intake-tests-')
        self.root=Path(self.temp.name);self.store=Store(self.root/'runtime');setup(self.store)
        self.cfg={'sourceRoots':[str(self.root/'source')]}
        self.tools={name:{'sha256':'tool-'+name,'fileVersion':None,'path':'private'} for name in DEPENDENCIES}
        self.settings={'stillSize':768,'frameCount':48}
        self.source='fixture-source'

    def tearDown(self):
        self.store.db.close();self.temp.cleanup()

    def entry(self,index,category='furniture',status='pending',reason=''):
        model=hashlib.sha256(('model'+str(index)).encode()).hexdigest()
        folder=self.root/'source';folder.mkdir(exist_ok=True)
        file=folder/('model'+str(index)+'.fmdl');file.write_bytes(b'native'+str(index).encode())
        dds=folder/('base'+str(index)+'.dds');dds.write_bytes(b'texture'+str(index).encode())
        recipe={'id':'prop'+str(index),'stem':'prop'+str(index),'title':'Prop '+str(index),
                'description':'Clean ordinary description','category':'Furniture','tags':['prop'],'staticOnly':True,
                'adapter':'retained-static','lods':[0],'model':{'file':str(file),'sha256':model,
                'virtualPath':'/Assets/prop'+str(index)+'.fmdl','container':{'virtualPath':'/Assets/pack.fpk','sha256':'c'*64}},
                'baseTextures':[{'materialIndex':0,'nativePathHash':'123','samplerName':'Base_Tex_SRGB','dds':{'file':str(dds),'sha256':sha(dds)}}]}
        e={'key':model+'-lod0','position':index,'category':category,'recipe':recipe,'signature':'signature'+str(index),'reason':reason}
        self.store.db.execute('INSERT INTO intake VALUES(?,?,?,?,?,?,?,?,?,0)',
            (e['key'],self.source,index,category,canonical(e),e['signature'],status,reason,None))
        self.store.db.commit()
        return e

    def runner(self,store,job,cfg,tools):
        r=json.loads(store.job(job)['recipe']);key=r['id']
        folder=store.root/'fixture-media'/key;folder.mkdir(parents=True,exist_ok=True)
        media=[]
        for suffix in ('.png','-thumb.png','-360.gif'):
            p=folder/(key+suffix);Image.new('RGB',(8,8),'white').save(p)
            media.append({'file':str(p),'sha256':sha(p)})
        record={'id':key,'modelSha256':r['model']['sha256'],'lod':0,'baseTextures':[
                    {'materialIndex':0,'nativePathHash':'123','sha256':r['baseTextures'][0]['dds']['sha256']}],
                'tools':{name:{k:v for k,v in x.items() if k!='path'} for name,x in self.tools.items()}}
        store.db.execute('INSERT OR REPLACE INTO assets VALUES(?,?)',(job,canonical(record)))
        store.status(job,'complete',result={'media':media})
        render=store.root/'fixture-render'/job;render.mkdir(parents=True,exist_ok=True)
        save(render/'render-config.json',{'settings':self.settings})
        store.db.execute('INSERT OR REPLACE INTO stages VALUES(?,?,?,?,?,0)',(job,'render','fingerprint','complete',str(render/'stage.json')))
        store.db.commit()
        return True

    def test_next25_then_next25_after_restart_excludes_completed(self):
        for i in range(52):self.entry(i)
        first=execute_batch(self.store,self.source,'furniture',25,self.cfg,self.tools,self.runner)
        self.assertEqual(first['attemptedUniqueAssets'],25)
        before={r['key'] for r in self.store.db.execute("SELECT key FROM intake WHERE status='complete'")}
        self.store.db.close();self.store=Store(self.root/'runtime');setup(self.store)
        second=execute_batch(self.store,self.source,'furniture',25,self.cfg,self.tools,self.runner)
        self.assertEqual(second['attemptedUniqueAssets'],25)
        after={r['key'] for r in self.store.db.execute("SELECT key FROM intake WHERE status='complete'")}
        self.assertEqual(len(after-before),25)
        self.assertEqual(len(aggregate_jobs(self.store)),50)
        self.assertEqual([json.loads(x['entry'])['position'] for x in next_entries(self.store,self.source,'furniture',25)],[50,51])

    def test_allowance_positive_custom_and_all(self):
        self.assertEqual(allowance('25'),25);self.assertEqual(allowance('3'),3);self.assertIsNone(allowance('ALL'))
        for value in ('0','-1','2.5','no'):
            with self.assertRaises(ValueError):allowance(value)
        for i in range(3):self.entry(i)
        self.assertEqual(len(next_entries(self.store,self.source,'all',None)),3)

    def test_unknown_category_and_review_entries_are_finite(self):
        self.entry(0,'unknown');self.entry(1,'unknown','manual_review','Unsupported layout')
        result=execute_batch(self.store,self.source,'unknown',25,self.cfg,self.tools,self.runner)
        self.assertEqual(result['attemptedUniqueAssets'],1)
        self.assertEqual(counts(self.store,self.source,'unknown'),{'complete':1,'manual_review':1})
        with self.assertRaises(ManualReview):prompt(self.store,self.source,{'intake':{}},'nonexistent','1')

    def test_cancelled_asset_resumes_before_next_and_does_not_advance_past_it(self):
        first=self.entry(0);self.entry(1)
        def cancel(store,job,*unused):
            store.status(job,'cancelled','Fixture cooperative cancellation');return False
        r=execute_batch(self.store,self.source,'furniture',2,self.cfg,self.tools,cancel)
        self.assertTrue(r['cancelled']);self.assertEqual(r['attemptedUniqueAssets'],1)
        self.assertEqual(next_entries(self.store,self.source,'furniture',1)[0]['key'],first['key'])
        execute_batch(self.store,self.source,'furniture',1,self.cfg,self.tools,self.runner)
        self.assertEqual(json.loads(next_entries(self.store,self.source,'furniture',1)[0]['entry'])['position'],1)

    def test_keyboard_interrupt_at_claim_before_runner_can_resume(self):
        first=self.entry(0);self.entry(1)
        real_print=print
        def interrupt(*args,**kwargs):
            if args and str(args[0]).startswith('Asset '):raise KeyboardInterrupt()
            return real_print(*args,**kwargs)
        with patch('builtins.print',side_effect=interrupt):
            r=execute_batch(self.store,self.source,'furniture',2,self.cfg,self.tools,self.runner)
        self.assertTrue(r['cancelled'])
        self.assertEqual(self.store.db.execute('SELECT status FROM intake WHERE key=?',(first['key'],)).fetchone()[0],'cancelled')
        self.assertEqual(self.store.db.execute('SELECT status FROM batches').fetchone()[0],'cancelled')
        execute_batch(self.store,self.source,'furniture',1,self.cfg,self.tools,self.runner)
        self.assertEqual(counts(self.store,self.source),{'complete':1,'pending':1})

    def test_failures_are_attention_and_next_batch_does_not_retry_infinitely(self):
        self.entry(0);self.entry(1)
        def fail(store,job,*unused):
            store.status(job,'manual_review','Unsupported static fixture');return False
        r=execute_batch(self.store,self.source,'furniture',25,self.cfg,self.tools,fail)
        self.assertEqual(r['needsAttention'],2)
        self.assertEqual(next_entries(self.store,self.source,'furniture',25),[])

    def test_completion_reconciles_cross_recipe_and_stale_media_requeues(self):
        e=self.entry(0);job=self.store.enqueue(e['recipe'],0);self.runner(self.store,job,self.cfg,self.tools)
        old=json.loads(self.store.db.execute('SELECT record FROM assets').fetchone()[0]);old['description']='metadata-only test wording'
        self.store.db.execute('UPDATE assets SET record=?',(canonical(old),));self.store.db.commit()
        reconcile(self.store,self.source,self.cfg,self.tools,self.settings,lambda *_:None)
        self.assertEqual(counts(self.store,self.source),{'complete':1})
        updated=json.loads(self.store.db.execute('SELECT record FROM assets').fetchone()[0])
        self.assertEqual(updated['description'],'Clean ordinary description')
        output=json.loads(self.store.job(job)['result'])['media'][0]['file'];Path(output).write_bytes(b'corrupt')
        reconcile(self.store,self.source,self.cfg,self.tools,self.settings,lambda *_:None)
        self.assertEqual(counts(self.store,self.source),{'pending':1})
        self.assertEqual(aggregate_jobs(self.store),[])

    def test_tool_change_invalidates_completion_without_changing_source(self):
        e=self.entry(0);job=self.store.enqueue(e['recipe'],0);self.runner(self.store,job,self.cfg,self.tools)
        tools=copy.deepcopy(self.tools);tools['blender']['sha256']='changed-version'
        reconcile(self.store,self.source,self.cfg,tools,self.settings,lambda *_:None)
        self.assertEqual(counts(self.store,self.source),{'pending':1})

    def test_changed_texture_binding_never_runs_old_still_available_recipe(self):
        e=self.entry(0);old=self.store.enqueue(e['recipe'],0);self.runner(self.store,old,self.cfg,self.tools)
        changed=copy.deepcopy(e);changed['recipe']['baseTextures'][0]['dds']['sha256']='new-texture-content'
        # Defensive execution guard also protects a stale assignment from an older DB/import.
        self.store.db.execute('UPDATE intake SET entry=?,job_id=? WHERE key=?',(canonical(changed),old,e['key']));self.store.db.commit()
        seen=[]
        def inspect(store,job,*unused):
            seen.append(json.loads(store.job(job)['recipe'])['baseTextures'][0]['dds']['sha256'])
            store.status(job,'manual_review','Fixture stops before native execution');return False
        execute_batch(self.store,self.source,'furniture',1,self.cfg,self.tools,inspect)
        self.assertEqual(seen,['new-texture-content'])
        self.assertEqual(json.loads(self.store.job(old)['recipe'])['baseTextures'][0]['dds']['sha256'],e['recipe']['baseTextures'][0]['dds']['sha256'])

    def test_changed_import_signature_clears_previous_job_assignment(self):
        e=self.entry(0);old=self.store.enqueue(e['recipe'],0)
        self.store.db.execute('UPDATE intake SET job_id=? WHERE key=?',(old,e['key']))
        self.store.db.execute('INSERT INTO intake_sources VALUES(?,?,?)',(self.source,'old',1));self.store.db.commit()
        changed=copy.deepcopy(e);changed['signature']='changed';changed['recipe']['baseTextures'][0]['dds']['sha256']='different'
        sourcepath=self.root/'index.json';sourcepath.write_text('{}')
        # Keep source id deterministic exactly as import_index computes it.
        from runtime import digest
        source=digest(str(sourcepath).casefold())[:24]
        self.store.db.execute('UPDATE intake SET source_id=?',(source,));self.store.db.execute('DELETE FROM intake_sources');self.store.db.commit()
        with patch('intake.bundle_paths',return_value=(self.root,{'index':sourcepath,'materials':[],'members':[]})),patch('intake.build_entries',return_value=[changed]):
            import_index(self.store,{})
        row=self.store.db.execute('SELECT job_id,status FROM intake').fetchone()
        self.assertIsNone(row['job_id']);self.assertEqual(row['status'],'pending')

    def test_inaccessible_old_source_uses_current_recipe(self):
        e=self.entry(0);old_recipe=copy.deepcopy(e['recipe']);old_recipe['model']['file']='obsolete/missing.fmdl'
        old=self.store.enqueue(old_recipe,0);self.store.db.execute('UPDATE intake SET job_id=? WHERE key=?',(old,e['key']));self.store.db.commit()
        seen=[]
        def verify(recipe,cfg):
            if not Path(recipe['model']['file']).is_file():raise ManualReview('Moved source')
        def inspect(store,job,*unused):
            seen.append(json.loads(store.job(job)['recipe'])['model']['file'])
            store.status(job,'manual_review','Fixture stops before native execution');return False
        execute_batch(self.store,self.source,'furniture',1,self.cfg,self.tools,inspect,verify)
        self.assertEqual(seen,[e['recipe']['model']['file']])

if __name__=='__main__':
    unittest.main(verbosity=2)
