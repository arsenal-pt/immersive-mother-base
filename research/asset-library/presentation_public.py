"""Generate public display pages only; raw records, provenance and media stay unchanged."""
import copy, json, posixpath
from pathlib import Path
import presentation as display

ROOT = Path(__file__).resolve().parent
LEGACY_TABLES = ('seating-1.md','architecture-batch-1.md','equipment-batch-1.md','furniture-batch-1.md',
 'discovered-static-models-4b29110f-batch-1.md','discovered-static-models-4b29110f-batch-2.md','discovered-static-models-4b29110f-batch-3.md')

def relative(page, target):
    return posixpath.relpath(target,posixpath.dirname('research/asset-library/'+page))

def context(page, records, title, category=None):
    links={}
    for a in records:
        preview=a['preview'];identifier=a['id']
        links[identifier]={key:relative(page,preview[key]) for key in ('thumbnail','still','turntable')}
        links[identifier]['detail']=relative(page,'research/asset-library/assets/'+identifier+'.md')
        links[identifier]['technical']=relative(page,'research/asset-library/catalogue.json')
    out={'title':title,'library_href':relative(page,'research/asset-library/README.md'),
         'raw_href':relative(page,'research/asset-library/catalogue.json'),
         'credits_href':relative(page,'research/asset-library/sources-and-credits.md'),'links':links}
    if category:out['category_href']=relative(page,'research/asset-library/'+category)
    return out

def generated(catalogue, registry=None, include_legacy=True):
    records=catalogue['assets'];registry=registry or display.load_registry()
    if len({a['id'] for a in records})!=len(records): raise ValueError('Duplicate parent identity')
    views=[display.present(a,registry) for a in records];by_id={a['id']:a for a in records};groups={};slugs={}
    for v in views:
        key=(v['category'],v['subcategory']);name=display.slug(v['subcategory'])
        if name in slugs and slugs[name]!=key:name=display.slug(v['category'])+'-'+name
        if name in slugs and slugs[name]!=key:raise ValueError('Category slug collision')
        slugs[name]=key;groups.setdefault(key,{'slug':name,'views':[]})['views'].append(v)
    outputs={};category_pages={};categories=[]
    for key,group in sorted(groups.items()):
        items=sorted(group['views'],key=lambda v:(v['display_name'].casefold(),v['native_filename'],v['id']))
        pages=(len(items)+display.PAGE_SIZE-1)//display.PAGE_SIZE
        category_pages[key]='tables/'+group['slug']+'-1.md'
        categories.append({'category':key[0],'title':' > '.join(key),'count':len(items),'href':category_pages[key]})
        for start in range(0,len(items),display.PAGE_SIZE):
            number=start//display.PAGE_SIZE+1;page='tables/'+group['slug']+'-'+str(number)+'.md'
            ctx=context(page,records,' > '.join(key)+' - page '+str(number))
            text=display.render_table(items[start:start+display.PAGE_SIZE],ctx)
            text+='\nPages: '+' | '.join(display.link(str(n),group['slug']+'-'+str(n)+'.md') for n in range(1,pages+1))+'\n'
            outputs[page]=text
    for v in views:
        a=by_id[v['id']];page='assets/'+v['id']+'.md';category=category_pages[(v['category'],v['subcategory'])]
        ctx=context(page,records,v['display_name'],category);text=display.render_detail(v,ctx)
        q=a.get('quality') or {};variants=q.get('variants',[])
        if variants:
            text+='\n## Native LOD comparison\n\n'
            if q.get('comparisonImage'):text+='!['+display.cell(v['display_name'])+' native LOD comparison]('+display.href(relative(page,q['comparisonImage']))+')\n\n'
            text+='| Preview | Native LOD | Geometric detail | Triangles | Open |\n|---|---|---|---:|---|\n'
            for child in variants:
                lod=child['nativeLod'];target='#still-reference' if lod==v['lod'] else child['id']+'.md'
                thumb=relative(page,child['preview']['thumbnail'])
                text+='| [!['+display.cell(v['display_name'])+' LOD'+str(lod)+']('+display.href(thumb)+')]('+display.href(target)+') | LOD'+str(lod)+' | '+display.cell(child['qualityLabel'])+' | '+str(child['triangles'])+' | '+display.link('Still and 360 view',target)+' |\n'
                if lod!=v['lod']:
                    child_record=copy.deepcopy(a);child_record['id']=child['id'];child_record['preview']=copy.deepcopy(child['preview'])
                    child_view=copy.deepcopy(v);child_view.update(id=child['id'],library_id=child['id'],lod=lod,triangles=child['triangles'])
                    child_page='assets/'+child['id']+'.md';child_ctx=context(child_page,[child_record],v['display_name']+' - LOD'+str(lod),category)
                    outputs[child_page]=display.render_detail(child_view,child_ctx)+'\n'+display.link('Parent reference and LOD comparison',a['id']+'.md#native-lod-comparison')+'\n'
        outputs[page]=text
    index=display.render_index(views,categories,{'title':'MGSV asset reference library','raw_href':'catalogue.json','credits_href':'sources-and-credits.md'})
    index+='\nReadable names and descriptions are a separate display registry. Game filenames, Library IDs, genuine variants, source records and media remain unchanged. Naming review never changes processing completion.\n\n'
    index+='['+'Readable CSV](display-catalogue.csv) | [Readable JSON](display-catalogue.json) | [Naming registry](naming-registry.json) | [Refresh / labeling guide](PRESENTATION.md) | [Source records](catalogue.json) | [Source / tool credits](sources-and-credits.md) | [Workflow](workflow.md)\n\n'
    index+='## Quality and source scope\n\n'
    index+=str(len(records))+' parent references and '+str(sum(len(a.get('quality',{}).get('variants',[])) or 1 for a in records))+' rendered views. Original seating families retain their native LOD comparison pages. Other native levels are inventoried separately from rendered coverage. Model components are not asserted to be complete assembled or interactive objects.\n\n'
    index+='Exact native paths, captured container/texture chains, texture pixels/mips, hashes, provenance, Library IDs and naming evidence are in detail/technical views. Source namespaces include MGO references found in as-installed archives; vanilla-install status, exhaustive alternatives and effective runtime priority remain unresolved. Original retained-only records do not claim a current DAT check.\n\n'
    index+='Actual base textures/UVs use approximate studio shading. Normal/specular/packed FOX shaders and game collisions/interactions are not reproduced. Turntables are camera orbits around static models, not native animations.\n\n'
    index+='Konami retains rights in game artwork; only reference previews/metadata are included. Project owner: arsenal-pt. Authored preparation uses OpenAI Codex (AI/LLM). Community tool attribution remains in [central credits](sources-and-credits.md). No raw models, textures, archives, decoded geometry or Blender scenes are distributed.\n'
    outputs['README.md']=index
    for name in LEGACY_TABLES if include_legacy else ():
        page='tables/'+name
        if page not in outputs:outputs[page]='# Asset category navigation\n\nThis previous upload page has moved to the consistent category catalogue.\n\n[Browse categories](../README.md)\n'
    outputs.update(display.display_exports(sorted(views,key=lambda v:v['id'])))
    return outputs
