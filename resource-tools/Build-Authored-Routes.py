"""Compile/check authored routes with explicit preexisting pinned tools. Never install or download."""
from pathlib import Path
import argparse,hashlib,json,subprocess,datetime
T=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--foxlib',type=Path,required=True);p.add_argument('--fsharp',type=Path,required=True)
p.add_argument('--cityhash',type=Path,required=True);p.add_argument('--csc',type=Path,required=True)
p.add_argument('--output-dir',type=Path)
a=p.parse_args()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pins={'foxlib':'eaeb00940bffd333a717aca7c3585f6702ff0f520d07cec12b8fe1d5626332da','fsharp':'2eee5b134a56e6316f3b1e903492dad41450968d201e2dccf751cc3c462c02c9','cityhash':'def6c4506d461b65e4059b2936b2cbd5f852ba5d1d8a1a527f1c0e6dc7008c8f'}
for k,v in pins.items():assert sha(getattr(a,k))==v,'Dependency hash mismatch: '+k
out=(a.output_dir or T/'private-builds'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')).resolve()
assert out.is_relative_to((T/'private-builds').resolve())and not out.exists(),'New private resource-tools/private-builds output required'
out.mkdir(parents=True)
exe=out/'AuthoredRoutes.exe';frt=out/'imb_life_routes.frt';src=T/'AuthoredRoutes.cs';data=T.parent/'resources-authored/Route-Waypoints.json'
compile_args=[str(a.csc),'/nologo','/out:'+str(exe),'/r:'+str(a.csc.parent/'System.Web.Extensions.dll'),'/r:'+str(a.foxlib),'/r:'+str(a.fsharp),'/r:'+str(a.cityhash),str(src)]
r=subprocess.run(compile_args,capture_output=True,text=True)
receipt={'schema':1,'authoredSourceSha256':sha(src),'waypointsSha256':sha(data),'dependencyHashes':pins,'compilerSha256':sha(a.csc),'compileExit':r.returncode,'compileLog':r.stdout+r.stderr,'inheritedRoutes':0,'installed':False,'nativeProof':False,'toolBinariesRedistributed':False}
if r.returncode==0:
 run=subprocess.run([str(exe),str(data),str(frt),str(a.foxlib.resolve()),str(a.fsharp.resolve()),str(a.cityhash.resolve())],capture_output=True,text=True)
 receipt.update(runExit=run.returncode,runLog=run.stdout+run.stderr)
 if run.returncode==0:receipt.update(routeCount=len(json.loads(data.read_text())['routes']),frtSha256=sha(frt),frtBytes=frt.stat().st_size)
receipt['status']='offline-authored-route-roundtrip-pass'if receipt.get('runExit')==0 else'offline-build-failed'
(out/'Build-Receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
if receipt.get('runExit')!=0:raise SystemExit(1)
