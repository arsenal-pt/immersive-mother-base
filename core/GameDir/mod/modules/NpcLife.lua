-- Engine adapter for the shared daily-life core. NPCs only; no player input/camera control.
local this={updateRate=0,execState={nextUpdate=0}}
this.registerMenus={"npcLifeMenu"}
this.npcLifeMenu={parentRefs={"ImmersiveMotherBase.immersiveMotherBaseMenu"},options={
 "NpcLife.MusterNow","NpcLife.GatherNow","NpcLife.ToiletQueue","NpcLife.ShowerQueue","NpcLife.RoamNow","NpcLife.ToggleAutonomy"}}
this.langStrings={eng={npcLifeMenu="Mother Base daily life",musterNow="Muster (route resource pending)",gatherNow="Gather (route resource pending)",
 toiletQueue="Toilet queue (resource pending)",showerQueue="Shower queue (resource pending)",roamNow="Dismiss and roam",toggleAutonomy="Toggle personal routines"},
 help={eng={npcLifeMenu="Shared needs, roles and daily activities. Facility pads are temporary prototype locations."}}}
local core,layout,world,registry,registryApi
local providers={}
local serviceApi,serviceCatalog,legacyFacilities,serviceStatus,nextServiceRefresh=nil,nil,nil,{},0
local servicePilot,lastPilot
local hierarchyApi,hierarchy
local cqcTraining
local conversations={};local nextHierarchy=0;local nextDialogue=0;local dialogueHistory={}
function this.RegisterProvider(key,adapter)providers[key]=adapter;if registry then registryApi.AddProvider(registry,key,adapter)end end
local nextUpdate,nextSave,nextPublish,lastNow=0,0,0,0
local errors={}
local lastCommand,lastCommandError="none",""
-- Ignore commands from an earlier run/reload; only a new command id is executed.
local previousCommand=io.open(InfCore.paths.mod.."nlab_life_command.txt","r")
if previousCommand then
 local data=previousCommand:read("*a");previousCommand:close()
 lastCommand=data:match("^([%w_%-]+)%s+")or "none"
end
local function serialize(v,lua)
 local t=type(v)
 if t=="nil"then return lua and "nil"or "null"end
 if t=="boolean"or t=="number"then return tostring(v)end
 if t=="string"then
  if lua then return string.format("%q",v)end
  return '"'..v:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r'):gsub('\t','\\t')..'"'
 end
 if t~="table"then return serialize(tostring(v),lua)end
 local count,max=0,0;local array=true
 for k in pairs(v)do count=count+1;if type(k)~="number"or k<1 or k%1~=0 then array=false else max=math.max(max,k)end end
 array=array and max==count
 local rows={}
 if array then for i=1,count do rows[#rows+1]=serialize(v[i],lua)end
 else for k,val in pairs(v)do rows[#rows+1]=(lua and "["..serialize(k,true).."]="or serialize(tostring(k),false)..":")..serialize(val,lua)end end
 return (lua and "{"or(array and "["or "{"))..table.concat(rows,",")..(lua and "}"or(array and "]"or "}"))
end
local function write(path,data)local f=io.open(path,"w");if f then f:write(data);f:close();return true end;return false end
local function active()return vars.missionCode==30050 and gvars.usingNormalMissionSlot==true and MotherBaseStage.GetCurrentCluster()<7 end
local function save()
 if world then local saved=core.Save(world);write(InfCore.paths.mod.."nlab/imb-life-save.lua","return "..serialize(saved,true))end
 if hierarchy then write(InfCore.paths.mod.."nlab/imb-native-ranks.lua","return "..serialize(hierarchyApi.Save(hierarchy),true))end
end
local function apply(actions,now)
 for _,action in ipairs(actions)do
  if cqcTraining then cqcTraining.CancelForAction(action)end
  local ok,e=pcall(registryApi.Apply,registry,action,now)
  if not ok and #errors<32 then errors[#errors+1]=tostring(e)end
 end
end
local function serviceContext()
 local cluster=MotherBaseStage.GetCurrentCluster()+1
 return {missionCode=vars.missionCode,normalSlot=gvars.usingNormalMissionSlot==true,
  cluster=cluster,completedGrade=TppLocation.GetMbStageClusterGrade(cluster),
  layoutCode=MotherBaseStage.GetCurrentLayout(),routeHashValidated=serviceCatalog.routeHashValidated==true,
  validatedRoutes=serviceCatalog.validatedRoutes or{},
  ready=not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()}
end
-- Service locations are resolved at low frequency from completed native platforms.
-- The private catalog contains owned-game route coordinates; it is not distributed.
local function refreshServices(now,force)
 if not serviceApi or not layout or(not force and now<nextServiceRefresh)then return end
 nextServiceRefresh=now+2
 local ok,definitions,status=pcall(function()
  local context=serviceContext()
  local defs,status=serviceApi.Build(context,serviceCatalog)
  if servicePilot then
   context.validationMode=true
   local candidates,candidateStatus=serviceApi.Build(context,serviceCatalog)
   local cfg=candidates[servicePilot.key]
   assert(cfg and cfg.enabled,"pilot binding became unavailable")
   cfg.allowActors={[servicePilot.actor]=true};cfg.travelTimeoutReal=servicePilot.deadline-servicePilot.started
   defs[servicePilot.key]=cfg
   status.productionEnabledCount=status.enabledCount
   status.enabledCount=status.enabledCount+1;status.ready=true;status.validationMode=true
   status.reason="One-actor controlled service pilot; production validation unchanged"
   status.facilities[servicePilot.key]=candidateStatus.facilities and candidateStatus.facilities[servicePilot.key]or{enabled=true,bindingState="validation_only"}
  end
  return defs,status
 end)
 if not ok then
  if #errors<32 then errors[#errors+1]="service bindings: "..tostring(definitions)end
  definitions={};status={enabled=false,reason="native service context unavailable"}
 end
 serviceStatus=status or {}
 local merged={};for key,value in pairs(legacyFacilities or{})do merged[key]=value end
 for key,value in pairs(definitions or{})do merged[key]=value end
 if world then apply(core.SyncFacilities(world,merged,now),now)else layout.facilities=merged end
end
local function initialize(now)
 if world then return true end
 if not active()then return false end
 registryApi=assert(loadfile(InfCore.paths.mod.."nlab/NpcRegistry.lua"))()
 registry=registryApi.Create()
 if NpcSoldiers then registryApi.AddProvider(registry,"soldiers",NpcSoldiers)end
 for key,adapter in pairs(providers)do registryApi.AddProvider(registry,key,adapter)end
 local roster=registryApi.Collect(registry);if #roster==0 then return false end
 core=assert(loadfile(InfCore.paths.mod.."nlab/NpcLifeCore.lua"))()
 layout=assert(loadfile(InfCore.paths.mod.."nlab/LifeLayout.lua"))()
 local saved
 local fn=loadfile(InfCore.paths.mod.."nlab/imb-life-save.lua")
 if fn then local ok,s=pcall(fn);if ok then saved=s end end
 local profile=assert(loadfile(InfCore.paths.mod.."nlab/StaffConfig.lua"))()
 layout.nativeMode=profile.nativeMode;layout.version="0.1.21";layout.autonomousDuties=true
  layout.strictNativeObservations=profile.nativeMode;layout.deferUnboundNeeds=profile.nativeMode
  layout.allowConcurrentLocalServices=true;legacyFacilities=layout.facilities
  serviceStatus={ready=false,enabledCount=0,reason="Private service catalog excluded; local generation and native acceptance pending"}
  refreshServices(now,true)
 hierarchyApi=assert(loadfile(InfCore.paths.mod.."nlab/NativeHierarchy.lua"))()
 local hf=loadfile(InfCore.paths.mod.."nlab/imb-native-ranks.lua");local hs;if hf then local ok,v=pcall(hf);if ok then hs=v end end
 hierarchy=hierarchyApi.Create(hs)
 world=core.Create(layout,roster,TppClock.GetTime("number"),saved);world.realNow=now;apply(world.actions,now)
 local trainingApi=assert(loadfile(InfCore.paths.mod.."nlab/NativeCqcTraining.lua"))()
 local proof=assert(loadfile(InfCore.paths.mod.."nlab/CqcTrainingProof.lua"))()
 cqcTraining=trainingApi.Create(core,world,layout,NpcSoldiers,proof)
 TppClock.Start();nextSave=now+30
 return true
end
function this.OnAllocateTop()if cqcTraining then cqcTraining.Stop("allocation");cqcTraining=nil end;if servicePilot then this.EndServicePilot("allocation",lastNow)end;save();world=nil;core=nil;layout=nil;registry=nil;serviceApi=nil;serviceCatalog=nil;legacyFacilities=nil;serviceStatus={};nextServiceRefresh=0;nextUpdate=0;nextPublish=0;errors={}end
function this.Command(command,now)
 now=now or lastNow
 assert(initialize(now),"daily life requires registered Mother Base staff")
 if command=="muster"or command=="gather"then assert(layout.assembliesAvailable~=false,layout.assemblyUnavailableReason)end
 if command=="cqc"or command=="cqc_verify"or command=="cqc_four"then
  local roster,observations=registryApi.Collect(registry)
  cqcTraining.Start(roster,observations,command=="cqc_four"and 4 or 6,command=="cqc_verify",command~="cqc_verify")
  nextPublish=0;return
 elseif command=="cqc_stop"then cqcTraining.Stop("manual cancellation");nextPublish=0;return
 elseif command=="cqc_auto"then cqcTraining.ToggleAutomatic();nextPublish=0;return end
 if cqcTraining then cqcTraining.Stop("manual routine: "..command)end
 local r={kind=command}
 if command=="toilet"or command=="shower"or command=="mess"or command=="water"or command=="bunk"then
  assert(serviceStatus.ready==true,"Requested service is unavailable in this source candidate");r={kind="facility",facility=command}
 elseif command=="duty"then r={kind="native_duty",duty="patrol",reason="leader assigned patrol",durationSeconds=90}
 elseif command=="guard"then r={kind="native_duty",duty="guard",reason="leader assigned guard posts",durationSeconds=120}
  elseif command=="autonomy"then r={kind="autonomy",enabled=not world.autonomousNeeds}
 elseif command=="morning_test"or command=="evening_test"then
  local seconds=command=="morning_test"and 21580 or 64780
  TppClock.SetTime(command=="morning_test"and "05:59:40"or "17:59:40")
  core.RebaseClock(world,seconds);TppClock.Start();nextPublish=0;return
 end
 apply(core.Request(world,r,TppClock.GetTime("number"),now),now)
 nextPublish=0;save()
end
function this.Request(request,now)
 now=now or lastNow;assert(initialize(now),"daily life requires registered staff")
 if request.kind=="muster"or request.kind=="gather"then assert(layout.assembliesAvailable~=false,layout.assemblyUnavailableReason)end
 apply(core.Request(world,request,TppClock.GetTime("number"),now),now);nextPublish=0;save()
end

-- Explicit bounded native proof only. The ordinary catalog validation flags are never changed.
function this.BeginServicePilot(actor,service,timeout,now)
 now=now or lastNow;timeout=timeout or 300
 assert(world,"daily life requires initialized staff")
 assert(not world.assemblyReservation,"Another activity reserves the assembly pad")
 assert(not servicePilot,"service pilot already active")
 assert(world and serviceApi and serviceCatalog,"native services unavailable")
 assert(type(now)=="number"and now==now and math.abs(now-lastNow)<=1,"stale core heartbeat")
 assert(type(timeout)=="number"and timeout==timeout and timeout>=10 and timeout<=300,"invalid pilot timeout")
 assert(service=="water","only the water pilot has approved endpoint evidence")
 local context=serviceContext()
 assert(context.missionCode==30050 and context.normalSlot and context.ready and context.cluster==1 and context.layoutCode==3 and context.completedGrade>=2,"unsafe pilot context")
 assert(not(world.facilities.command_2_water and world.facilities.command_2_water.config.enabled),"water is already verified; use the ordinary service request")
 assert(not world.group,"finish the active assembly before a service pilot")
 local selected
 for _,person in ipairs(NpcSoldiers.GetRoster())do if person.id==actor and person.native~=false then selected=person;break end end
 local o=NpcSoldiers.GetObservations()[actor]
 assert(selected and selected.cluster==1 and selected.platform==1 and o and o.real==true and o.available==true and o.alive~=false,"fresh native actor unavailable")
 for _,key in ipairs({"x","y","z"})do assert(type(o[key])=="number"and o[key]==o[key]and math.abs(o[key])<math.huge,"native position unavailable")end
 local a=world.actors[actor]
 assert(a and a.name==selected.name and a.nativeStaffId==selected.nativeStaffId,"stale native identity")
 context.validationMode=true
 local defs=serviceApi.Build(context,serviceCatalog);local key="command_2_"..service
 assert(defs[key]and defs[key].enabled,"service candidate unavailable")
 servicePilot={actor=actor,name=a.name,staffId=a.nativeStaffId,key=key,started=now,deadline=now+timeout,
  autonomyNeeds=world.autonomousNeeds,autonomySocial=world.autonomousSocial}
 world.autonomousNeeds=false;world.autonomousSocial=false
 local ok,e=pcall(refreshServices,now,true)
 if not ok or not(world.facilities[key]and world.facilities[key].config.enabled)then
  this.EndServicePilot("begin failed",now);error(e or"pilot binding rejected")
 end
 nextPublish=0;return this.GetSnapshot().servicePilot
end
function this.EndServicePilot(reason,now)
 local old=servicePilot;if not old then return false end
 now=now or lastNow;servicePilot=nil
 if world then
  world.autonomousNeeds=old.autonomyNeeds;world.autonomousSocial=old.autonomySocial
  refreshServices(now,true)
  -- SyncFacilities retires an active visit. Do not dismiss a newer muster/gathering here.
 end
 lastPilot={reason=reason or"manual cleanup",ended=now};nextPublish=0;save();return true
end
local function pilotGuard(roster,observations,now)
 if not servicePilot then return end
 local p=servicePilot;local a=world.actors[p.actor];local current
 for _,person in ipairs(roster)do if person.id==p.actor then current=person;break end end
 local o=observations[p.actor]
 local safe=active()and gvars.usingNormalMissionSlot==true and MotherBaseStage.GetCurrentLayout()==3
  and not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()and TppLocation.GetMbStageClusterGrade(1)>=2
 if now>=p.deadline or not safe or world.group or not current or current.name~=p.name or current.nativeStaffId~=p.staffId
  or not a or a.name~=p.name or not o or o.real~=true or o.available~=true or o.alive==false then
  this.EndServicePilot(now>=p.deadline and"pilot timeout"or"pilot context or actor interrupted",now)
 end
end
local function addPilotStatus(s)
 if servicePilot then s.servicePilot={actor=servicePilot.actor,facility=servicePilot.key,started=servicePilot.started,deadline=servicePilot.deadline,productionEnabled=false}end
 s.lastServicePilot=lastPilot;return s
end

function this.MusterNow()this.Command("muster")end
function this.GatherNow()this.Command("gather")end
function this.ToiletQueue()this.Command("toilet")end
function this.ShowerQueue()this.Command("shower")end
function this.RoamNow()this.Command("roam")end
function this.ToggleAutonomy()this.Command("autonomy")end
function this.Update(checks,now)
 lastNow=now
 if not active()or not checks.inGame or not checks.missionCanStart then
  if cqcTraining then cqcTraining.Stop("game context left")end
  if servicePilot then this.EndServicePilot("game context left",now)end;return
 end
 if now<nextUpdate then return end;nextUpdate=now+.25
 if not initialize(now)then return end
 local f=io.open(InfCore.paths.mod.."nlab_life_command.txt","r")
 if f then
  local text=f:read("*a");f:close()
  local id,command=text:match("^([%w_%-]+)%s+([%w_]+)%s*$")
  if id and id~=lastCommand then
   lastCommand=id
   local ok,e=pcall(this.Command,command,now)
   lastCommandError=ok and ""or tostring(e)
   if not ok and #errors<32 then errors[#errors+1]=lastCommandError end
  end
 end
 if NpcSoldiers and not registry.providers.soldiers then registryApi.AddProvider(registry,"soldiers",NpcSoldiers)end
 local roster,observations=registryApi.Collect(registry)
 pilotGuard(roster,observations,now)
 refreshServices(now)
  apply(core.SyncRoster(world,roster,now),now)
 local entry=layout.facilities.shower and layout.facilities.shower.enabled~=false and layout.facilities.shower.entry
 local available=true
 if entry then
  local dx,dz=vars.playerPosX-entry.x,vars.playerPosZ-entry.z
  -- Leave the real player's shower interaction and entrance priority intact.
  available=dx*dx+dz*dz>1.2*1.2
  local ok,busy=pcall(function()return PlayerInfo.OrCheckStatus{PlayerStatusEx.SHOWER,PlayerStatusEx.TOILET_DOOR}end)
  if ok and busy and dx*dx+dz*dz<9 then available=false end
 end
 apply(core.Step(world,TppClock.GetTime("number"),now,observations,{shower=available}),now)
 if cqcTraining then local ok,e=pcall(cqcTraining.Update,roster,observations);if not ok then cqcTraining.Stop("coordinator error");if #errors<32 then errors[#errors+1]=tostring(e)end end end
 if now>=nextHierarchy then hierarchyApi.Sync(hierarchy,roster,observations);nextHierarchy=now+2 end
 -- Dialogue uses the authoritative group; full dashboard snapshots are sampled separately.
 local group=world.group
 if now>=nextDialogue and group and group.kind=="GATHERING"then
  local started=false
  for _,g in ipairs(group.groups or{})do if g.phase=="talking"and #g.ids>=2 then
   local a,b=observations[g.ids[1]],observations[g.ids[2]]
   if a and b and a.available and b.available and a.conversationSupported~=false and b.conversationSupported~=false and (a.x-b.x)^2+(a.z-b.z)^2<16 and math.abs(a.y-b.y)<1 then
    local label=({"MB_story_03","MB_story_07","MB_story_08","MB_story_18"})[(#dialogueHistory%4)+1]
    local ok,e=pcall(GameObject.SendCommand,g.ids[1],{id="CallConversation",label=label,friend=g.ids[2]})
    dialogueHistory[#dialogueHistory+1]={time=now,label=label,speaker=g.ids[1],partner=g.ids[2],accepted=ok,error=not ok and tostring(e)or nil}
    if #dialogueHistory>32 then table.remove(dialogueHistory,1)end
    nextDialogue=now+55;started=true;break
   end
  end end
  if not started then nextDialogue=now+5 end
 end
 if now>=nextPublish then
  nextPublish=now+.5
  local s=addPilotStatus(core.Snapshot(world));s.cqcTraining=cqcTraining and cqcTraining.Snapshot();s.hierarchy=hierarchyApi.Snapshot(hierarchy);s.dialogues=dialogueHistory;s.nativeProfile=true;s.serviceCoverage=serviceStatus;s.pilotScope="Command platform 1 assemblies; platform-local daily service prototypes follow verified bindings";s.errors=errors;s.playerControlsFree=true;s.commanderRemainsPlayer=true;s.lastCommand=lastCommand;s.commandError=lastCommandError
 s.player={x=vars.playerPosX,y=vars.playerPosY,z=vars.playerPosZ,yaw=vars.playerRotY,
  cameraYaw=vars.playerCameraRotation[1],cameraPitch=vars.playerCameraRotation[0]}
 local data=serialize(s,false)
 write(InfCore.paths.mod.."nlab_life_status.json",data)
 end -- one canonical status feed at 2 Hz; simulation remains 4 Hz
 if now>=nextSave then save();nextSave=now+30 end
end
function this.GetSnapshot()if not world then return end;local s=addPilotStatus(core.Snapshot(world));s.serviceCoverage=serviceStatus;s.cqcTraining=cqcTraining and cqcTraining.Snapshot();s.hierarchy=hierarchyApi and hierarchyApi.Snapshot(hierarchy);return s end
return this
