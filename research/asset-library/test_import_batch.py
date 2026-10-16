"""Focused guards for the portable export/public-library seam."""
import copy
import json
from PIL import Image
import tempfile
import unittest
from pathlib import Path
import import_batch

class ImportTests(unittest.TestCase):
 def record(self):
  return {'id':'sample','source':{'nativeSha256':'a'*64},'title':'Sample'}
 def test_idempotent_merge_preserves_accepted_record(self):
  old={'assets':[self.record()]};result=import_batch.merge(old,[copy.deepcopy(old['assets'][0])]);self.assertEqual(result,old);self.assertIsNot(result,old)
 def test_identity_or_payload_conflict_rejected(self):
  old={'assets':[self.record()]};changed=self.record();changed['title']='Changed'
  with self.assertRaises(ValueError):import_batch.merge(old,[changed])
  changed=self.record();changed['id']='alias'
  with self.assertRaises(ValueError):import_batch.merge(old,[changed])
 def test_escaped_or_machine_path_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   for rel in ['../raw.fmdl','C:/private/model.png','/private/model.png',r'\\server\share\model.png']:
    with self.assertRaises(ValueError):import_batch.safe_path(Path(folder),rel)
  with self.assertRaises(ValueError):import_batch.portable({'source':'Z:/private/example.fmdl'})
 def test_table_pages_are_bounded_and_still_only(self):
  a={'id':'sample','title':'Sample','category':'Architecture','subcategory':'Components','tags':['panel'],'description':'A panel.','source':{'nativePath':'/Assets/test.fmdl','container':{'nativePath':'/Assets/test.fpk','sha256':'b'*64},'nativeSha256':'a'*64,'locationStatus':'Retained'},'geometry':{'lod':0,'triangles':2},'quality':{'nativeLods':[{'nativeLod':0,'triangles':2,'indicesSha256':'c'*64}],'renderedNativeLods':[0],'baseTextureSummary':'1 x 1; 1 mip'},'preview':{'thumbnail':'media/a-thumb.png','still':'media/a.png','turntable':'media/a.gif'},'batchImport':{'upstreamPreparation':'Retained'},'materials':[]}
  records=[]
  for n in range(25):
   b=copy.deepcopy(a);b['id']='sample'+str(n);records.append(b)
  out=import_batch.generated(records);tables={k:v for k,v in out.items() if k.startswith('tables/')}
  self.assertEqual(len(tables),3)
  for value in tables.values():self.assertLessEqual(value.count('-thumb.png'),12);self.assertNotIn('.gif',value)

class GenericExportTests(unittest.TestCase):
 def fixture(self, folder):
  root=Path(folder);(root/'media').mkdir()
  Image.new('RGB',(768,768),'gray').save(root/'media/sample.png')
  Image.new('RGB',(160,160),'gray').save(root/'media/sample-thumb.png')
  frames=[Image.new('RGB',(480,480),(n*5,100,200)) for n in range(48)]
  frames[0].save(root/'media/sample.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False,disposal=2)
  asset={'id':'unknown-static_01','modelPath':'/Assets/tpp/chara/example/scenes/example_static.fmdl','modelSha256':'a'*64,'containerPath':'/Assets/tpp/pack/example.fpk','containerSha256':'b'*64,'title':'Unknown <model>','category':'Custom / [components] ..','tags':['prop','panel'],'description':'A static [test] model.','still':'media/sample.png','gif':'media/sample.gif','thumbnail':'media/sample-thumb.png','baseTextures':[{'materialIndex':0,'nativePathHash':'123','sha256':'c'*64,'width':32,'height':32,'mipCount':1,'nativeMipCountVerified':False}],'nativeLods':[{'nativeLod':0,'triangles':1,'indicesSha256':'d'*64}],'lod':0,'triangles':1,'baseTextureSummary':'32 x 32; 1 DDS mip','upstreamPreparation':'Native selected-job export; no retained-specific evidence supplied'}
  self.write(root,asset);return root,asset
 def write(self,root,asset):
  (root/'catalogue.json').write_text(json.dumps({'assets':[asset]}),encoding='utf-8')
  files=[]
  for p in [root/'catalogue.json',*sorted((root/'media').iterdir())]:
   data=p.read_bytes();files.append({'path':p.relative_to(root).as_posix(),'sha256':import_batch.sha(data),'bytes':len(data)})
  (root/'manifest.json').write_text(json.dumps({'files':files}),encoding='utf-8')
 def test_unknown_non_object_export_and_sampler_fallback(self):
  with tempfile.TemporaryDirectory() as folder:
   root,asset=self.fixture(folder)
   records,copies=import_batch.prepare(root,[asset['id']],'media/asset-previews/test')
   a=records[0];self.assertEqual(a['title'],'Unknown model');self.assertEqual(a['description'],'A static test model.');self.assertIn('Unknown',a['sourceNamespace']);self.assertEqual(a['source']['nativePath'],asset['modelPath']);self.assertIn('not independently verified',a['source']['locationStatus']);self.assertIn('Unknown sampler name',a['materials'][0]['sampler'])
   self.assertRegex(import_batch.table_slug(a['category']),r'^[a-z0-9-]+$');self.assertNotEqual(import_batch.table_slug('A/B'),import_batch.table_slug('A B'))
   asset['baseTextures'][0]['samplerName']='Base_Tex_LIN';self.write(root,asset)
   result,_=import_batch.prepare(root,[asset['id']],'media/asset-previews/test');self.assertEqual(result[0]['materials'][0]['sampler'],'Base_Tex_LIN')
 def test_unsafe_id_and_private_path_variants(self):
  with tempfile.TemporaryDirectory() as folder:
   root,asset=self.fixture(folder);asset['id']='../../escape';self.write(root,asset)
   with self.assertRaisesRegex(ValueError,'Unsafe portable asset ID'):import_batch.prepare(root,[asset['id']],'media/asset-previews/test')
  for value in [r'\\server\share\asset.fmdl','//server/share/asset.fmdl','/home/user/asset.fmdl','/Users/sample/asset.fmdl','Z:/private/asset.fmdl']:
   with self.assertRaises(ValueError):import_batch.portable({'value':value})
  import_batch.portable({'value':'/Assets/tpp/environ/home/model.fmdl'})
 def test_media_contract_and_hash_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   root,asset=self.fixture(folder);Image.new('RGB',(32,32),'white').save(root/'media/sample-thumb.png');self.write(root,asset)
   with self.assertRaisesRegex(ValueError,'dimensions differ'):import_batch.prepare(root,[asset['id']],'media/asset-previews/test')
   (root/'media/sample-thumb.png').write_bytes(b'changed')
   with self.assertRaisesRegex(ValueError,'Media hash mismatch'):import_batch.prepare(root,[asset['id']],'media/asset-previews/test')

if __name__=='__main__':unittest.main()
