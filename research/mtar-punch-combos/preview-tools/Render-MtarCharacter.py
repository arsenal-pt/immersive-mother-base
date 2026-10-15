"""Render real selected MTAR actions with installed mctrollin tools and a private weighted character.
Authored orchestration only: no animation decoder or community source is embedded.
Run with Blender --background --disable-autoexec --threads 2 --python this.py -- <arguments>.
"""
import argparse,hashlib,json,re,sys,time
from pathlib import Path
import bpy
from mathutils import Vector

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arguments():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['tool-dir','rig-file','track-map','bone-map','character-blend','catalogue','mtar-root','output']:
  p.add_argument('--'+name,type=Path,required=True)
 p.add_argument('--clip-id',action='append');p.add_argument('--width',type=int,default=640);p.add_argument('--height',type=int,default=640)
 p.add_argument('--source-fps',type=int,default=30);p.add_argument('--sample-step',type=int,default=2)
 return p.parse_args(sys.argv[sys.argv.index('--')+1:])

def render_clip(a,clip,mapping,mtar_reader,importer,header_types):
 started=time.monotonic();short=clip['name'].rsplit('/',1)[-1];directory=a.output/clip['id'];directory.mkdir()
 mtar=a.mtar_root/clip['sourceArchive']/(clip['sourceArchive']+'.mtar');before=sha(mtar)
 if clip.get('sourceMtarSha256'):assert before==clip['sourceMtarSha256'],'Source archive hash does not match catalogue'
 header_cls,row_cls=header_types
 with mtar.open('rb') as f:
  header=header_cls.read(f);rows=[row_cls.read(f) for _ in range(header.file_count)]
 fullhash=0xFC50000000000000+int(clip['hashId'],16);indices=[i for i,row in enumerate(rows) if row.path==fullhash]
 assert len(indices)==1,'Ambiguous or absent full archive hash'
 reader=mtar_reader(str(mtar));decoded=reader.read_selected_ganis(indices)[indices[0]]
 count=decoded.gani_track_mini_header.frame_count
 assert decoded.file_header.path==fullhash and count==clip['frameCount'],'Decoded identity/frame mismatch'
 missing=[track.name for track in decoded.gani_bone_tracks if track.name not in mapping.fox_to_blender]
 assert not missing,'Missing base track mappings: '+repr(missing)
 bpy.ops.wm.open_mainfile(filepath=str(a.rig_file))
 for o in list(bpy.data.objects):
  if o.type=='ARMATURE':o.animation_data_clear();o.hide_render=True
  else:bpy.data.objects.remove(o,do_unlink=True)
 for lc in bpy.context.view_layer.layer_collection.children:lc.exclude=False
 rig=bpy.data.objects['rig'];rig.hide_set(False);rig.hide_viewport=False
 props=bpy.context.scene.mtar_properties;props.import_props.use_verbose_naming=True;props.settings_props.sort_gani=False
 result,raw=importer.import_mtar(bpy.context,str(mtar),None,mapping.fox_to_blender,indices,rig,0,gani_hash_dict={fullhash:clip['name']},transform_constraints=mapping.transform_constraints)
 assert 'FINISHED' in result,str(result)
 with bpy.data.libraries.load(str(a.character_blend),link=False) as (source,loaded):loaded.objects=list(source.objects)
 for o in loaded.objects:
  if o.name not in bpy.context.scene.collection.objects:bpy.context.scene.collection.objects.link(o)
 bpy.context.view_layer.update();native=next(o for o in loaded.objects if o.type=='ARMATURE');target=bpy.data.objects['Skeleton_mgs5_Rigify'];meshes=[o for o in loaded.objects if o.type=='MESH']
 choices={}
 for author,native_name in re.findall(r'^\s*([^#;:\s]+)\s*:\s*(SKL_\w+)\s*;',a.bone_map.read_text(),re.M):choices.setdefault(native_name,[]).append(author)
 exact={name:targets[0] for name,targets in choices.items() if targets[0] in target.data.bones};resolved=dict(exact);fallback={}
 for bone in native.data.bones:
  if bone.name in exact:continue
  parent=bone.parent
  while parent and parent.name not in exact:parent=parent.parent
  if parent:resolved[bone.name]=exact[parent.name];fallback[bone.name]=parent.name
 weighted={g.name for o in meshes for g in o.vertex_groups};assert weighted<=set(resolved),'Unmapped weighted native bones: '+repr(weighted-set(resolved))
 weight_audit=[]
 for o in meshes:
  o.hide_render='_IV' in o.name
  o.data.materials.clear();mat=bpy.data.materials.new('Untextured stock reference');mat.diffuse_color=(.44,.53,.64,1);o.data.materials.append(mat)
  for polygon in o.data.polygons:polygon.use_smooth=True
  old_groups={g.index:g.name for g in o.vertex_groups};weights=[];original_sums=[]
  for vertex in o.data.vertices:
   merged={};original_sums.append(sum(g.weight for g in vertex.groups))
   for g in vertex.groups:
    name=resolved[old_groups[g.group]];merged[name]=merged.get(name,0)+g.weight
   weights.append(merged)
  o.vertex_groups.clear();names=sorted({name for row in weights for name in row});groups={n:o.vertex_groups.new(name=n) for n in names}
  for i,row in enumerate(weights):
   for name,value in row.items():groups[name].add([i],value,'REPLACE')
  errors=[abs(original-sum(g.weight for g in vertex.groups)) for original,vertex in zip(original_sums,o.data.vertices)]
  assert max(errors,default=0)<1e-5,'Weight conservation failure'
  weight_audit.append({'mesh':o.name,'vertices':len(o.data.vertices),'sourceGroups':sorted(old_groups.values()),'targetGroups':names,'maxPerVertexWeightSumError':max(errors,default=0)})
  for modifier in o.modifiers:
   if modifier.type=='ARMATURE':modifier.object=target
 scene=bpy.context.scene
 def set_frame(frame):scene.frame_set(frame);bpy.context.view_layer.update()
 def vertices():
  dg=bpy.context.evaluated_depsgraph_get();coords=[]
  for o in meshes:
   if o.hide_render:continue
   evaluated=o.evaluated_get(dg);mesh=evaluated.to_mesh();coords.extend(evaluated.matrix_world@v.co for v in mesh.vertices);evaluated.to_mesh_clear()
  return coords
 # Fit one fixed camera to all integer-frame evaluated vertices, preserving root travel.
 direction=Vector((-3.5,6,2.1)).normalized();rotation=(-direction).to_track_quat('-Z','Y');inverse=rotation.inverted()
 projected_min=[float('inf')]*3;projected_max=[float('-inf')]*3;world_min=[float('inf')]*3;world_max=[float('-inf')]*3;frame_bounds=[]
 for frame in range(count+1):
  set_frame(frame);coords=vertices();lo=[min(p[i] for p in coords) for i in range(3)];hi=[max(p[i] for p in coords) for i in range(3)];frame_bounds.append({'frame':frame,'min':lo,'max':hi})
  for p in coords:
   q=inverse@p
   for axis in range(3):
    projected_min[axis]=min(projected_min[axis],q[axis]);projected_max[axis]=max(projected_max[axis],q[axis]);world_min[axis]=min(world_min[axis],p[axis]);world_max[axis]=max(world_max[axis],p[axis])
 assert all(abs(x)<100 for x in world_min+world_max),'Implausible motion bounds; inspect before publication'
 center=rotation@Vector([(x+y)/2 for x,y in zip(projected_min,projected_max)])
 bpy.ops.mesh.primitive_plane_add(size=200,location=(center.x,center.y,world_min[2]-.02));ground=bpy.context.object;material=bpy.data.materials.new('Studio ground');material.diffuse_color=(.12,.15,.2,1);ground.data.materials.append(material)
 bpy.ops.object.camera_add(location=center+direction*10);camera=bpy.context.object;camera.rotation_euler=rotation.to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=max((projected_max[1]-projected_min[1])*1.16,(projected_max[0]-projected_min[0])*a.height/a.width*1.16);scene.camera=camera
 scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=a.width;scene.render.resolution_y=a.height;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.render.fps=a.source_fps
 scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.world.color=(.055,.065,.09)
 sampled=list(range(0,count,a.sample_step));rendered=sampled+[count]
 for frame in rendered:set_frame(frame);scene.render.filepath=str(directory/('frame-'+str(frame).zfill(4)+'.png'));bpy.ops.render.render(write_still=True)
 assert sha(mtar)==before,'Original archive changed'
 report={'id':clip['id'],'name':clip['name'],'shortIdentifier':short,'sourceArchive':clip['sourceArchive'],'sourceArchiveSha256':before,'sourceRole':clip['sourceRole'],'role':clip['role'],'sequenceFamily':clip['sequenceFamily'],'phase':clip['phase'],'phaseKind':clip['phaseKind'],'hashId':clip['hashId'],'originalGaniSha256':next(s['sha256'] for s in (clip.get('sidecars') or clip['payloads']) if s['extension']=='.gani'),'headerIndex':indices[0],'fullArchivePathHash':hex(fullhash),'rawFrameCount':count,'decodedTrackCount':len(decoded.gani_bone_tracks),'sourceFramesSampled':sampled,'separateEndpointFrame':count,'chosenSourceFramesPerSecond':a.source_fps,'nativeFrameRate':None,'rawLayoutFrameRateField':str(reader.common_info.layout_track.header.frame_rate),'sampleStep':a.sample_step,'referenceCharacter':'Stock Ocelot oce0_main0_def','nativeGameplayProof':False,'pairedAlignmentProof':False,'ordinarySoldierAttackProof':False,'referenceArmature':target.name,'boneMapChoices':choices,'nativeToReference':resolved,'secondaryBoneAncestorFallbacks':fallback,'weightAudit':weight_audit,'visibleMeshes':[o.name for o in meshes if not o.hide_render],'hiddenMeshes':[o.name for o in meshes if o.hide_render],'worldBounds':{'min':world_min,'max':world_max},'camera':{'fixedForEntireClip':True,'location':list(camera.location),'rotation':list(camera.rotation_euler),'orthographicScale':camera.data.ortho_scale,'projectedMin':projected_min,'projectedMax':projected_max},'frameBounds':frame_bounds,'cleanPngs':[{'path':('frame-'+str(f).zfill(4)+'.png'),'sha256':sha(directory/('frame-'+str(f).zfill(4)+'.png'))} for f in rendered],'seconds':round(time.monotonic()-started,3),'limitations':['Community offline reference-rig deformation','Hair/scarf/holster secondary bones follow nearest mapped native ancestor without native simulation','Native Fox twist/cloth/gameplay/contact/timing compatibility unverified']}
 (directory/'render-receipt.json').write_text(json.dumps(report,indent=2));print('CLIP_RENDER_COMPLETE '+clip['id'],flush=True);return {'id':clip['id'],'renderReceipt':clip['id']+'/render-receipt.json','renderReceiptSha256':sha(directory/'render-receipt.json'),'rawFrameCount':count,'pngCount':len(rendered)}

def main():
 a=arguments();assert not a.output.exists(),'Output must be a fresh directory';a.output.mkdir(parents=True)
 sys.path.insert(0,str(a.tool_dir.parent));addon=__import__(a.tool_dir.name);addon.register()
 from fox_engine_mtar_tools_blender.py_tools import tools_mtar_importer
 from fox_engine_mtar_tools_blender.py_foxwrap.fwrap_mtar_reader import MtarReader
 from fox_engine_mtar_tools_blender.py_foxwrap import fwrap_mapping
 from fox_engine_mtar_tools_blender.py_fox.fox_mtar_types import MtarHeader,MtarTableList2
 catalogue=json.loads(a.catalogue.read_text(encoding='utf-8-sig'));clips=[c for c in catalogue['animations'] if not a.clip_id or c['id'] in a.clip_id];assert clips
 if a.clip_id:assert set(a.clip_id)=={c['id'] for c in clips},'Unknown requested clip'
 mapping=fwrap_mapping.parse_track_mapping_file(str(a.track_map));provenance={'blender':bpy.app.version_string,'referenceRigSha256':sha(a.rig_file),'trackMapSha256':sha(a.track_map),'boneMapSha256':sha(a.bone_map),'privateWeightedCharacterBlendSha256':sha(a.character_blend),'catalogueSha256':sha(a.catalogue),'scriptSha256':sha(__file__),'communityRevision':'7fa90e589349ad4ba87102f0061a8d8d343a8bf4','chosenSourceFramesPerSecond':a.source_fps,'sampleStep':a.sample_step,'clips':[]}
 for clip in clips:
  provenance['clips'].append(render_clip(a,clip,mapping,MtarReader,tools_mtar_importer,(MtarHeader,MtarTableList2)));(a.output/'batch-receipt.json').write_text(json.dumps(provenance,indent=2))
 print('BATCH_COMPLETE '+str(len(clips)),flush=True)
if __name__=='__main__':main()

