"""Selected static asset pipeline: local processes only; no AI/MCP/network dependency."""
import argparse
import copy
import ctypes
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import time
import uuid
import zlib

from runtime import (Cancelled, ManualReview, Store, WorkerLock, canonical, digest, inside,
                     load, save, sha, tool_info)
from native import bind_materials, inspect_model
from catalogue import export_catalogue

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent.parent
HELPERS = PUBLIC / 'research/asset-library'
SETTINGS = {'stillSize':768,'gifSize':480,'frameCount':48,'frameDelayMs':100,
            'background':'neutral-light','thumbnailSize':160,'nativeRenderingEquivalent':False}


def config_load(path):
    cfg = load(path)
    cfg['runtime'] = os.path.expandvars(cfg.get('runtime', '%LOCALAPPDATA%/MGSV-Asset-Reference'))
    runtime = Path(cfg['runtime']).resolve()
    roots = [Path(os.path.expandvars(x)).resolve() for x in cfg['sourceRoots']]
    if not roots:
        raise ManualReview('Configure explicit read-only sourceRoots')
    if inside(runtime, PUBLIC) or any(inside(runtime, r) or inside(r, runtime) for r in roots):
        raise ManualReview('Private runtime must be outside source roots and public checkout')
    if os.name == 'nt':
        if ctypes.windll.kernel32.GetDriveTypeW(runtime.anchor) != 3:
            raise ManualReview('Use a local fixed disk for SQLite/cache, not a network/removable drive')
    cfg['runtime'], cfg['sourceRoots'] = str(runtime), list(map(str, roots))
    export = Path(os.path.expandvars(cfg.get('exportRoot', '%LOCALAPPDATA%/MGSV-Asset-Reference-Exports'))).resolve()
    if inside(export,PUBLIC) or inside(export,runtime) or inside(runtime,export) or any(inside(export,r) or inside(r,export) for r in roots):
        raise ManualReview('Export root must be outside public checkout, private runtime and source roots')
    cfg['exportRoot'] = str(export)
    return cfg


def source_inputs(recipe):
    model = recipe['model']
    values = [model['container']] if recipe['adapter'] == 'known-static-native' else [model]
    if recipe['adapter'] == 'prepared':
        values += [recipe['prepared']['cache'], recipe['prepared']['lodCache']]
    for t in recipe['baseTextures']:
        values += [t['ftex'], *t['sidecars']] if recipe['adapter'] == 'known-static-native' else [t['dds']]
        if t.get('ftexHeader'):
            values.append(t['ftexHeader'])
    return values


def verify_inputs(recipe, cfg):
    result = []
    for item in source_inputs(recipe):
        p = Path(item['file']).resolve()
        if not any(inside(p, r) for r in cfg['sourceRoots']):
            raise ManualReview('Source is outside configured read-only source roots: ' + str(p))
        if not p.is_file():
            raise ManualReview('Required source is missing: ' + str(p))
        if sha(p) != item['sha256']:
            raise ManualReview('Pinned source SHA256 differs: ' + str(p))
        result.append({'file':str(p),'sha256':item['sha256'],'bytes':p.stat().st_size})
    return result


def validate_recipe(r):
    if r.get('adapter') not in ('known-static-native', 'prepared', 'retained-static'):
        raise ManualReview('Unsupported adapter; Unity/FOVA/GUI/animation steps require manual preparation')
    if not r.get('staticOnly'):
        raise ManualReview('Recipe must explicitly select a known static prop; no character assembly')
    for key in ('id','stem'):
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', r[key]):
            raise ManualReview('Use safe portable id/stem identifiers')
    if not r['model']['virtualPath'].startswith('/Assets/') or '..' in r['model']['virtualPath'].split('/'):
        raise ManualReview('Preserve the exact recorded /Assets virtual model path')
    if not r.get('baseTextures'):
        raise ManualReview('Explicit reviewed native material/base texture bindings are required')
    if r['adapter'] == 'known-static-native':
        member = Path(r['model']['member'])
        if member.is_absolute() or '..' in member.parts or member.as_posix() != r['model']['virtualPath'].lstrip('/'):
            raise ManualReview('FPK member must exactly match virtual model path')
    if any(type(v) is not int or v < 0 for v in r['lods']):
        raise ManualReview('Explicit nonnegative native LOD indices are required')


def fingerprints(cfg):
    tools = {}
    for name in ('python','blender','gzs','ftex'):
        spec = cfg['tools'].get(name)
        if not spec:
            continue
        info = tool_info(spec['path'])
        if spec.get('sha256') and spec['sha256'] != info['sha256']:
            raise ManualReview('Configured tool pin differs: ' + name)
        tools[name] = info
    for name in ('render-preview.py','encode-previews.py'):
        tools[name] = tool_info(HELPERS / name)
    for name in ('FmdlReader.py','Native-Materials.py'):
        tools[name] = tool_info(HERE / 'decoder' / name)
    tools['native.py'] = tool_info(HERE / 'native.py')
    # Query the configured interpreter, not whichever Python happens to run this CLI.
    if 'python' in tools:
        flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        p = subprocess.run([tools['python']['path'],'-c',
                            'import sys,PIL,json;print(json.dumps({"python":sys.version,"pillow":PIL.__version__}))'],
                           capture_output=True,text=True,timeout=15,creationflags=flags)
        if p.returncode:
            raise ManualReview('Configured Python must have Pillow installed; no automatic install')
        tools['python']['runtime'] = json.loads(p.stdout)
    return tools


def identity(info):
    return {k:v for k,v in info.items() if k != 'path'}


def legacy_path(path):
    # Gzs/Ftex are legacy .NET tools. Use an existing NTFS alias when available.
    # Both spellings address the same staged copy; never create drive mappings.
    path = Path(path).resolve()
    if os.name == 'nt':
        buffer = ctypes.create_unicode_buffer(32768)
        target = path.parent if path.is_file() else path
        if ctypes.windll.kernel32.GetShortPathNameW(str(target), buffer, len(buffer)):
            return str(Path(buffer.value) / path.name) if path.is_file() else buffer.value
    return str(path)


def file_stage(store, job, recipe, tools):
    model = recipe['model']
    if recipe['adapter'] in ('prepared','retained-static'):
        return Path(model['file']).resolve()
    if 'gzs' not in tools:
        raise ManualReview('GzsTool is not configured for native FPK staging')
    container = model['container']
    key = digest({'container':container['sha256'],'member':model['member'],
                  'gzs':identity(tools['gzs']),'adapterVersion':1})

    def execute(out):
        p = out / Path(container['file']).name
        if p.suffix.lower() != '.fpk':
            raise ManualReview('First slice supports selected FPK inputs, not arbitrary DAT/PFTXS discovery')
        shutil.copyfile(container['file'], p)
        store.process(job,'gzs',[tools['gzs']['path'],legacy_path(p)],out)
        extracted = out / (p.stem + '_fpk') / model['member']
        if not inside(extracted, out) or not extracted.is_file() or sha(extracted) != model['sha256']:
            raise ManualReview('GzsTool output missing or selected member hash differs')
        return {'model':extracted.relative_to(out).as_posix()}
    folder, result = store.stage(job,'extract',key,execute)
    return folder / result['model']


def texture_stage(store, job, recipe, tools):
    textures = {}
    for binding in recipe['baseTextures']:
        index = str(binding['materialIndex'])
        if index in textures:
            raise ManualReview('Ambiguous duplicate material/base binding')
        if recipe['adapter'] in ('prepared','retained-static'):
            p = Path(binding['dds']['file']).resolve()
        else:
            if 'ftex' not in tools:
                raise ManualReview('FtexTool is not configured for selected FTEX family')
            ftex, sidecars = binding['ftex'], binding['sidecars']
            source = Path(ftex['file'])
            expected_names = {Path(x['file']).name for x in sidecars}
            actual_names = {p.name for p in source.parent.glob(source.stem + '.*.ftexs')}
            if expected_names != actual_names:
                raise ManualReview('Explicit FTEX sidecar family differs; review recipe instead of dropping mips')
            key = digest({'ftex':ftex['sha256'],'sidecars':sorted(x['sha256'] for x in sidecars),
                          'dds':binding['ddsSha256'],'tool':identity(tools['ftex']),'adapterVersion':1})

            def execute(out):
                family = out / 'family'
                family.mkdir()
                for item in [ftex,*sidecars]:
                    shutil.copyfile(item['file'],family / Path(item['file']).name)
                store.process(job,'ftex',[tools['ftex']['path'],legacy_path(family)],out)
                output = family / (source.stem + '.dds')
                if not output.is_file() or sha(output) != binding['ddsSha256']:
                    raise ManualReview('FtexTool DDS missing or differs from reviewed expected texture')
                return {'dds':output.relative_to(out).as_posix()}
            folder, result = store.stage(job,'texture-'+index,key,execute)
            p = folder / result['dds']
        b = p.read_bytes()
        if b[:4] != b'DDS ':
            raise ManualReview('Expected real DDS texture')
        height, width = struct.unpack_from('<II',b,12)
        mips = struct.unpack_from('<I',b,28)[0]
        native_mips_verified = False
        header = binding.get('ftexHeader') or (binding['ftex'] if recipe['adapter']=='known-static-native' else None)
        if header:
            fb = Path(header['file']).read_bytes()
            if fb[:4] != b'FTEX' or struct.unpack_from('<HH',fb,10) != (width,height) or fb[16] != mips:
                raise ManualReview('Native FTEX/DDS pixel or mip dimensions differ')
            native_mips_verified = True
        textures[index] = {'file':str(p),'sha256':sha(p),'width':width,'height':height,'mipCount':mips,
                           'materialIndex':int(index),'nativePathHash':str(binding['nativePathHash']),
                           'nativeMipCountVerified':native_mips_verified}
    return textures


def run_job(store, job, cfg, tools):
    row = store.job(job)
    r, lod = json.loads(row['recipe']),row['lod']
    store.status(job,'running')
    try:
        validate_recipe(r)
        inputs = verify_inputs(r,cfg)
        model = file_stage(store,job,r,tools)
        if sha(model) != r['model']['sha256']:
            raise ManualReview('Selected native model identity differs')
        textures = texture_stage(store,job,r,tools)
        decoder_key = digest({'model':r['model']['sha256'],'reader':identity(tools['FmdlReader.py']),
                              'materials':identity(tools['Native-Materials.py']),'lodAudit':identity(tools['native.py']),
                              'prepared':r.get('prepared')})

        def decode(out):
            data, quality = inspect_model(model,out,r.get('prepared'))
            unique = {}
            for q in quality:
                if q['indicesSha256'] in unique:
                    q['duplicateOf'] = unique[q['indicesSha256']]
                else:
                    unique[q['indicesSha256']] = q['nativeLod']
            return {'quality':quality,'bounds':data['bounds'],'sha256':data['sha256']}
        decoded, native = store.stage(job,'inspect',decoder_key,decode)
        if lod not in [q['nativeLod'] for q in native['quality']]:
            raise ManualReview('Requested native LOD is absent; no generated fallback')
        data = json.loads(zlib.decompress((decoded/'model.json.z').read_bytes()))
        materials = bind_materials(data,r,textures)
        if 'blender' not in tools or 'python' not in tools:
            raise ManualReview('Configure installed Blender and Python/Pillow')
        variant = r['id'] if lod == 0 else r['id'] + '-lod' + str(lod)
        render_key = digest({'decoder':decoder_key,'materials':materials,'lod':lod,'settings':SETTINGS,
                             'blender':identity(tools['blender']),'renderer':identity(tools['render-preview.py'])})

        def render(out):
            entry = {'id':r['id'],'stem':r['stem'],'asset':{'raw':str(model),'sha256':r['model']['sha256'],
                     'nativeFmdlPath':r['model']['virtualPath'],'cache':str(decoded/'model.json.z'),
                     'lodFacesCache':str(decoded/'lods.json.z'),'bounds':native['bounds']},'material':materials}
            config = {'sourceRoot':str(out),'outputRoot':str(out/'renders'),'assets':[entry],'settings':SETTINGS}
            save(out/'render-config.json',config)
            log = store.process(job,'blender',[tools['blender']['path'],'--background','--factory-startup',
                                '--disable-autoexec','--threads','2','--python',tools['render-preview.py']['path'],
                                '--','--config',out/'render-config.json','--asset',r['stem'],'--lod',str(lod),'--full'],out)
            if 'ASSET_REFERENCE_COMPLETE '+variant not in log.read_text(encoding='utf-8',errors='replace'):
                raise RuntimeError('Blender did not confirm completion (exit zero alone is insufficient)')
            receipt = load(out/'renders'/variant/'render-receipt.json')
            if len(receipt['images']) != 49 or receipt['selectedNativeLod'] != lod:
                raise RuntimeError('Incomplete production render receipt')
            for image in receipt['images']:
                p = out/'renders'/variant/image['file']
                if not inside(p,out) or sha(p) != image['sha256']:
                    raise RuntimeError('Render receipt hash differs')
            return {'variant':variant,'renderRoot':'renders','entry':entry}
        rendered, result = store.stage(job,'render',render_key,render)
        encode_key = digest({'render':render_key,'encoder':identity(tools['encode-previews.py']),
                             'python':identity(tools['python']),'format':'48x480-100ms-loop0-v1'})

        def encode(out):
            entry = copy.deepcopy(result['entry'])
            entry['id'] = variant  # unchanged encoder expects its output directory identity.
            config = {'outputRoot':str(rendered/result['renderRoot']),'assets':[entry]}
            save(out/'encode-config.json',config)
            store.process(job,'encode',[tools['python']['path'],tools['encode-previews.py']['path'],
                                        '--config',out/'encode-config.json','--media-output',out/'media'],out)
            from PIL import Image
            gif = out/'media'/(variant+'-360.gif')
            with Image.open(gif) as im:
                if im.n_frames != 48 or im.size != (480,480) or im.info.get('loop') != 0:
                    raise RuntimeError('GIF output contract differs')
                for frame in range(48):
                    im.seek(frame)
                    if im.info.get('duration') != 100:
                        raise RuntimeError('GIF timing differs')
            for name,size in [(variant+'.png',(768,768)),(variant+'-thumb.png',(160,160))]:
                with Image.open(out/'media'/name) as im:
                    if im.size != size:
                        raise RuntimeError('Still/thumbnail dimensions differ')
            return {'media':[{'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size}
                             for p in sorted((out/'media').iterdir())]}
        encoded, output = store.stage(job,'encode',encode_key,encode)
        # Recheck original sources after subprocesses; all tools received staged copies only.
        if inputs != verify_inputs(r,cfg):
            raise ManualReview('Original sources changed during job')
        selected = next(q for q in native['quality'] if q['nativeLod'] == lod)
        public_textures = [{k:v for k,v in t.items() if k != 'file'} for t in textures.values()]
        record = {'id':variant,'sourceAssetId':r['id'],'title':r['title'],'description':r['description'],
                  'category':r['category'],'tags':r['tags'],'modelPath':r['model']['virtualPath'],
                  'modelSha256':r['model']['sha256'],'containerPath':r['model'].get('container',{}).get('virtualPath'),
                  'containerSha256':r['model'].get('container',{}).get('sha256'),'lod':lod,
                  'triangles':selected['triangles'],'nativeLods':native['quality'],'baseTextures':public_textures,
                  'baseTextureSummary':'; '.join(f"{t['width']} x {t['height']}; {t['mipCount']} "+('native/DDS mips' if t.get('nativeMipCountVerified') else 'DDS mips (native header not rechecked)') for t in public_textures),
                  'still':'media/'+variant+'.png','gif':'media/'+variant+'-360.gif','thumbnail':'media/'+variant+'-thumb.png',
                  'sourceScope':'Explicit selected retained recipe, not a whole-game variant inventory',
                  'sourceEvidence':r.get('sourceEvidence'),
                  'upstreamPreparation':('Actual GzsTool/FtexTool staged-copy invocation' if r['adapter']=='known-static-native' else 'Retained pre-extracted native FMDL/converted DDS; no converter invoked by this job'),
                  'nativeShaderEquivalent':False,'rotation':'Camera orbit; static native geometry, not animation',
                  'tools':{name:{k:v for k,v in tools[name].items() if k != 'path'} for name in tools}}
        store.db.execute('INSERT OR REPLACE INTO assets VALUES(?,?)',(job,canonical(record)))
        final = {'media':[{'file':str(encoded/'media'/m['name']),**m} for m in output['media']],
                 'originalInputs':inputs,'renderFingerprint':render_key}
        store.status(job,'complete',result=final)
        store.event(job,'job','complete')
        return True
    except (Cancelled,KeyboardInterrupt) as ex:
        store.status(job,'cancelled',str(ex))
        store.event(job,'job','cancelled')
    except ManualReview as ex:
        store.status(job,'manual_review',str(ex))
        store.event(job,'job','manual_review',str(ex))
    except Exception as ex:
        store.status(job,'failed',str(ex))
        store.event(job,'job','failed',str(ex))
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',type=Path,required=True)
    sub = ap.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    p = sub.add_parser('library',help='Prompt/select the next unfinished retained assets and export aggregate results')
    p.add_argument('--category')
    p.add_argument('--count',help='Positive integer or all; default prompt25')
    p.add_argument('--plan',action='store_true',help='Show next selection without processing/advancing it')
    p.add_argument('--retry-review',action='store_true',help='Explicitly retry review/failed entries; does not loop automatically')
    for name in ('run','queue'):
        p = sub.add_parser(name)
        p.add_argument('--manifest',type=Path)
        if name == 'run':
            p.add_argument('--export-default',action='store_true',help='Write a fresh local catalogue under configured exportRoot after success')
    p = sub.add_parser('work')
    p.add_argument('--job',action='append')
    sub.add_parser('status')
    p = sub.add_parser('cancel')
    p.add_argument('--job',required=True)
    p = sub.add_parser('export')
    p.add_argument('--job',action='append',required=True)
    p.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    try:
        cfg = config_load(args.config)
        store = Store(cfg['runtime'])
        if args.command == 'cancel':
            store.job(args.job)
            store.db.execute('UPDATE jobs SET cancel=1 WHERE id=?',(args.job,))
            store.db.commit()
            return 0
        if args.command == 'status':
            print(json.dumps([dict(x) for x in store.db.execute('SELECT id,lod,status,error,updated FROM jobs ORDER BY updated')],indent=2))
            return 0
        if args.command == 'export':
            if inside(args.output,PUBLIC) or any(inside(args.output,r) or inside(r,args.output) for r in cfg['sourceRoots']):
                raise ManualReview('Export must be separate from public checkout/source roots')
            print(json.dumps(export_catalogue(store,args.output,args.job),indent=2))
            return 0
        tools = fingerprints(cfg)
        if args.command == 'library':
            from intake import library
            summary=library(store,cfg,tools,SETTINGS,verify_inputs,run_job,args.category,args.count,args.plan,args.retry_review)
            return 130 if summary.get('cancelled') else (1 if summary.get('needsAttention') else 0)
        if args.command == 'doctor':
            print(json.dumps({'runtime':cfg['runtime'],'tools':tools,
                              'adapters':['known-static-native selected FPK/FTEX recipe','prepared pinned caches + native proof','retained-static automatic retained-index FMDL/DDS intake'],
                              'manual':['FOVA/characters','Unity GUI import','unknown material/hash resolution','unselected archive discovery'],
                              'networkCallsRequired':0},indent=2))
            return 0
        if args.command in ('run','queue'):
            manifest = args.manifest or Path(cfg['defaultManifest'])
            selected = load(manifest)
            if selected.get('schemaVersion') != 1 or not selected.get('assets'):
                raise ManualReview('Expected deterministic selected assets manifest schemaVersion1')
            jobs = []
            for recipe in selected['assets']:
                validate_recipe(recipe)
                verify_inputs(recipe,cfg)
                jobs += [store.enqueue(recipe,lod) for lod in sorted(set(recipe['lods']))]
            print('JOBS '+canonical(jobs),flush=True)
            if args.command == 'queue':
                return 0
        else:
            jobs = args.job or [r[0] for r in store.db.execute("SELECT id FROM jobs WHERE status IN ('queued','cancelled','failed','manual_review') ORDER BY updated,id")]
            for key in jobs:
                store.job(key)
                store.db.execute('UPDATE jobs SET cancel=0 WHERE id=?',(key,))
            store.db.commit()
        with WorkerLock(store.root):
            successes = [run_job(store,job,cfg,tools) for job in jobs]
        if all(successes) and args.command == 'run' and args.export_default:
            export_root = Path(os.path.expandvars(cfg.get('exportRoot', '%LOCALAPPDATA%/MGSV-Asset-Reference-Exports')))
            destination = export_root / (time.strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8])
            if inside(destination,PUBLIC) or any(inside(destination,r) or inside(r,destination) for r in cfg['sourceRoots']):
                raise ManualReview('Default export must be separate from public checkout/source roots')
            summary = export_catalogue(store,destination,jobs)
            print('CATALOGUE_EXPORT '+str(destination.resolve()),flush=True)
            print('Open README.md in that folder for the catalogue. '+canonical(summary),flush=True)
        return 0 if all(successes) else 1
    except KeyboardInterrupt:
        print('Stopped before/after the active asset; completed work is retained. Relaunch to resume.',file=sys.stderr)
        return 130
    except (ValueError,KeyError,ManualReview,OSError) as ex:
        print('MANUAL_REVIEW: '+str(ex),file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
