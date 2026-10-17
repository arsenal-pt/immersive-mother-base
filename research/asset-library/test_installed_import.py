import copy, hashlib, json, os, tempfile, unittest
from pathlib import Path
from PIL import Image
import installed_import as subject
import import_batch


def fixture():
    texture={'materialIndex':0,'samplerName':'Base_Tex_LIN','nativePathHash':'123','nativePath':'/Assets/tpp/texture/base.ftex','sha256':'d'*64,'familyId':'f'*64,'width':256,'height':128,'mipCount':2,'nativeMipCountVerified':True,'sourceOccurrences':[{'source':'first'}]}
    a={'id':'fixture_1','title':'native_fixture','category':'Discovered static models','description':'Selected native model component; interaction untested.','tags':['static'],'modelPath':'/Assets/tpp/model/fixture.fmdl','modelSha256':'a'*64,'containerPath':'/Assets/tpp/pack/test.fpk','containerSha256':'b'*64,'sourceEvidence':{'contentSha256':'a'*64,'source_path':'master/0/00.dat','occurrence_id':'o1'},'baseTextures':[texture],'nativeLods':[{'nativeLod':0,'triangles':3,'indicesSha256':'i'*64},{'nativeLod':1,'triangles':1,'indicesSha256':'j'*64}],'lod':0,'triangles':3,'baseTextureSummary':'256 x 128; 2 mips','upstreamPreparation':'Actual community reader/converter','still':'media/fixture.png','gif':'media/fixture-360.gif','thumbnail':'media/fixture-thumb.png'}
    r={'policy':{'renderer':'1'*64},'artifact_files':[{'file':'PRIVATE/'+Path(a[k]).name,'sha256':'e'*64,'bytes':1} for k in ['still','gif','thumbnail']]}
    return a,r


class InstalledImport(unittest.TestCase):
    def test_native_and_material_evidence_preserved_without_operational_paths(self):
        a,r=fixture();out,copies=subject.normalize(a,r,'media/asset-previews/test',verify=False)
        self.assertEqual(out['source']['evidence'],a['sourceEvidence']);self.assertEqual(out['materials'][0]['nativeBinding'],a['baseTextures'][0])
        self.assertEqual(out['materials'][0]['sampler'],'Base_Tex_LIN');self.assertTrue(out['source']['selectedInstalledMemberVerified']);self.assertFalse(out['source']['currentInstalledDatVerified'])
        self.assertEqual(out['quality']['renderedNativeLods'],[0]);self.assertEqual(len(out['quality']['nativeLods']),2)
        self.assertIn('Unknown',out['sourceNamespace']);self.assertNotIn('PRIVATE/',json.dumps(out));self.assertEqual(len(copies),3)

    def test_legacy_objects_and_different_texture_versions_survive(self):
        a,r=fixture();first,_=subject.normalize(a,r,'media/asset-previews/test',False)
        b=copy.deepcopy(a);b['id']='fixture_2';b['baseTextures'][0]['sha256']='c'*64
        second,_=subject.normalize(b,r,'media/asset-previews/test',False)
        old={'id':'old','source':{'nativeSha256':'a'*64},'custom':['keep',1]};original={'assets':[old]}
        out,aliases=subject.merge(original,[first,second]);self.assertEqual(out['assets'][0],old);self.assertEqual(original,{'assets':[old]});self.assertEqual(len(out['assets']),3);self.assertEqual(aliases,{})

    def test_exact_render_identity_dedupes_but_changed_id_conflicts(self):
        a,r=fixture();first,_=subject.normalize(a,r,'media/asset-previews/test',False);second=copy.deepcopy(first);second['id']='alias'
        out,aliases=subject.merge({'assets':[]},[first,second]);self.assertEqual(len(out['assets']),1);self.assertEqual(aliases,{'alias':'fixture_1'})
        second=copy.deepcopy(first);second['title']='changed'
        with self.assertRaises(ValueError):subject.merge({'assets':[first]},[second])

    def test_provenance_occurrences_do_not_change_render_identity(self):
        a,r=fixture();value=subject.reference_identity(a,r['policy']);b=copy.deepcopy(a);b['baseTextures'][0]['sourceOccurrences']=[{'source':'other'}]
        self.assertEqual(value,subject.reference_identity(b,r['policy']))
        for change in ['texture','lod','policy']:
            b=copy.deepcopy(a);policy=copy.deepcopy(r['policy'])
            if change=='texture':b['baseTextures'][0]['sha256']='c'*64
            elif change=='lod':b['lod']=1
            else:policy['renderer']='2'*64
            self.assertNotEqual(value,subject.reference_identity(b,policy))

    def test_unsafe_identifiers_prefixes_and_private_metadata_rejected(self):
        for change in ['id','prefix','private','hash']:
            a,r=fixture();prefix='media/asset-previews/test'
            if change=='id':a['id']='../escape'
            elif change=='prefix':prefix='media/asset-previews/../../escape'
            elif change=='private':a['sourceEvidence']['leak']='C:'+ '/Users/test/private'
            else:a['sourceEvidence']['contentSha256']='0'*64
            with self.assertRaises(ValueError):subject.normalize(a,r,prefix,False)

    def test_actual_hash_and_image_contract_are_checked(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('MGSV_LIBRARY_TEST_ROOT')) as temp:
            a,r=fixture();path=Path(temp)/'fixture.png';path.write_bytes(b'wrong');r['artifact_files'][0]['file']=str(path)
            with self.assertRaisesRegex(ValueError,'hash/size'):subject.normalize(a,r,'media/asset-previews/test')
            Image.new('RGB',(16,16)).save(path)
            with self.assertRaisesRegex(ValueError,'dimensions'):import_batch.validate_media(path,'still')


if __name__=='__main__':unittest.main()
