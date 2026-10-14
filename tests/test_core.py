"""Portable Lua51 candidate checks. Supply existing Lupa with --library-dir; no installation."""
from pathlib import Path
import argparse,hashlib,json,re,sys
T=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--candidate',type=Path,default=T.parent/'core')
ap.add_argument('--library-dir',type=Path,default=None)
a=ap.parse_args();C=a.candidate.resolve()
if a.library_dir:sys.path.insert(0,str(a.library_dir.resolve()))
from lupa.lua51 import LuaRuntime
manifest=json.loads((T.parent/'source-manifest.json').read_text())
checks=[]
def check(name,value,detail=None):
 checks.append({'name':name,'passed':bool(value),'detail':detail})
 if not value:raise AssertionError(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return p.read_text(encoding='utf-8-sig')
actual={p.relative_to(C).as_posix():p for p in C.rglob('*.lua')}
check('Exact authored Lua file inventory',set(actual)==set(manifest['coreLua']))
for rel,e in manifest['coreLua'].items():
 check('Frozen candidate hash: '+rel,sha(C/rel)==e['candidateSha256'])
for rel,p in actual.items():
 s=read(p)
 check('No IH-extra-NPC integration: '+rel,not re.search(r'NpcIHStaff|IHInspection|IHStaffNames|ih_staff|NpcCivilians|NativeServiceData',s))
 check('No machine-specific paths or HTTP dependency: '+rel,not re.search(r'[EGC]:[\\/]|localhost|127\.0\.0\.1|https?://',s))
check('No supplied game assets/binaries/archives/saves',all(p.suffix in ('.lua','.json','.md')and p.name not in ('life-save.lua','native-ranks.lua','native-staff-names.lua')for p in C.rglob('*')if p.is_file()))
check('GPL-3.0-only selected',manifest['license']=='GPL-3.0-only')
l=LuaRuntime(unpack_returned_tuples=True)
syntax=l.eval('function(s,n)local f,e=loadstring(s,n);return f~=nil,e end')
for rel,p in actual.items():
 ok,e=syntax(read(p),rel);check('Lua51 syntax: '+rel,ok,e)
mods={p.name[:-4]:read(p)for p in (C/'GameDir/mod/modules').glob('*.lua')}
sources={rel[len('GameDir/mod/'):]:read(p)for rel,p in actual.items()}
l.globals().SOURCES=l.table_from(sources)
l.execute(r'''
local realLoad=loadfile
loadfile=function(path)
 local name=path:match("^fixture/(.+)$")
 if name then local s=SOURCES[name];if not s then return nil,"absent optional data"end;return loadstring(s,name)end
 return realLoad(path)
end
WRITES={};READS=0;NATIVE={};NOW=0;CLOCK=43200;IOCALLS=0
io={open=function(path,mode)
 IOCALLS=IOCALLS+1
 if mode=="r"or mode=="rb"then READS=READS+1;return nil end
 local f={parts={}}
 function f:write(data)self.parts[#self.parts+1]=data;return self end
 function f:close()WRITES[path]=table.concat(self.parts);return true end
 return f
end}
InfCore={paths={mod="fixture/"}}
InfMenuDefs={inMissionMenu={sentinel="external-original-menu"},safeSpaceMenu={sentinel="external-safe-menu"}}
InfMenu={Print=function(s)LAST_NOTICE=s end}
vars={missionCode=40050,playerPosX=1,playerPosY=0,playerPosZ=10,playerRotY=0,playerCameraRotation={[0]=0,[1]=0}}
gvars={usingNormalMissionSlot=true};mvars={}
Time={GetRawElapsedTimeSinceStartUp=function()return NOW end}
MotherBaseStage={GetCurrentCluster=function()return 0 end,GetCurrentLayout=function()return 3 end,IsLoading=function()return false end,IsActivating=function()return false end}
TppLocation={GetMbStageClusterGrade=function()return 1 end}
TppGameObject={NPC_STATE_DISABLE=0,NPC_LIFE_STATE_NORMAL=0,NPC_LIFE_STATE_DEAD=2}
TppMotherBaseManagement={GetMbsStaffCombatRank=function()return 3 end}
TppEnemy={GetMBEnemyAssetTable=function()return {plnt0={soldierList={"native_1"},soldierRouteList={Sneak={{inPlnt={"patrol_a","patrol_b"}}},Night={}}}}end}
GameObject={NULL_ID=65535,GetGameObjectId=function(kind,name)assert(kind=="TppSoldier2","only regular soldier lookup");return name=="native_1"and 1060 or 65535 end}
GameObject.SendCommand=function(id,c)
 assert(id==1060,"unexpected actor")
 if c.id=="GetPosition"then return {GetX=function()return 10 end,GetY=function()return 0 end,GetZ=function()return 10 end}end
 if c.id=="GetStatus"then return 1 end
 if c.id=="GetLifeStatus"then return 0 end
 if c.id=="GetStaffId"then return 10001 end
 if c.id=="GetCurrentEquipId"then return 0 end
 assert(c.id=="SetSneakRoute"and(c.route=="patrol_a"or c.route=="patrol_b"),"unsupported native command/route: "..tostring(c.id).." "..tostring(c.route))
 NATIVE[#NATIVE+1]=c;return true
end
TppClock={GetTime=function()return CLOCK end,Start=function()end,SetTime=function()error("clock mutation unexpected")end}
PlayerInfo={OrCheckStatus=function()return false end}
PlayerStatusEx={SHOWER=1,TOILET_DOOR=2}
local forbidden=setmetatable({},{__index=function()error("player input/camera mutation forbidden")end})
TppPlayer=forbidden;InfCamera=forbidden
Tpp={StrCode32Table=function(t)return t end,MakeMessageExecTable=function(t)return t end}
TppMission={CheckMessageOption=function()end}
NpcSoldiers=assert(loadfile("fixture/modules/NpcSoldiers.lua"))()
NpcLife=assert(loadfile("fixture/modules/NpcLife.lua"))()
NpcTraining=assert(loadfile("fixture/modules/NpcTraining.lua"))()
NlabActionRecorder=assert(loadfile("fixture/modules/NlabActionRecorder.lua"))()
ImmersiveMotherBase=assert(loadfile("fixture/modules/ImmersiveMotherBase.lua"))()
NpcBaseMap=assert(loadfile("fixture/modules/NpcBaseMap.lua"))()
ALL={NpcSoldiers=NpcSoldiers,NpcLife=NpcLife,NpcTraining=NpcTraining,NlabActionRecorder=NlabActionRecorder,ImmersiveMotherBase=ImmersiveMotherBase,NpcBaseMap=NpcBaseMap}
''')
menus=l.eval(r'''function()
 local rows={}
 for name,m in pairs(ALL)do
  for _,key in ipairs(m.registerMenus or{})do
   local menu=assert(m[key],"missing registered menu")
   for _,ref in ipairs(menu.parentRefs or{})do rows[#rows+1]={module=name,key=key,parent=ref}end
   for _,ref in ipairs(menu.options or{})do
    local module,fn=ref:match("^([%w_]+)%.([%w_]+)$")
    assert(ALL[module]and type(ALL[module][fn])=="function","missing menu callback "..ref)
   end
  end
 end
 return rows
end''')()
rows=[{k:v for k,v in r.items()}for _,r in menus.items()]
externals=[r for r in rows if r['parent'].startswith('InfMenuDefs.')]
check('Exactly one owned top-level root',len(externals)==1 and externals[0]['module']=='ImmersiveMotherBase')
check('Life, staff, training, testing, recorder reachable below root',len(rows)==6 and all(r['parent']=='ImmersiveMotherBase.immersiveMotherBaseMenu'or r in externals for r in rows),rows)
check('Original IH menu tables preserved',l.eval('InfMenuDefs.inMissionMenu.sentinel=="external-original-menu"and InfMenuDefs.safeSpaceMenu.sentinel=="external-safe-menu"'))
l.execute(r'''
local before=IOCALLS
for i=1,10000 do NpcSoldiers.Update({inGame=false,missionCanStart=false},i);NpcLife.Update({inGame=false,missionCanStart=false},i);NlabActionRecorder.Update()end
assert(IOCALLS==before and #NATIVE==0,"idle work or native mutation")
''')
check('10000 inactive ticks require no HTTP, IO or NPC mutations',True)
l.execute(r'''
vars.missionCode=30050;NOW=0
NpcSoldiers.Update({inGame=true,missionCanStart=true},NOW)
assert(#NpcSoldiers.GetRoster()==1)
NpcLife.Update({inGame=true,missionCanStart=true},NOW)
local s=assert(NpcLife.GetSnapshot())
assert(#s.actors==1 and s.actors[1].name=="mb_staff_10001"and s.actors[1].role=="soldier")
assert(s.serviceCoverage.ready==false and s.serviceCoverage.enabledCount==0)
assert(s.cqcTraining.ready==false and s.cqcTraining.automatic==false)
assert(s.deferUnboundNeeds and s.strictNativeObservations)
assert(s.hierarchy.people.mb_staff_10001.rank=="Private")
local ioBefore=IOCALLS;NOW=.1
NpcLife.Update({inGame=true,missionCanStart=true},NOW)
assert(IOCALLS==ioBefore,"4Hz adapter throttle lost")
for _,command in ipairs({"muster","gather","water","bunk","toilet","shower","cqc","cqc_verify","cqc_four"})do
 local ok=pcall(NpcLife.Command,command,NOW);assert(not ok,"unavailable operation accepted: "..command)
end
assert(not pcall(NpcLife.Request,{kind="muster"},NOW))
NpcLife.Command("duty",NOW)
assert(#NATIVE>0,"normal native patrol dispatch missing")
NpcLife.Command("autonomy",NOW);NOW=.5
NpcSoldiers.Update({inGame=true,missionCanStart=true},NOW);NpcLife.Update({inGame=true,missionCanStart=true},NOW)
assert(not NpcLife.GetSnapshot().group,"missing route assembly bypassed via autonomy")
local count=0;for _,c in ipairs(NATIVE)do assert(c.route=="patrol_a"or c.route=="patrol_b");count=count+1 end
assert(count>0)
local status=assert(WRITES["fixture/nlab_life_status.json"])
assert(not status:match("ihStaff")and not status:match("ih_staff"))
NpcLife.OnAllocateTop()
assert(WRITES["fixture/nlab/imb-life-save.lua"]and WRITES["fixture/nlab/imb-native-ranks.lua"])
assert(not WRITES["fixture/nlab/life-save.lua"]and not WRITES["fixture/nlab/native-ranks.lua"])
''')
check('Actual copied regular Soldier2 provider initializes life/hierarchy with no catalog or companion',True)
check('Missing route/service/CQC resources fail closed while patrol and cleanup remain functional',True)
check('4Hz adapter and new private save namespace preserved',True)
l.execute(r'''
local before=IOCALLS;NlabActionRecorder.Init()
for i=1,10000 do NlabActionRecorder.Update()end
assert(IOCALLS==before)
NOW=1
assert(NlabActionRecorder.StartCapture{durationSeconds=5,sampleHz=5})
assert(NlabActionRecorder.MarkCapture("synthetic"))
for i=0,25 do NOW=1+i/5;NlabActionRecorder.Update()end
local s=NlabActionRecorder.GetStatus()
assert(not s.active and s.last.traceComplete and s.last.summarySaved and s.last.samples>0)
assert(s.diagnostic.enabled==false and s.diagnostic.notifications==false)
''')
check('Actual recorder012 idle/start/mark/sample/automatic close works with synthetic IO and default notifications off',True)
# Exercise existing pure behavior tests with the ORIGINAL authored resource assumptions,
# rather than mistake intentionally unavailable candidate routes for gameplay regressions.
l2=LuaRuntime(unpack_returned_tuples=True)
life=l2.execute(read(C/'GameDir/mod/nlab/NpcLifeCore.lua'))
layout=l2.execute(read(T/'fixtures/LifeLayout.lua'))
reg=l2.execute(read(C/'GameDir/mod/nlab/NpcRegistry.lua'))
tests=l2.execute(read(T/'fixtures/NpcLifeTests.lua'))
out=tests.Run(life,layout,reg)
count=int(re.search(r'ALL (\d+) BEHAVIORAL TESTS PASSED',out).group(1))
check('Existing pure daily-life behavioral suite under original authored resource assumptions',count==31,{'passed':count,'nativeProof':False})
H=l2.execute(read(C/'GameDir/mod/nlab/NativeHierarchy.lua'))
can=l2.eval('function(H,rank,post)return H.CanLead({kind="military",active=true,available=true,rank=rank},post)end')
check('Private cannot lead, corporal/team, sergeant/squad, lieutenant/platoon ceilings preserved',not can(H,'Private','Team leader')and can(H,'Corporal','Team leader')and not can(H,'Corporal','Squad leader')and can(H,'Sergeant','Squad leader')and not can(H,'Sergeant','Platoon leader')and can(H,'Lieutenant','Platoon leader'))
l2.globals().LIFE=life;l2.globals().LAYOUT=layout
l2.execute(r'''
local w=LIFE.Create(LAYOUT,{{id=1,name="one",index=1,role="soldier",kind="soldier"}},43200)
w.assemblyReservation="another_activity"
assert(not pcall(LIFE.PrepareActivity,w,{},0))
assert(not pcall(LIFE.Request,w,{kind="muster"},43200,0))
LIFE.Step(w,21600,1,{[1]={real=true,available=true,alive=true,x=0,y=0,z=0}})
assert(not w.group,"reservation lost")
''')
check('Generic shared-pad reservations remain fail closed',True)
(T.parent/'build').mkdir(exist_ok=True)
report={'schema':1,'status':'offline-pass-native-pending','nativeProof':False,'installationTested':False,'companionHttpRequired':False,'passed':len(checks),'failed':0,'checks':checks,'menus':rows,'sourceManifestSha256':sha(T/'../source-manifest.json')}
(T.parent/'build'/'Offline-Core-Report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':len(checks),'behavioralChecks':count,'failed':0,'nativeProof':False}))
