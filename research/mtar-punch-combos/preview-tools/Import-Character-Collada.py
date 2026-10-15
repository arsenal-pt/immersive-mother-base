"""Import a copied community-exported COLLADA character with Blender 3.6 standard skinning."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
 a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);assert a.input.is_file() and not a.output.exists();a.output.parent.mkdir(parents=True,exist_ok=True)
 before=hashlib.sha256(a.input.read_bytes()).hexdigest();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 assert 'FINISHED' in bpy.ops.wm.collada_import(filepath=str(a.input));bpy.context.view_layer.update()
 meshes=[o for o in bpy.data.objects if o.type=='MESH'];arms=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert meshes and arms
 inventory=[]
 for o in meshes:
  assert all(vertex.groups for vertex in o.data.vertices),'Unweighted vertices in '+o.name
  inventory.append({'mesh':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'vertexGroups':[g.name for g in o.vertex_groups],'armatureModifiers':[m.object.name for m in o.modifiers if m.type=='ARMATURE' and m.object]})
 assert hashlib.sha256(a.input.read_bytes()).hexdigest()==before
 bpy.ops.wm.save_as_mainfile(filepath=str(a.output),check_existing=False)
 report={'blender':bpy.app.version_string,'sourceColladaSha256':before,'weightedCharacterBlendSha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'sourceUnchanged':True,'armatures':[{'name':o.name,'bones':len(o.data.bones)} for o in arms],'meshes':inventory}
 a.output.with_suffix('.import-receipt.json').write_text(json.dumps(report,indent=2));print('WEIGHTED_CHARACTER_IMPORTED '+str(len(meshes)))
if __name__=='__main__':main()
