using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using FmdlStudio.Scripts.Classes;
using FmdlStudio.Scripts.MonoBehaviours;
using FmdlStudio.Scripts.Static;
public static class PreviewPartsExport {
 public static void Run(){
  string dir=Environment.GetEnvironmentVariable("MGSV_CHARACTER_PARTS_DIR");
  try{
   Directory.SetCurrentDirectory(Path.GetFullPath(Path.Combine(Application.dataPath,"..")));
   Globals.SetFmdlVersion(2.04f);Globals.SetTexturePath(Path.Combine(dir,"empty-textures"));
   foreach(string input in Directory.GetFiles(Path.Combine(dir,"inputs"),"*.fmdl")){
    foreach(var old in UnityEngine.Object.FindObjectsOfType<FoxModel>())UnityEngine.Object.DestroyImmediate(old.gameObject);
    var importer=(FmdlImporter)Activator.CreateInstance(typeof(FmdlImporter));importer.ReadWithoutAssetImportContext(input);
    var model=UnityEngine.Object.FindObjectsOfType<FoxModel>().Single();
    string name=Path.GetFileNameWithoutExtension(input);
    COLLADAConverter.ConvertToCOLLADA(model.gameObject,Path.Combine(dir,name+".dae"));
    var rows=model.GetComponentsInChildren<SkinnedMeshRenderer>(true).Select(r=>r.name+" | vertices="+r.sharedMesh.vertexCount+" | bounds="+r.sharedMesh.bounds+" | active="+r.gameObject.activeSelf);
    File.WriteAllLines(Path.Combine(dir,name+"-meshes.txt"),rows);Debug.Log("PART_EXPORT_COMPLETE "+name);
   }
   EditorApplication.Exit(0);
  }catch(Exception ex){File.WriteAllText(Path.Combine(dir,"failure.txt"),ex.ToString());Debug.LogException(ex);EditorApplication.Exit(2);}
 }
}
