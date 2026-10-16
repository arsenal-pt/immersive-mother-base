"""Render a bounded reference from a private retained-cache configuration.

Run inside Blender: --background --factory-startup --disable-autoexec
--threads 2 --python render-preview.py -- --config PRIVATE.json --asset STEM
--sample (still + four small angles), or --full (still + 48 camera angles).
This script never extracts assets, edits originals, exports models or saves blends.
"""
import argparse, hashlib, json, math, sys, zlib
from pathlib import Path
import bpy
from mathutils import Vector

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

def run():
    args = sys.argv[sys.argv.index('--') + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--asset', required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--sample', action='store_true')
    mode.add_argument('--full', action='store_true')
    a = ap.parse_args(args)
    cfg = json.loads(a.config.read_text(encoding='utf-8-sig'))
    selected = [x for x in cfg['assets'] if x['stem'] == a.asset]
    if len(selected) != 1:
        raise ValueError('Asset selector must match exactly one approved entry')
    entry = selected[0]; asset = entry['asset']; root = Path(cfg['sourceRoot'])
    original = root / asset['raw']
    if sha(original) != asset['sha256']:
        raise ValueError('Original FMDL SHA256 changed')
    cache = json.loads(zlib.decompress((root / asset['cache']).read_bytes()))
    if cache['sha256'] != asset['sha256']:
        raise ValueError('Retained decoded cache identity differs')
    lod = json.loads(zlib.decompress((root / asset['lodFacesCache']).read_bytes()))
    face_sets = {x['meshIndex']: x['faces'] for x in lod if x['level'] == 0}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.render.film_transparent = False; sc.render.resolution_percentage = 100
    sc.render.threads_mode = 'FIXED'; sc.render.threads = 2
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
    sc.view_settings.exposure = 0; sc.view_settings.gamma = 1
    world = bpy.data.worlds.new('Reference neutral white'); world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (1,1,1,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = .65
    sc.world = world
    mats = []; texture_receipts = []
    for m in entry['material']['materials']:
        mat = bpy.data.materials.new('Retained base-color reference'); mat.use_nodes = True
        shader = mat.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Roughness'].default_value = .72
        shader.inputs['Specular IOR Level'].default_value = .18
        bases = [t for t in m['textures'] if t['samplerName'] in ('Base_Tex_SRGB', 'Base_Tex_LIN')]
        if len(bases) != 1:
            raise ValueError('Require exactly one unambiguous base-color binding')
        t = bases[0]; choices = {x['sha256']:x for x in t['ddsChoices']}
        if len(choices) != 1:
            raise ValueError('Ambiguous DDS variant')
        ch = next(iter(choices.values())); image_path = root / ch['dds']
        if sha(image_path) != ch['sha256']:
            raise ValueError('DDS content differs')
        img = bpy.data.images.load(str(image_path), check_existing=False)
        img.colorspace_settings.name = 'sRGB' if t['samplerName'].endswith('_SRGB') else 'Non-Color'
        nodes = mat.node_tree.nodes; links = mat.node_tree.links
        uv = nodes.new('ShaderNodeUVMap'); uv.uv_map = 'NativeUV0'
        mapping = nodes.new('ShaderNodeMapping')
        mapping.inputs['Location'].default_value = (0,1,0)
        mapping.inputs['Scale'].default_value = (1,-1,1)
        tex = nodes.new('ShaderNodeTexImage'); tex.image = img; tex.interpolation = 'Linear'
        links.new(uv.outputs['UV'],mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'],tex.inputs['Vector'])
        links.new(tex.outputs['Color'],shader.inputs['Base Color'])
        texture_receipts.append({'sampler':t['samplerName'],'nativePathHash':t['nativeHash'],
            'ddsSha256':ch['sha256'],'dimensions':list(img.size),'previewUvMapping':'u, 1-v'})
        mats.append(mat)
    objects=[]; topology=[]
    lo,hi = asset['bounds']; center=((lo[0]+hi[0])/2,(lo[2]+hi[2])/2,lo[1])
    for i,m in enumerate(cache['meshes']):
        faces=face_sets[i]; mesh=bpy.data.meshes.new('Retained LOD0')
        verts=[(v[0]-center[0],-v[2]+center[1],v[1]-center[2]) for v in m['vertices']]
        mesh.from_pydata(verts,[],[(f[0],f[2],f[1]) for f in faces]); mesh.update()
        if mesh.validate(verbose=False): raise ValueError('Mesh needed repair; stop')
        layer=mesh.uv_layers.new(name='NativeUV0')
        layer.data.foreach_set('uv',[n for loop in mesh.loops for n in m['attributes']['8'][loop.vertex_index]])
        for poly in mesh.polygons:poly.use_smooth=True
        if '2' in m['attributes']:
            mesh.normals_split_custom_set_from_vertices([(v[0],-v[2],v[1]) for v in m['attributes']['2']])
        mesh.materials.append(mats[m['material']])
        obj=bpy.data.objects.new('Preview '+str(i),mesh);sc.collection.objects.link(obj);objects.append(obj)
        topology.append({'meshIndex':i,'vertices':len(verts),'lod':0,'triangles':len(faces),
            'UV0Loops':len(mesh.loops),'nativeGeometryEdited':False})
    width=hi[0]-lo[0]; depth=hi[2]-lo[2]; height=hi[1]-lo[1]
    scale=max(height*1.35,math.hypot(width,depth)*1.4)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.006))
    ground=bpy.context.object;ground.name='Reference studio floor'
    mat=bpy.data.materials.new('Neutral light gray');mat.use_nodes=True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.91,.93,.95,1)
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.95
    ground.data.materials.append(mat)
    target=(0,0,height*.5)
    for name,loc,power,size in [('Key',(-3,-4,6),450,4),('Fill',(4,1,4),300,3)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
        ob=bpy.data.objects.new(name,data);sc.collection.objects.link(ob);ob.location=loc;aim(ob,target)
    camdata=bpy.data.cameras.new('Reference orbit camera');camdata.type='ORTHO';camdata.ortho_scale=scale
    camera=bpy.data.objects.new('Reference orbit camera',camdata);sc.collection.objects.link(camera);sc.camera=camera
    out=Path(cfg['outputRoot'])/entry['id'];out.mkdir(parents=True,exist_ok=True)
    def render(angle,size,path):
        radius=5*scale;rad=math.radians(angle)
        camera.location=(radius*math.sin(rad),-radius*math.cos(rad),height*.5+radius*.45)
        aim(camera,target);sc.render.resolution_x=size;sc.render.resolution_y=size;sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
    still=out/'clean-still.png'
    if not still.exists():render(35,cfg['settings']['stillSize'],still)
    frame_angles=[35,125,215,305] if a.sample else [35+360*i/cfg['settings']['frameCount'] for i in range(cfg['settings']['frameCount'])]
    directory=out/('sample-angles' if a.sample else 'clean-frames');directory.mkdir(exist_ok=True)
    for i,angle in enumerate(frame_angles):
        path=directory/f'{i:03d}.png'
        if not path.exists():render(angle,240 if a.sample else cfg['settings']['gifSize'],path)
    receipt={'assetId':entry['id'],'nativeFmdlPath':asset['nativeFmdlPath'],'nativeSha256':asset['sha256'],
        'blenderVersion':bpy.app.version_string,'stage':'sample' if a.sample else 'full',
        'rotation':'camera orbit only; static retained LOD0 geometry; not native animation',
        'anglesDegrees':frame_angles,'baseColorTextures':texture_receipts,'topology':topology,
        'nativeShaderEquivalent':False,'materials':'actual base-color texture; approximate Principled diffuse; no FOX shader/packed material reconstruction',
        'images':[{'file':p.relative_to(out).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in [still,*sorted(directory.glob('*.png'))]]}
    (out/('sample-receipt.json' if a.sample else 'render-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('ASSET_REFERENCE_COMPLETE '+entry['id'],flush=True)

if __name__=='__main__':run()
