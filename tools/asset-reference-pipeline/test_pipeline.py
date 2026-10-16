"""Focused contracts with real tiny child processes; no game assets required."""
import copy
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from runtime import ManualReview, Store, WorkerLock, digest, load, save, sha
from native import bind_materials
from catalogue import export_catalogue, public_scan

HERE = Path(__file__).resolve().parent
FLAGS = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='mgsv-pipeline-tests-')
        self.root = Path(self.tmp.name)
        self.store = Store(self.root/'runtime')

    def tearDown(self):
        self.store.db.close()
        self.tmp.cleanup()

    def test_metadata_does_not_change_job_identity(self):
        a = {'id':'prop','title':'Old','description':'Old','tags':['chair'],'category':'Seating','model':{'sha256':'x'}}
        key = self.store.enqueue(a,0)
        b = {**a,'title':'Clearer title','description':'Plain words','tags':['folding'],'category':'Furniture'}
        self.assertEqual(key,self.store.enqueue(b,0))
        self.assertEqual(json.loads(self.store.job(key)['recipe'])['title'],'Clearer title')
        self.store.status(key,'complete')
        self.store.enqueue(b,0)
        self.assertEqual(self.store.job(key)['status'],'queued')
        self.store.status(key,'running')
        with self.assertRaises(ManualReview):
            self.store.enqueue(b,0)

    def test_cache_validation_corrupt_receipt_and_output_rebuild(self):
        key = self.store.enqueue({'id':'fixture'},0)
        calls = []
        def stage(out):
            calls.append(1)
            (out/'result.txt').write_text('valid')
            return {'ok':True}
        folder,_ = self.store.stage(key,'fixture','abc',stage)
        self.store.stage(key,'fixture','abc',stage)
        self.assertEqual(len(calls),1)
        (folder/'stage.json').write_text('{truncated')
        self.store.stage(key,'fixture','abc',stage)
        self.assertEqual(len(calls),2)
        (folder/'result.txt').write_text('corrupt')
        self.store.stage(key,'fixture','abc',stage)
        self.assertEqual(len(calls),3)
        self.assertEqual(len(list(folder.parent.glob('abc-incomplete-*'))),2)

    def test_failed_process_never_gets_complete_receipt_then_resumes(self):
        key = self.store.enqueue({'id':'fixture'},0)
        def fail(out):
            self.store.process(key,'test',[sys.executable,'-c','import sys;sys.exit(7)'],out,10)
        with self.assertRaisesRegex(RuntimeError,'exited 7'):
            self.store.stage(key,'process','failure',fail)
        folder = self.store.root/'cache/process/failure'
        self.assertFalse((folder/'stage.json').exists())
        self.assertEqual(self.store.db.execute("SELECT status FROM stages WHERE name='process'").fetchone()[0],'failed')
        def succeed(out):
            self.store.process(key,'test',[sys.executable,'-c',"open('ok.txt','w').write('done')"],out,10)
            return {'ok':True}
        self.store.stage(key,'process','failure',succeed)
        self.assertTrue((folder/'stage.json').exists())

    def test_real_process_cancel_via_cli_and_restart_reuses_completed_stage(self):
        recipe = {'id':'fixture'}
        key = self.store.enqueue(recipe,0)
        cfg = {'runtime':str(self.store.root),'sourceRoots':[str(self.root/'sources')]}
        save(self.root/'config.json',cfg)
        worker = self.root/'worker.py'
        worker.write_text(
            "import sys,time\nfrom pathlib import Path\n"
            f"sys.path.insert(0,{str(HERE)!r})\n"
            "from runtime import Store,WorkerLock,Cancelled\n"
            f"s=Store({str(self.store.root)!r});key={key!r}\n"
            "def first(out):\n (out/'first.txt').write_text('complete');return {'ok':True}\n"
            "def second(out):\n"
            " s.process(key,'sleeper',[sys.executable,'-c',"
            "\"import time;from pathlib import Path;Path('started').write_text('yes');time.sleep(\"+sys.argv[1]+\");Path('finished').write_text('yes')\"],out,20)\n"
            " return {'ok':True}\n"
            "with WorkerLock(s.root):\n"
            " try:\n"
            "  s.stage(key,'first','one',first)\n"
            "  s.stage(key,'second','two',second)\n"
            "  s.status(key,'complete')\n"
            " except Cancelled:\n  s.status(key,'cancelled')\n",encoding='utf-8')
        log = (self.root/'worker.log').open('wb')
        child = subprocess.Popen([sys.executable,str(worker),'15'],stdout=log,stderr=subprocess.STDOUT,creationflags=FLAGS)
        try:
            start = time.monotonic()
            while not list(self.store.root.glob('cache/second/two/started')):
                if child.poll() is not None:
                    self.fail('Synthetic worker stopped: '+(self.root/'worker.log').read_text())
                if time.monotonic()-start > 10:
                    self.fail('Synthetic child did not start')
                time.sleep(.1)
            p = subprocess.run([sys.executable,str(HERE/'pipeline.py'),'--config',str(self.root/'config.json'),
                                'cancel','--job',key],capture_output=True,text=True,creationflags=FLAGS,timeout=15)
            self.assertEqual(p.returncode,0,p.stderr)
            child.wait(timeout=10)
        finally:
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=5)
            log.close()
        self.assertEqual(self.store.job(key)['status'],'cancelled')
        self.assertEqual(self.store.db.execute("SELECT status FROM stages WHERE name='second'").fetchone()[0],'cancelled')
        self.assertFalse((self.store.root/'cache/second/two/finished').exists())
        self.assertFalse((self.store.root/'cache/second/two/stage.json').exists())
        self.store.enqueue(recipe,0)  # Normal queue update clears the cancellation flag.
        p = subprocess.run([sys.executable,str(worker),'0'],capture_output=True,text=True,creationflags=FLAGS,timeout=15)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(self.store.job(key)['status'],'complete')
        first = self.store.db.execute("SELECT kind FROM events WHERE stage='first' ORDER BY sequence").fetchall()
        self.assertEqual([r[0] for r in first],['started','complete','cache_hit'])
        self.assertTrue((self.store.root/'cache/second/two/finished').exists())

    def test_short_cache_key_collision_blocks_wrong_reuse(self):
        key=self.store.enqueue({'id':'fixture'},0)
        def stage(out):
            (out/'ok').write_text('ok');return {'ok':True}
        self.store.stage(key,'fixture','a'*16+'1111',stage)
        with self.assertRaisesRegex(ManualReview,'collision'):
            self.store.stage(key,'fixture','a'*16+'2222',stage)

    def test_timeout_terminates_owned_child_and_marks_stage_failed(self):
        key=self.store.enqueue({'id':'fixture'},0)
        def stage(out):
            self.store.process(key,'timeout',[sys.executable,'-c','import time;time.sleep(10)'],out,.1)
        with self.assertRaises(TimeoutError):
            self.store.stage(key,'fixture','timeout',stage)
        self.assertEqual(self.store.db.execute("SELECT status FROM stages WHERE name='fixture'").fetchone()[0],'failed')

    def test_worker_lock_refuses_second_owner(self):
        with WorkerLock(self.store.root):
            with self.assertRaises(ManualReview):
                with WorkerLock(self.store.root):
                    pass

    def test_named_sampler_mismatch_with_absent_hashes_is_rejected(self):
        data={'materials':[{'textures':[{'pathHash':123,'samplerName':'NormalMap_Tex_NRM'}]}],'sha256':'abc','shaderRecords':[]}
        recipe={'model':{'virtualPath':'/Assets/prop.fmdl'},'baseTextures':[
            {'materialIndex':0,'samplerName':'Base_Tex_SRGB','nativePathHash':'123'}]}
        with self.assertRaises(ManualReview):
            bind_materials(data,recipe,{'0':{'file':'ignored','sha256':'ignored'}})

    def test_string_material_path_is_explicit_manual_review(self):
        data={'materials':[{'textures':[]}],'sha256':'abc','shaderRecords':[]}
        recipe={'model':{'virtualPath':'/Assets/prop.fmdl'},'baseTextures':[
            {'materialIndex':0,'samplerName':'Base_Tex_SRGB','nativePathHash':'/Assets/texture.ftex'}]}
        with self.assertRaisesRegex(ManualReview,'String-path'):
            bind_materials(data,recipe,{})

    def test_public_scan_rejects_private_paths(self):
        for value in ('C:'+'/Users/me/game/file.fmdl',r'E:\Game\asset.ftex','/home/user/private/config.json'):
            with self.assertRaises(ManualReview):
                public_scan({'description':value})
        public_scan({'modelPath':'/Assets/tpp/prop.fmdl'})

    def test_export_uses_fresh_public_schema_and_distinct_lod_ids(self):
        jobs=[]
        for lod in (0,1):
            key=self.store.enqueue({'id':'prop','lod':lod},lod)
            ident='prop' if lod==0 else 'prop-lod1'
            record={'id':ident,'title':'Reference','description':'Textured prop','category':'Furniture','tags':['chair'],
                    'modelPath':'/Assets/prop.fmdl','modelSha256':'a'*64,'containerPath':'/Assets/test.fpk',
                    'containerSha256':'b'*64,'lod':lod,'triangles':12-lod,
                    'baseTextureSummary':'8x8; 1 mip','baseTextures':[{'materialIndex':0,'nativePathHash':'123','width':8,'height':8,'mipCount':1,'sha256':'c'*64}],'nativeLods':[],
                    'still':'media/'+ident+'.png','gif':'media/'+ident+'-360.gif','thumbnail':'media/'+ident+'-thumb.png'}
            media=self.store.root/'synthetic-media';media.mkdir(exist_ok=True)
            from PIL import Image
            outputs=[]
            for name in (ident+'.png',ident+'-360.gif',ident+'-thumb.png'):
                p=media/name;Image.new('RGB',(8,8),'white').save(p)
                outputs.append({'file':str(p),'sha256':sha(p)})
            self.store.db.execute('INSERT INTO assets VALUES(?,?)',(key,json.dumps(record)))
            self.store.status(key,'complete',result={'media':outputs})
            jobs.append(key)
        out=self.root/'export'
        export_catalogue(self.store,out,jobs)
        db=sqlite3.connect(out/'catalog.sqlite')
        self.assertEqual({r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")},
                         {'assets','lods','textures'})
        self.assertEqual(db.execute('SELECT COUNT(*) FROM assets').fetchone()[0],2)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM textures').fetchone()[0],2)
        db.close()
        self.assertNotIn('![',(out/'README.md').read_text())
        self.assertNotIn('.gif',(out/'table-1.md').read_text())
        self.assertEqual(len(list((out/'media').glob('*'))),6)
        with self.assertRaises(ManualReview):
            export_catalogue(self.store,self.root/'another',[jobs[0],jobs[0]])


if __name__ == '__main__':
    unittest.main(verbosity=2)
