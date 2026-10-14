-- Reversible physical test staff. Never dismisses/recruits saved Mother Base staff.
local this={updateRate=0,execState={nextUpdate=0},version="0.1.18"}
this.registerMenus={"npcStaffControlMenu"}
this.npcStaffControlMenu={parentRefs={"NpcLife.npcLifeMenu","InfMenuDefs.inMissionMenu"},options={
 "NpcStaffControl.AddOne","NpcStaffControl.RemoveOne","NpcStaffControl.AddFive",
 "NpcStaffControl.FillPool","NpcStaffControl.ClearTests","NpcStaffControl.ShowCapacity"}}
this.langStrings={eng={npcStaffControlMenu="Mother Base test staff",addOne="Add one test soldier",
 removeOne="Remove one test soldier",addFive="Add five test soldiers",fillPool="Fill test pool (up to 10)",
 clearTests="Remove all test soldiers",showCapacity="Show test staff capacity"},
 help={eng={npcStaffControlMenu="Ten loaded private Soldier2 slots on Command platform 1. Removal hides only test actors; saved staff are never dismissed."}}}
local MAX=10
local session=_G.NlabStaffControlSession
if type(session)~="table"then
 session={actors={},lastCommand="none",commandError="",errors={},sequence=0}
 _G.NlabStaffControlSession=session
 local f=io.open(InfCore.paths.mod.."nlab_staff_command.txt","r")
 if f then session.lastCommand=f:read("*a"):match("^([%w_%-]+)%s+")or"none";f:close()end
end
local actors=session.actors
local nextTick,nextPublish,lastNow=0,0,0
local routes,staffNames={},{}
local nextNames,nextSavedCount=0,0
local savedCount
local registeredTo
local identity=assert(loadfile(InfCore.paths.mod.."nlab/NpcRegistry.lua"))().StaffIdentity
local function errorMessage(msg)
 if #session.errors>=32 then table.remove(session.errors,1)end
 session.errors[#session.errors+1]=tostring(msg)
end
local function read(id,command)
 local ok,value=pcall(GameObject.SendCommand,id,{id=command})
 if ok then return value end
 return nil
end
local function send(id,command)
 local ok,value=pcall(GameObject.SendCommand,id,command)
 if not ok then errorMessage(command.id..": "..tostring(value))end
 return ok,value
end
local function cluster()
 local ok,value=pcall(MotherBaseStage.GetCurrentCluster)
 return ok and value or -1
end
local function active()return vars.missionCode==30050 and cluster()==0 and gvars.usingNormalMissionSlot==true end
local function nowTime()return Time.GetRawElapsedTimeSinceStartUp()end
local function validHandle(a)
 return vars.missionCode==30050 and GameObject.GetGameObjectId("TppSoldier2",a.locator)==a.id
end
local function physical(a)
 if not validHandle(a)then return false end
 local status=read(a.id,"GetStatus")
 return status~=nil and status~=TppGameObject.NPC_STATE_DISABLE
end
local function position(id)
 local p=read(id,"GetPosition")
 if not p then return nil end
 return {x=p:GetX(),y=p:GetY(),z=p:GetZ()}
end
local function ownedCount()
 local n=0;for _ in pairs(actors)do n=n+1 end;return n
end
local function scanPool()
 local slots={};local loaded,free,occupied=0,0,0
 for i=0,MAX-1 do
  local name=string.format("sol_nlab_%04d",i);local id=GameObject.GetGameObjectId("TppSoldier2",name)
  if id~=GameObject.NULL_ID then
   loaded=loaded+1
   local status=read(id,"GetStatus");local owned=actors[id]and actors[id].locator==name
   if status==TppGameObject.NPC_STATE_DISABLE and not owned then free=free+1
   elseif not owned then occupied=occupied+1 end
   slots[#slots+1]={id=id,locator=name,index=i,status=status,owned=owned}
  end
 end
 return slots,loaded,free,occupied
end
local function collectRoutes()
 routes={}
 local fn=TppEnemy.GetMBEnemyAssetTable or mvars.mbSoldier_funcGetAssetTable
 local assets=fn and fn(1);local a=assets and assets.plnt0;local seen={}
 for _,category in ipairs({"Sneak","Night"})do
  for _,g in ipairs(a and a.soldierRouteList and a.soldierRouteList[category]or{})do
   for _,name in ipairs(g.inPlnt or{})do if not seen[name]then seen[name]=true;routes[#routes+1]=name end end
  end
 end
end
local function route(a,name,now,urgent)
 if not name then return false end
 local ok=send(a.id,{id="SetSneakRoute",route=name,point=0,isRelaxed=not urgent})
 if ok then a.route=name;a.assignedAt=now;a.lastMoved=now end
 return ok
end
local function roam(a,now)
 if #routes==0 then collectRoutes()end
 if #routes==0 then a.reason="Waiting for a native patrol route";return end
 local i=math.random(1,#routes);if routes[i]==a.route and #routes>1 then i=i%#routes+1 end
 a.lifeControlled=false;a.target=nil;a.detourUntil=nil;a.nextChange=now+math.random(90,180);a.reason="test staff native patrol"
 if route(a,routes[i],now)then a.routeChanges=a.routeChanges+1 end
end
local function refreshNames(now)
 if now<nextNames then return end;nextNames=now+5
 local fn=loadfile(InfCore.paths.mod.."nlab/native-staff-names.lua")
 if fn then local ok,names=pcall(fn);if ok and type(names)=="table"then staffNames=names end end
end
local function duplicateIdentity(id,locator)
 local name=identity(read(id,"GetStaffId"),locator)
 for _,s in ipairs(NpcSoldiers and NpcSoldiers.GetRoster()or{})do if s.id==id or s.name==name then return true end end
 for other,a in pairs(actors)do if other~=id and identity(read(other,"GetStaffId"),a.locator)==name then return true end end
 return false
end
local function finishDisable(a)
 -- Restore only the realization flags this controller set on its private slot.
 send(a.id,{id="SetForceRealize",forceRealize=false})
 send(a.id,{id="SetIgnoreDisableNpc",enable=false})
 actors[a.id]=nil
end
local function disable(a,now)
 if not validHandle(a)then actors[a.id]=nil;return true end
 if read(a.id,"GetStatus")==TppGameObject.NPC_STATE_DISABLE then finishDisable(a);return true end
 if a.phase=="removing"then return true end
 local ok=send(a.id,{id="SetEnabled",enabled=false})
 if not ok then a.reason="Engine rejected removal of the test actor";return false end
 if read(a.id,"GetStatus")==TppGameObject.NPC_STATE_DISABLE then finishDisable(a)
 else a.removeFromPhase=a.phase;a.phase="removing";a.removalRequestedAt=now or nowTime();a.reason="Waiting for engine disable confirmation"end
 return true
end
local function enable(slot,now)
 if duplicateIdentity(slot.id,slot.locator)then return false,"A test slot duplicates an active person's staff identity"end
 local params=mvars.mbSoldier_clusterParamList and mvars.mbSoldier_clusterParamList[cluster()+1]
 if not(params and params.CP_NAME)then return false,"Mother Base command post is unavailable"end
 local a={id=slot.id,locator=slot.locator,index=slot.index,phase="initializing",activateAt=now+2,startedAt=now,
  travelled=0,routeChanges=0,lastMoved=now,assignedAt=now,nextChange=now+120,reason="DD model initialization"}
 actors[a.id]=a
 if not send(a.id,{id="SetCommandPost",cp=params.CP_NAME})or not send(a.id,{id="SetEnabled",enabled=false,noAssignRoute=true})then
  disable(a);return false,"Private actor command-post binding failed"
 end
 local ok,e=pcall(TppEnemy.SetSoldierType,a.id,EnemyType.TYPE_DD)
 if not ok then errorMessage(e);disable(a);return false,"DD model initialization failed"end
 local commands={
  {id="ChangeFova",faceId=222,balaclavaFaceId=222,bodyId=TppEnemyBodyId.dds3_main0_v00,seed=slot.index+1},
  {id="SetSneakRoute",route=routes[slot.index%#routes+1],point=0,isRelaxed=true},
  {id="SetEnabled",enabled=true,noAssignRoute=true},
  {id="SetFriendly",enabled=true},{id="SetUnarmed",enabled=true},{id="SetIgnoreDisableNpc",enable=true},
  {id="SetForceRealize",forceRealize=true}}
 for _,c in ipairs(commands)do
  if not send(a.id,c)then disable(a);return false,"Could not initialize the private test actor"end
 end
 -- SetEnabled is asynchronous in the live engine; confirm it after model initialization.
 local p=position(a.id);if p then a.x=p.x;a.y=p.y;a.z=p.z end
 return true
end
function this.SetCount(n,now)
 if type(n)~="number"or n%1~=0 or n<0 or n>MAX then return false,"Count must be an integer from 0 to 10"end
 if not active()then return false,"Test staff controls require the normal Mother Base Command cluster"end
 now=now or nowTime();lastNow=now;collectRoutes()
 local slots,loaded,free=scanPool()
 local current=ownedCount()
 if n>current and #routes==0 then return false,"Native Command patrol routes are unavailable"end
 if n>current+free then return false,"Not enough free loaded test slots ("..free.." free; "..loaded.." loaded)"end
 if n>current then
  for _,slot in ipairs(slots)do
   if current>=n then break end
   if not slot.owned and slot.status==TppGameObject.NPC_STATE_DISABLE then
    local ok,e=enable(slot,now);if not ok then return false,e end;current=current+1
   end
  end
 else
  local ordered={};for _,a in pairs(actors)do ordered[#ordered+1]=a end
  table.sort(ordered,function(a,b)return a.index>b.index end)
  for _,a in ipairs(ordered)do if current<=n then break end
   if not disable(a)then return false,"A private test actor could not be disabled"end;current=current-1
  end
 end
 return true
end
function this.Control(action,count,now)
 if action=="count"then return this.SetCount(count,now)
 elseif action=="add"or action=="remove"then
  if type(count)~="number"or count%1~=0 or count<1 or count>MAX then return false,"Amount must be an integer from 1 to 10"end
  local target=ownedCount()+(action=="add"and count or-count)
  if target<0 then target=0 end
  return this.SetCount(target,now)
 elseif action=="clear"then
  if count~=0 then return false,"Clear requires count zero"end
  return this.SetCount(0,now)
 end
 return false,"Unsupported staff action"
end
function this.GetRoster()
 local out={};if not active()then return out end
 refreshNames(lastNow)
 for id,a in pairs(actors)do
  local life=read(id,"GetLifeStatus");local p=position(id)
  if (a.phase=="active"or(a.phase=="removing"and a.removeFromPhase=="active"))and physical(a)and life~=nil and life~=TppGameObject.NPC_LIFE_STATE_DEAD
   and p and math.abs(p.x)+math.abs(p.y)+math.abs(p.z)>.1 then
   local staff=read(id,"GetStaffId");local name=identity(staff,a.locator);local codeName=staffNames[name]
   local ok,ability=pcall(TppMotherBaseManagement.GetMbsStaffCombatRank,{staffId=staff})
   out[#out+1]={id=id,name=name,codeName=codeName,label=codeName or"DD test soldier",locator=a.locator,
    nameSource=codeName and"native codename + owned English language data"or"unresolved native name",
    role="soldier",kind="soldier",index=1000+a.index,nativeStaffId=staff,skillRating=ok and ability or nil,
    cluster=1,platform=0,pilotEligible=true,native=false,managedTest=true}
  end
 end
 table.sort(out,function(a,b)return a.locator<b.locator end);return out
end
function this.GetObservations()
 local out={}
 for _,s in ipairs(this.GetRoster())do
  local a=actors[s.id];local p=position(s.id);local life=read(s.id,"GetLifeStatus")
  if p then out[s.id]={x=p.x,y=p.y,z=p.z,real=physical(a),alive=life~=TppGameObject.NPC_LIFE_STATE_DEAD,
   available=life==TppGameObject.NPC_LIFE_STATE_NORMAL,nativeLifeStatus=life,managedTest=true,
   presenceSource="enabled private Soldier2 test actor",equip=read(s.id,"GetCurrentEquipId")}end
 end
 return out
end
function this.ApplyLifeAction(action,now)
 local a=actors[action.actor]
 if not a or a.phase~="active"or not physical(a)or read(a.id,"GetLifeStatus")~=TppGameObject.NPC_LIFE_STATE_NORMAL then return end
 if action.kind=="roam"then roam(a,now)
 elseif action.kind=="move"and action.target and action.target.route then
  a.lifeControlled=true;a.target=action.target;a.detourUntil=nil;a.reason="ordered test staff destination"
  route(a,action.target.route,now,action.target.urgency=="muster")
 elseif action.kind=="hold"then a.lifeControlled=true;a.target=nil;a.detourUntil=nil;a.reason="native standing wait"
 elseif action.kind=="nativeDuty"then
  roam(a,now);a.lifeControlled=true;a.reason="test staff duty patrol"
 end
end
local function json(v)
 local t=type(v);if t=="nil"then return"null"end
 if t=="number"then return(v==v and v~=math.huge and v~=-math.huge)and tostring(v)or"null"end
 if t=="boolean"then return tostring(v)end
 if t=="string"then return'"'..v:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r'):gsub('\t','\\t')..'"'end
 if t~="table"then return json(tostring(v))end
 local n,m,array=0,0,true;for k in pairs(v)do n=n+1;if type(k)~="number"or k<1 or k%1~=0 then array=false else m=math.max(m,k)end end
 array=array and n==m;local rows={}
 if array then for i=1,n do rows[#rows+1]=json(v[i])end else for k,x in pairs(v)do rows[#rows+1]=json(tostring(k))..":"..json(x)end end
 return(array and"["or"{")..table.concat(rows,",")..(array and"]"or"}")
end
function this.GetSnapshot(now)
 now=now or lastNow
 local loaded,free,occupied=0,0,0
 if vars.missionCode==30050 then local slots;slots,loaded,free,occupied=scanPool()end
 local rows={};local activeCount,pending,removing=0,0,0
 for _,a in pairs(actors)do
  local present=physical(a)
  if a.phase=="removing"then removing=removing+1 end
  if present and(a.phase=="active"or(a.phase=="removing"and a.removeFromPhase=="active"))then activeCount=activeCount+1
  elseif a.phase=="initializing"or a.phase=="confirming"then pending=pending+1 end
  local staff=validHandle(a)and read(a.id,"GetStaffId")or nil
  rows[#rows+1]={id=a.id,locator=a.locator,name=identity(staff,a.locator),codeName=staffNames[identity(staff,a.locator)],
   nativeStaffId=staff and string.format("%.0f",staff)or nil,phase=a.phase,present=present,
   x=a.x,y=a.y,z=a.z,travelled=a.travelled,route=a.route,reason=a.reason}
 end
 table.sort(rows,function(a,b)return a.locator<b.locator end)
 if vars.missionCode==30050 and now>=nextSavedCount then
  nextSavedCount=now+10;local ok,v=pcall(TppMotherBaseManagement.GetStaffCount);savedCount=ok and v or nil
 end
 return{schema=1,version=this.version,time=now,mission=vars.missionCode,cluster=cluster()+1,
  ready=active(),scope="Command platform 1; ten private test Soldier2 slots",limit=MAX,
  loaded=loaded,free=free,occupied=occupied,managedCount=ownedCount(),activeCount=activeCount,initializing=pending,removing=removing,
  nativeCount=#(NpcSoldiers and NpcSoldiers.GetRoster()or{}),savedRosterCount=savedCount,
  actors=rows,lastCommand=session.lastCommand,commandError=session.commandError,errors=session.errors,
  removal="SetEnabled(false) on owned sol_nlab actors only; saved staff are never dismissed",
  persistence="Test presence resets on mission allocation. Shared needs and ranks are archived by staff identity."}
end
function this.Publish(now)
 local f=io.open(InfCore.paths.mod.."nlab_staff_control_status.json","w")
 if f then f:write(json(this.GetSnapshot(now)));f:close()end
end
function this.Execute(id,action,count,now)
 session.lastCommand=id
 local ok,result,e=pcall(this.Control,action,count,now)
 session.commandError=ok and(result and""or tostring(e))or tostring(result)
 if session.commandError~=""then errorMessage(session.commandError)end
 this.Publish(now);return ok and result,session.commandError
end
local function menu(action,count)
 session.sequence=session.sequence+1
 local ok,e=this.Execute("ihstaff_"..session.sequence,action,count,nowTime())
 if InfCore.DebugPrint then InfCore.DebugPrint(ok and("Test staff: "..ownedCount().."/10")or e)end
 return ok,e
end
function this.AddOne()return menu("add",1)end
function this.RemoveOne()return menu("remove",1)end
function this.AddFive()return menu("add",5)end
function this.FillPool()return menu("count",MAX)end
function this.ClearTests()return menu("clear",0)end
function this.ShowCapacity()
 local s=this.GetSnapshot(nowTime());this.Publish(s.time)
 if InfCore.DebugPrint then InfCore.DebugPrint("Test staff "..s.activeCount.." active, "..s.initializing.." initializing; "..s.free.." free / "..s.loaded.." loaded (max 10)")end
 return s
end
function this.OnAllocateTop()
 session.actors={};actors=session.actors;routes={};nextTick=0;nextPublish=0;nextSavedCount=0;nextNames=0
 -- No stale GameObject handles are mutated while a new mission allocates.
end
function this.Update(checks,now)
 lastNow=now
 if NpcLife and registeredTo~=NpcLife then NpcLife.RegisterProvider("managed_tests",this);registeredTo=NpcLife end
 if now<nextTick then return end;nextTick=now+.5
 if not checks.inGame or not checks.missionCanStart then return end
 if vars.missionCode==30050 and not active()and ownedCount()>0 then
  local list={};for _,a in pairs(actors)do list[#list+1]=a end
  for _,a in ipairs(list)do disable(a)end
 end
 local f=io.open(InfCore.paths.mod.."nlab_staff_command.txt","r")
 if f then
  local text=f:read("*a");f:close()
  local id,action,count=text:match("^([%w_%-]+)%s+([%w_]+)%s+(%d+)%s*$")
  if id and id~=session.lastCommand then this.Execute(id,action,tonumber(count),now)end
 end
 if active()then
  for _,a in pairs(actors)do
   if validHandle(a)then
    if a.phase=="removing"then
     if read(a.id,"GetStatus")==TppGameObject.NPC_STATE_DISABLE then finishDisable(a)
     elseif now-a.removalRequestedAt>5 then
      a.phase=a.removeFromPhase;a.reason="Engine disable confirmation timed out"
      session.commandError=a.reason;errorMessage(a.reason)
     end
    end
    if a.phase=="initializing"and now>=a.activateAt then
     local ok,e=pcall(TppEnemy.SetSoldierType,a.id,EnemyType.TYPE_SOVIET)
     if ok then
      -- Previously verified controller: initialized DD uniform with friendly standard walking AI.
      send(a.id,{id="SetFriendly",enabled=true});send(a.id,{id="SetUnarmed",enabled=true})
      send(a.id,{id="SetSaluteDisable",enabled=true});send(a.id,{id="SetSaluteMoraleDisable",enabled=true})
      a.phase="confirming";roam(a,now)
      send(a.id,{id="SetEnabled",enabled=true,noAssignRoute=true})
     else a.phase="initialization_failed";errorMessage(e);disable(a)end
    end
    if a.phase=="confirming"and physical(a)then
     -- Command-post / DD initialization can assign a staff identity after the pre-enable check.
     if duplicateIdentity(a.id,a.locator)then
      session.commandError="Initialized test actor duplicates an active person's staff identity"
      errorMessage(session.commandError);disable(a,now)
     else a.phase="active"end
    elseif(a.phase=="initializing"or a.phase=="confirming")and now-a.startedAt>10 then
     session.commandError="Engine enable confirmation timed out";errorMessage(session.commandError);disable(a,now)
    end
    local p=position(a.id)
    if p then
     if a.x then local d=math.sqrt((p.x-a.x)^2+(p.y-a.y)^2+(p.z-a.z)^2);a.travelled=a.travelled+d;if d>.03 then a.lastMoved=now end end
     a.x=p.x;a.y=p.y;a.z=p.z
    end
    if a.phase=="active"and physical(a)and read(a.id,"GetLifeStatus")==TppGameObject.NPC_LIFE_STATE_NORMAL then
     if a.target and a.detourUntil and now>=a.detourUntil then route(a,a.target.route,now,a.target.urgency=="muster");a.detourUntil=nil
     elseif a.target and not a.detourUntil and now-a.lastMoved>30 and now-a.assignedAt>30 then
      local target=a.target;roam(a,now);a.target=target;a.lifeControlled=true;a.detourUntil=now+15;a.reason="native navigation retry"
     elseif not a.lifeControlled and now>=a.nextChange then roam(a,now)end
    end
   end
  end
 end
 if now>=nextPublish then this.Publish(now);nextPublish=now+1 end
end
return this