"""Display-only invariants: no asset/process/receipt identity may change."""
import copy, json, re, unittest
from pathlib import Path
import presentation as p
import presentation_public as public

ROOT=Path(__file__).resolve().parent

def record(identifier='one', path='/Assets/test/chair/example_vrtn002.fmdl'):
    return {'id':identifier,'title':'Raw internal stem','category':'Discovered static models','tags':['raw'],'description':'Raw.',
      'modelPath':path,'modelSha256':'a'*64,'lod':0,'triangles':10,'nativeLods':[{'nativeLod':0,'triangles':10,'indicesSha256':'b'*64}],
      'baseTextures':[],'still':'media/one.png','gif':'media/one.gif','thumbnail':'media/one-thumb.png'}

def registry():
    return {'schemaVersion':1,'overrides':{},'path_overrides':{},'rules':[]}

def context(views):
    return {'title':'Examples','library_href':'../README.md','raw_href':'../raw.json','links':{v['id']:{'thumbnail':'../media/'+v['id']+'-thumb.png','still':'../media/'+v['id']+'.png','turntable':'../media/'+v['id']+'.gif','detail':v['id']+'.md'} for v in views}}

class PresentationTests(unittest.TestCase):
    def test_exact_override_beats_path_and_family(self):
        r=registry();r['overrides']['one']={'display_name':'Reviewed exact','naming_status':'reviewed'};r['path_overrides'][record()['modelPath']]={'display_name':'Path'};r['rules']=[{'path_component':'chair','display_name':'Family'}]
        self.assertEqual(p.present(record(),r)['display_name'],'Reviewed exact')
    def test_exact_path_and_longest_rule(self):
        r=registry();r['rules']=[{'native_path_prefix':'/Assets/','display_name':'Broad'},{'native_path_prefix':'/Assets/test/','display_name':'Specific'}]
        self.assertEqual(p.present(record(),r)['display_name'],'Specific');r['path_overrides'][record()['modelPath']]={'display_name':'Exact'}
        self.assertEqual(p.present(record(),r)['display_name'],'Exact')
    def test_unknown_ignores_unreviewed_raw_title(self):
        v=p.present(record(),registry());self.assertEqual(v['display_name'],'Unidentified model (example_vrtn002)');self.assertTrue(v['metadata_review']);self.assertEqual(v['category'],'Unclassified')
    def test_variant_does_not_become_lod(self):
        a=record(path='/Assets/example_vrtn_002.fmdl');a['lod']=3;v=p.present(a,registry());self.assertEqual(v['variant'],'vrtn_002');self.assertEqual(v['lod'],3)
    def test_library_and_export_schema_agree(self):
        a=record();b=copy.deepcopy(a);b['source']={'nativePath':b.pop('modelPath'),'nativeSha256':b.pop('modelSha256')};b['geometry']={'lod':b.pop('lod'),'triangles':b.pop('triangles')}
        x,y=p.present(a,registry()),p.present(b,registry())
        for k in ('display_name','native_filename','variant','lod','triangles'):self.assertEqual(x[k],y[k])
    def test_present_is_immutable_and_idempotent(self):
        a=record();r=registry();before=json.dumps([a,r],sort_keys=True);self.assertEqual(p.present(a,r),p.present(a,r));self.assertEqual(json.dumps([a,r],sort_keys=True),before)
    def test_same_name_never_merges_ids(self):
        r=registry();r['rules']=[{'path_component':'chair','display_name':'Chair','naming_status':'path-derived'}];views=[p.present(record(x),r) for x in ('one','two')];self.assertEqual(len({v['id'] for v in views}),2);self.assertEqual({v['display_name'] for v in views},{'Chair'})
    def test_table_budget_and_static_previews(self):
        views=[p.present(record('item'+str(i)),registry()) for i in range(13)]
        with self.assertRaises(ValueError):p.render_table(views,context(views))
        text=p.render_table(views[:12],context(views));self.assertEqual(text.count('-thumb.png'),12);self.assertNotIn('.gif',text);self.assertIn('Game filename',text)
    def test_markdown_and_link_escape(self):
        r=registry();r['overrides']['one']={'display_name':'x](javascript:evil)|<script>','description':'[bad](javascript:bad)','tags':['x|y']}
        v=p.present(record(),r);text=p.render_table([v],context([v]));self.assertNotIn('<script>',text);self.assertNotIn('](javascript:',text);self.assertIn('&#124;',text)
        for link in ('javascript:bad','file:///C:/private','//server/a','a\\b'):
            with self.assertRaises(ValueError):p.href(link)
    def test_index_is_image_free(self):
        v=p.present(record(),registry());text=p.render_index([v],[{'category':'Furniture','href':'table-1.md','count':1}],context([v]));self.assertNotIn('![',text)
    def test_existing_ten_reviewed_labels_preserved(self):
        data=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'));r=p.load_registry()
        for a in data['assets'][:10]:
            v=p.present(a,r)
            for display,raw in [('display_name','title'),('category','category'),('subcategory','subcategory'),('description','description'),('tags','tags')]:self.assertEqual(v[display],a[raw])
    def test_all_forty_public_views_immutable_and_idempotent(self):
        data=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'));before=json.dumps(data,sort_keys=True);a=public.generated(data);self.assertEqual(a,public.generated(data));self.assertEqual(json.dumps(data,sort_keys=True),before);self.assertEqual(len([x for x in a if x.startswith('assets/')]),49)
    def test_all_legacy_table_and_lod_links_preserved(self):
        data=json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8'));pages=public.generated(data)
        for name in public.LEGACY_TABLES:self.assertIn('tables/'+name,pages)
        for asset in data['assets'][:3]:
            self.assertIn('## Native LOD comparison',pages['assets/'+asset['id']+'.md'])
            for v in asset['quality']['variants'][1:]:self.assertIn('assets/'+v['id']+'.md',pages)
    def test_readable_exports_separate_from_raw(self):
        pages=public.generated(json.loads((ROOT/'catalogue.json').read_text(encoding='utf-8')))
        self.assertIn('display-catalogue.csv',pages);self.assertIn('display-catalogue.json',pages);self.assertNotIn('catalogue.json',pages);self.assertNotIn('catalogue.csv',pages);self.assertNotIn('completion-proofs.json',pages)
    def test_future_folder_rule_honest_and_uncertain_fallback(self):
        r=p.load_registry();v=p.present(record('new','/Assets/new/light/new.fmdl'),r);self.assertEqual(v['display_name'],'Light component');self.assertEqual(v['naming_status'],'path-derived')
        self.assertEqual(p.present(record('new','/Assets/new/clod/new.fmdl'),r)['naming_status'],'unidentified')

if __name__=='__main__':unittest.main()
