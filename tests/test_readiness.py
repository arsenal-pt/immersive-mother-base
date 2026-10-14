"""Portable patched-core readiness tests; no game, installation or network operations.
The authored IH-contract fixture models module discovery and menu registration, not
a shipped copy of Infinite Heaven. Native performance requires separate real-game evidence.
"""
from pathlib import Path
import argparse, hashlib, json, sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--core", type=Path, default=HERE.parent / "core")
parser.add_argument("--library-dir", type=Path, default=None,
                    help="Existing Lupa library directory; no install is performed")
parser.add_argument("--output", type=Path, default=None)
args = parser.parse_args()
CORE = args.core.resolve()
if args.library_dir:
    sys.path.insert(0, str(args.library_dir.resolve()))
from lupa.lua51 import LuaRuntime

ENGINE_FIXTURE = '\nlocal realLoad=loadfile\nloadfile=function(path)\n local name=path:match("^fixture/(.+)$")\n if name then local s=SOURCES[name];if not s then return nil,"absent optional data"end;return loadstring(s,name)end\n return realLoad(path)\nend\nWRITES={};READS=0;NATIVE={};NOW=0;CLOCK=43200;IOCALLS=0\nio={open=function(path,mode)\n IOCALLS=IOCALLS+1\n if mode=="r"or mode=="rb"then READS=READS+1;return nil end\n local f={parts={}}\n function f:write(data)self.parts[#self.parts+1]=data;return self end\n function f:close()WRITES[path]=table.concat(self.parts);return true end\n return f\nend}\nInfCore={paths={mod="fixture/"}}\nInfMenuDefs={inMissionMenu={sentinel="external-original-menu"},safeSpaceMenu={sentinel="external-safe-menu"}}\nInfMenu={Print=function(s)LAST_NOTICE=s end}\nvars={missionCode=40050,playerPosX=1,playerPosY=0,playerPosZ=10,playerRotY=0,playerCameraRotation={[0]=0,[1]=0}}\ngvars={usingNormalMissionSlot=true};mvars={}\nTime={GetRawElapsedTimeSinceStartUp=function()return NOW end}\nMotherBaseStage={GetCurrentCluster=function()return 0 end,GetCurrentLayout=function()return 3 end,IsLoading=function()return false end,IsActivating=function()return false end}\nTppLocation={GetMbStageClusterGrade=function()return 1 end}\nTppGameObject={NPC_STATE_DISABLE=0,NPC_LIFE_STATE_NORMAL=0,NPC_LIFE_STATE_DEAD=2}\nTppMotherBaseManagement={GetMbsStaffCombatRank=function()return 3 end}\nTppEnemy={GetMBEnemyAssetTable=function()return {plnt0={soldierList={"native_1"},soldierRouteList={Sneak={{inPlnt={"patrol_a","patrol_b"}}},Night={}}}}end}\nGameObject={NULL_ID=65535,GetGameObjectId=function(kind,name)assert(kind=="TppSoldier2","only regular soldier lookup");return name=="native_1"and 1060 or 65535 end}\nGameObject.SendCommand=function(id,c)\n assert(id==1060,"unexpected actor")\n if c.id=="GetPosition"then return {GetX=function()return 10 end,GetY=function()return 0 end,GetZ=function()return 10 end}end\n if c.id=="GetStatus"then return 1 end\n if c.id=="GetLifeStatus"then return 0 end\n if c.id=="GetStaffId"then return 10001 end\n if c.id=="GetCurrentEquipId"then return 0 end\n assert(c.id=="SetSneakRoute"and(c.route=="patrol_a"or c.route=="patrol_b"),"unsupported native command/route: "..tostring(c.id).." "..tostring(c.route))\n NATIVE[#NATIVE+1]=c;return true\nend\nTppClock={GetTime=function()return CLOCK end,Start=function()end,SetTime=function()error("clock mutation unexpected")end}\nPlayerInfo={OrCheckStatus=function()return false end}\nPlayerStatusEx={SHOWER=1,TOILET_DOOR=2}\nlocal forbidden=setmetatable({},{__index=function()error("player input/camera mutation forbidden")end})\nTppPlayer=forbidden;InfCamera=forbidden\nTpp={StrCode32Table=function(t)return t end,MakeMessageExecTable=function(t)return t end}\nTppMission={CheckMessageOption=function()end}\n'

def runtime(reverse=False):
    lua = LuaRuntime(unpack_returned_tuples=True)
    mod = CORE / "GameDir/mod"
    sources = {f.relative_to(mod).as_posix(): f.read_text(encoding="utf-8-sig")
               for f in mod.rglob("*.lua")}
    lua.globals().SOURCES = lua.table_from(sources)
    lua.execute(ENGINE_FIXTURE)
    names = sorted(f.stem for f in (mod / "modules").glob("*.lua"))
    if reverse:
        names.reverse()
    lua.globals().MODULE_NAMES = lua.table_from(names)
    lua.execute(r"""
LOADING=false;ACTIVATING=false;CLUSTER=0;GETTERS=0
MotherBaseStage.GetCurrentCluster=function()return CLUSTER end
MotherBaseStage.IsLoading=function()return LOADING end
MotherBaseStage.IsActivating=function()return ACTIVATING end
MotherBaseStage.GetDemoCenter=function()return {GetX=function()return 0 end,GetY=function()return 0 end,GetZ=function()return 0 end}end
TppDefine={CLUSTER_NAME={"Command","Combat","RD","Support","Medical","Intel","Development"}}
local native=GameObject.SendCommand
GameObject.SendCommand=function(id,c)
 if c.id:sub(1,3)=="Get"then GETTERS=GETTERS+1 end
 return native(id,c)
end
IHH=setmetatable({},{__index=function()error("Core must not invoke IHHook named-pipe/native helper APIs")end})
InfModules={}
-- Authored contract fixture: IH discovers module filenames, requires returned tables,
-- binds globals, then calls lifecycle functions and registers menu parent references.
for _,n in ipairs(MODULE_NAMES)do
 local name=n
 package.preload[name]=function()return assert(loadstring(SOURCES["modules/"..name..".lua"],name))()end
 package.loaded[name]=nil
 local module=require(name);assert(type(module)=="table")
 _G[name]=module;module.name=name;InfModules[#InfModules+1]=module
end
InfMenuDefs.inMissionMenu.options={"External.sentinel"}
local function resolve(ref)
 local name,key=ref:match("^([%w_]+)%.([%w_]+)$")
 return _G[name]and _G[name][key],key
end
COMMAND_ITEMS={}
for _,module in ipairs(InfModules)do
 if module.Init then module.Init()end
 for _,key in ipairs(module.registerMenus or{})do
  local menu=assert(module[key]);assert(type(menu.options)=="table")
  for _,parentRef in ipairs(menu.parentRefs or{})do
   local parent=assert(resolve(parentRef));parent.options=parent.options or{}
   parent.options[#parent.options+1]=module.name.."."..key
  end
  for _,ref in ipairs(menu.options)do
   local value,key=resolve(ref)
   if type(value)=="function"then
    local lower=key:sub(1,1):lower()..key:sub(2)
    assert(not COMMAND_ITEMS[lower]or COMMAND_ITEMS[lower]==value,"command-name collision")
    COMMAND_ITEMS[lower]=value
   end
  end
 end
end
function Frame(t)
 NOW=t
 for _,module in ipairs(InfModules)do
  if module.Update then module.Update({inGame=true,missionCanStart=true},t)end
 end
end
function Ready()
 vars.missionCode=30050;gvars.usingNormalMissionSlot=true
 LOADING=false;ACTIVATING=false;CLUSTER=0
 Frame(0);Frame(.25);Frame(.5)
 assert(#NpcSoldiers.GetRoster()==1 and NpcLife.GetSnapshot().actors[1].name=="mb_staff_10001")
end
""")
    return lua

checks = []
def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})

for reverse in (False, True):
    lua = runtime(reverse)
    check("Module discovery/returned-table registration order " + str(reverse),
          lua.eval('#InfModules==6 and NpcLife.name=="NpcLife"'))
    check("One owned menu and original root sentinel preserved " + str(reverse),
          lua.eval('#InfMenuDefs.inMissionMenu.options==2 and InfMenuDefs.inMissionMenu.options[2]=="ImmersiveMotherBase.immersiveMotherBaseMenu" and InfMenuDefs.inMissionMenu.sentinel=="external-original-menu"'))
    lua.execute("Ready()")
    check("Normal regular-soldier startup order " + str(reverse), True)
    lua.execute(r"""
NATIVE={}
NpcLife.Command("duty",NOW)
assert(#NATIVE>0)
for _,c in ipairs(NATIVE)do assert(c.id=="SetSneakRoute"and(c.route=="patrol_a"or c.route=="patrol_b"))end
""")
    check("Valid normal patrol still dispatches stock routes " + str(reverse), True)

contexts = [
    ("non-normal mission slot", "gvars.usingNormalMissionSlot=false"),
    ("loading base", "LOADING=true"),
    ("activating base", "ACTIVATING=true"),
    ("different mission", "vars.missionCode=40050"),
    ("unsupported cluster", "CLUSTER=7"),
]
for name, transition in contexts:
    lua = runtime()
    lua.execute("Ready();NATIVE={};GETTERS=0\n" + transition)
    result = lua.execute(r"""
local commandOk=pcall(NpcLife.Command,"roam",NOW)
local requestOk=pcall(NpcLife.Request,{kind="native_duty",duty="patrol"},NOW)
NpcSoldiers.ApplyLifeAction({actor=1060,kind="roam"},NOW)
local rosterCount=#NpcSoldiers.GetRoster()
local observationCount=0;for _ in pairs(NpcSoldiers.GetObservations())do observationCount=observationCount+1 end
Frame(2)
return {commandAccepted=commandOk,requestAccepted=requestOk,nativeActions=#NATIVE,
 nativeGetters=GETTERS,rosterCount=rosterCount,observationCount=observationCount}
""")
    result = dict(result.items())
    passed = (not result["commandAccepted"] and not result["requestAccepted"]
              and all(result[k] == 0 for k in
                      ("nativeActions", "nativeGetters", "rosterCount", "observationCount")))
    check("Reject cached commands/actions and native queries: " + name, passed, result)

lua = runtime()
lua.execute("Ready();NATIVE={}")
lua.execute(r"""
for _,cmd in ipairs({"muster","gather","water","mess","bunk","toilet","shower","cqc","cqc_verify","cqc_four","cqc_auto"})do
 assert(not pcall(NpcLife.Command,cmd,NOW),"Unavailable resource action accepted: "..cmd)
end
assert(not pcall(NpcLife.Request,{kind="muster"},NOW))
assert(not pcall(NpcLife.Request,{kind="gather"},NOW))
local snapshot=NpcLife.GetSnapshot()
assert(snapshot.serviceCoverage.ready==false and snapshot.serviceCoverage.enabledCount==0)
assert(snapshot.cqcTraining.ready==false and snapshot.cqcTraining.automatic==false)
assert(#NATIVE==0)
""")
check("Missing assemblies/services/CQC stay fail closed without native actions", True)
lua.execute(r"""
local before=NpcLife.GetSnapshot().actors[1].needs
local h,t,f,y,b=before.hunger,before.thirst,before.fatigue,before.hygiene,before.bladder
CLOCK=46800;Frame(1)
local after=NpcLife.GetSnapshot().actors[1].needs
assert(after.hunger==h and after.thirst==t and after.fatigue==f and after.hygiene==y and after.bladder==b)
assert(not NpcLife.GetSnapshot().group)
""")
check("Unbound service needs defer rather than fabricate relief/availability", True)
ipc_tokens = ("IHH.", "CreateNamedPipe", "ConnectNamedPipe", "GetPipeInMessages", "QueuePipeOutMessage")
check("No authored core named-pipe API calls", not any(
    token in f.read_text(encoding="utf-8-sig")
    for f in CORE.rglob("*.lua") for token in ipc_tokens))
report = {
    "schema": 1,
    "test": "public-core-readiness",
    "fixture": "authored IH module/menu contract, synthetic native/file APIs",
    "passed": sum(c["passed"] for c in checks),
    "failed": sum(not c["passed"] for c in checks),
    "checks": checks,
    "coreHashes": {p.relative_to(CORE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in CORE.rglob("*.lua")},
    "nativeGameplayVerified": False,
    "stockIHHookPerformanceVerified": False,
    "resourceProofFlagsEnabled": False,
    "gameLaunched": False,
    "installedFilesChanged": False,
}
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"passed": report["passed"], "failed": report["failed"],
                  "nativeGameplayVerified": False}))
if report["failed"]:
    raise SystemExit(1)
