// Authored route-only writer. Input is owned waypoint JSON; never reads a route template.
// Hash recipe is independently expressed from local FoxKit Utils/Hashing.cs;
// third-party acknowledgement and pinned dependency/notice status are separate.
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Reflection;
using System.Web.Script.Serialization;
using FL=FoxLib.Tpp.RouteSet;
class Program {
 static string fox,fsharp,city;
 static Assembly Resolve(object sender,ResolveEventArgs e){
  string n=new AssemblyName(e.Name).Name;
  if(n=="FoxLib")return Assembly.LoadFrom(fox);
  if(n=="FSharp.Core")return Assembly.LoadFrom(fsharp);
  if(n=="CityHash")return Assembly.LoadFrom(city);
  return null;
 }
 static void Main(string[] a){
  if(a.Length!=5)throw new Exception("waypoint-json output-frt foxlib-dll fsharp-dll cityhash-dll required");
  fox=Path.GetFullPath(a[2]);fsharp=Path.GetFullPath(a[3]);city=Path.GetFullPath(a[4]);
  AppDomain.CurrentDomain.AssemblyResolve+=Resolve;
  RouteOnly.Run(a[0],a[1]);
 }
}
class RouteOnly {
 static uint Hash(string name){
  if(string.IsNullOrEmpty(name)||name.Any(c=>c>127)||name.Contains("."))throw new Exception("Only exact ASCII authored route/event names");
  ulong first=((ulong)name[0]<<16)+(ulong)name.Length;
  return (uint)CityHash.CityHash.CityHash64WithSeeds(name+"\0",0x9ae16a3b2f90404fUL,first);
 }
 static float F(Dictionary<string,object>d,string k){
  float f=Convert.ToSingle(d[k]);if(float.IsNaN(f)||float.IsInfinity(f))throw new Exception("Nonfinite coordinate");return f;
 }
 static FL.RouteSet Read(string path){
  using(var b=new BinaryReader(File.OpenRead(path)))return FL.Read(new FL.ReadFunctions(b.ReadSingle,b.ReadUInt16,b.ReadUInt32,b.ReadInt32,b.ReadBytes,n=>b.BaseStream.Seek(n,SeekOrigin.Current)));
 }
 public static void Run(string input,string output){
  if(File.Exists(output))throw new Exception("New output required; preserve prior artifacts");
  if(Hash("nlab_muster_00")!=1762947339U||Hash("RelaxedRun")!=2801188700U)throw new Exception("Hash recipe differs from prior authored/native-name vectors");
  var root=(Dictionary<string,object>)new JavaScriptSerializer().DeserializeObject(File.ReadAllText(input));
  var raw=(object[])root["routes"];
  var routes=new List<FL.Route>(); // EMPTY; no inherited/template/stock routes.
  var expected=new Dictionary<uint,Dictionary<string,object>>();
  foreach(var obj in raw){
   var d=(Dictionary<string,object>)obj;string name=(string)d["name"];
   if(!name.StartsWith("nlab_",StringComparison.Ordinal))throw new Exception("Route name outside owned namespace");
   uint hash=Hash(name);if(expected.ContainsKey(hash))throw new Exception("Authored hash collision");expected[hash]=d;
   uint edge=(string)d["edgeEvent"]=="legacy-default-edge"?591731182U:Hash((string)d["edgeEvent"]);
   uint node=Convert.ToUInt32(d["nodeEventId"]);
   if((edge!=591731182U&&edge!=2801188700U)||node!=561913624U)throw new Exception("Unreviewed route event");
   float x=F(d,"x"),y=F(d,"y"),z=F(d,"z");double yaw=Convert.ToDouble(d["yaw"]);
   if(double.IsNaN(yaw)||double.IsInfinity(yaw))throw new Exception("Nonfinite yaw");
   uint rot=(uint)Math.Round(((yaw%360+360)%360)/360*65535);uint packed=(rot<<16)|65535U;
   var pos=new FoxLib.Core.Vector3(x,y,z);var start=d.ContainsKey("start")?(Dictionary<string,object>)d["start"]:d;
   var nodes=new[]{
    new FL.RouteNode(new FoxLib.Core.Vector3(F(start,"x"),F(start,"y"),F(start,"z")),new FL.RouteEvent(edge,0,0,0,0,0,0,0,0,0,0,""),new FL.RouteEvent[0]),
    new FL.RouteNode(pos,new FL.RouteEvent(edge,0,0,0,0,0,0,0,0,0,0,""),new[]{new FL.RouteEvent(node,1,packed,0,0,0,0,0,0,0,0,"")})};
   routes.Add(new FL.Route(hash,nodes));
  }
  using(var b=new BinaryWriter(File.Create(output)))FL.Write(new FL.WriteFunctions(b.Write,b.Write,b.Write,b.Write,b.Write,n=>b.Write(new byte[n])),new FL.RouteSet(routes.ToArray()));
  var back=Read(output).Routes.ToArray();
  if(back.Length!=raw.Length||back.Select(r=>r.Name).Distinct().Count()!=raw.Length)throw new Exception("Round-trip membership mismatch");
  foreach(var r in back){
   var d=expected[r.Name];var nodes=r.Nodes.ToArray();if(nodes.Length!=2)throw new Exception("Route node count changed");
   // Verify field values via public RouteNode records without assuming native acceptance.
   var last=nodes[1];
   var prop=last.GetType().GetProperties().FirstOrDefault(property=>property.PropertyType==typeof(FoxLib.Core.Vector3));
   if(prop==null)throw new Exception("Position property unavailable");
   var p=(FoxLib.Core.Vector3)prop.GetValue(last,null);
   foreach(var axis in new[]{"X","Y","Z"}){
    var field=p.GetType().GetProperty(axis);
    if(field==null)throw new Exception("Vector axis property unavailable");
    double v=Convert.ToDouble(field.GetValue(p,null)),target=Convert.ToDouble(d[axis.ToLower()]);
    if(Math.Abs(v-target)>0.0001)throw new Exception("Coordinate round-trip changed");
   }
  }
  Console.WriteLine("AUTHORED ROUTE ROUNDTRIP "+back.Length+"; inherited=0; nativeProof=false");
 }
}
