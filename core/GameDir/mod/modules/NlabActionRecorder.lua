-- Standalone Infinite Heaven read-only player observation module and menu.
local this={VERSION="0.1.2",updateRate=0,execState={nextUpdate=0}}
this.registerMenus={"actionRecorderMenu"}
this.actionRecorderMenu={parentRefs={"ImmersiveMotherBase.immersiveMotherBaseMenu"},options={
 "NlabActionRecorder.StartCapture","NlabActionRecorder.MarkCapture",
 "NlabActionRecorder.StopCapture","NlabActionRecorder.ShowCaptureStatus"}}
this.langStrings={eng={actionRecorderMenu="Player action recorder",startCapture="Start action capture (up to 2 minutes)",
 markCapture="Mark current action",stopCapture="Stop and save action capture",showCaptureStatus="Show capture status"},
 help={eng={actionRecorderMenu="Read-only demonstrations: supported state/events, no animation or input replay.",
 startCapture="Starts a new unique trace. Default 5 Hz; automatically stops after 120 real seconds or context loss.",
 markCapture="Adds a numbered timestamp marker. Script calls may supply a descriptive label.",
 stopCapture="Flushes the bounded trace and writes a separate summary. Player controls stay untouched.",
 showCaptureStatus="Reports capture state, samples/events and trace path."}}}
local core,recorder,held,directMotion
local victims,victimCount={},0
local sequence=0
-- Diagnostic-only single take: no native UI notices unless explicitly requested.
local diagnostic={enabled=false,notifications=false,lines=0,bytes=0,path=nil,lastPhase=nil}
local function phase(name)
 if not diagnostic.enabled or not diagnostic.path then return end
 diagnostic.lastPhase=name
 if diagnostic.lines>=64 then diagnostic.capped=true;return end
 local line=string.format("%02d %s\n",diagnostic.lines+1,name):sub(1,96)
 if diagnostic.bytes+#line>8192 then diagnostic.capped=true;return end
 local snapshot=(diagnostic.snapshot or"")..line
 local f,err=io.open(diagnostic.path,"w")
 if not f then diagnostic.error=tostring(err);diagnostic.enabled=false;return end
 local wrote=f:write(snapshot);local closed=f:close()
 if not wrote or not closed then diagnostic.error="milestone write/close failed";diagnostic.enabled=false;return end
 diagnostic.snapshot=snapshot;diagnostic.lines=diagnostic.lines+1;diagnostic.bytes=#snapshot;diagnostic.lastPersistedPhase=name
end
local flagNames={"STAND","SQUAT","CRAWL","STOP","WALK","RUN","DASH","PARALLEL_MOVE",
 "GUN_FIRE","GUN_FIRE_SUPPRESSOR","GUN_RELOAD","ON_VEHICLE","ON_HORSE","DEAD"}
local playerEvents={"CqcHoldStart","CqcThrowAction","PlayerHoldWeapon","OnEquipWeapon","OnEquipItem",
 "OnCrawl","OnElude","PlayerDamaged","PlayerShowerStart","PlayerShowerEnd","DirectMotion","Dead"}
local eventAllowed={};for _,name in ipairs(playerEvents)do eventAllowed[name]=true end
local function scalar(v)
 if type(v)=="number"and v==v and v~=math.huge and v~=-math.huge or type(v)=="boolean"then return v end
 if type(v)=="string"then return v:sub(1,128)end
end
local function readVar(name)
 local ok,value=pcall(function()return vars[name]end)
 if ok then return scalar(value)end
end
local function context()
 if readVar("missionCode")~=30050 or not gvars or gvars.usingNormalMissionSlot~=true then return nil end
 if not MotherBaseStage or type(MotherBaseStage.IsLoading)~="function"
  or type(MotherBaseStage.IsActivating)~="function"then return nil end
 if MotherBaseStage.IsLoading()or MotherBaseStage.IsActivating()then return nil end
 return{missionCode=30050,normalMissionSlot=true}
end
local function sample()
 local flags,unavailable={},{}
 for _,name in ipairs(flagNames)do
  local enum=(PlayerStatusEx and PlayerStatusEx[name])or(PlayerStatus and PlayerStatus[name])
  if enum~=nil and PlayerInfo and type(PlayerInfo.OrCheckStatus)=="function"then
   local ok,value=pcall(PlayerInfo.OrCheckStatus,{enum})
   if ok and type(value)=="boolean"then flags[name]=value else unavailable[#unavailable+1]=name end
  else unavailable[#unavailable+1]=name end
 end
 local stance,count="unavailable",0
 for _,entry in ipairs({{"STAND","standing"},{"SQUAT","crouching"},{"CRAWL","prone"}})do
  if flags[entry[1]]then stance=entry[2];count=count+1 end
 end
 if count>1 then stance="ambiguous flags"end
 local appearance={}
 for _,name in ipairs({"playerType","playerPartsType","playerCamoType","playerFaceEquipId","playerHandType"})do
  appearance[name]=readVar(name)
 end
 return{position={x=readVar("playerPosX"),y=readVar("playerPosY"),z=readVar("playerPosZ")},
  orientation={yawDegrees=readVar("playerRotY"),pitch="unavailable",roll="unavailable"},
  appearance=appearance,equipmentSelection={inventorySlot=readVar("currentInventorySlot"),
   itemIndex=readVar("currentItemIndex"),supportWeaponIndex=readVar("currentSupportWeaponIndex")},
  heldEquipment=held or{availability="unavailable until equip/hold event in this take"},
  statusFlags=flags,unavailableStatusFlags=unavailable,
  stance={value=stance,derivedFrom="exposed STAND/SQUAT/CRAWL flags; not an animation ID"},
  animation={availability="unavailable",reason="no verified current clip/animation-ID getter in this capture route"},
  lastDirectMotionEvent=directMotion,gameClockSeconds=readVar("clock")}
end
local function exists(path)
 local f=io.open(path,"rb");if not f then return false end;f:close();return true
end
local function outputDirectory()
 assert(InfCore and InfCore.paths and type(InfCore.paths.mod)=="string","IH mod path unavailable")
 return InfCore.paths.mod.."nlab/action-recordings/"
end
local function allocate(now)
 -- Root prepares this directory. Never invokes a shell/mkdir or chooses caller-controlled paths.
 local root=outputDirectory()
 local stamp="raw";if os and type(os.date)=="function"then
  local ok,value=pcall(os.date,"!%Y%m%d-%H%M%S");if ok then stamp=value end
 end
 local id,trace,summary
 for attempt=1,100 do
  sequence=sequence+1
  id=string.format("nlab-actions-%s-%d-%04d",stamp,math.floor(now*1000),sequence)
  trace=root..id..".trace.jsonl";summary=root..id..".summary.json"
  if not exists(trace)and not exists(summary)and not exists(root..id..".milestones.txt")then break end
  id=nil
 end
 assert(id,"unique trace namespace exhausted")
 -- A single IH module instance owns this namespace; Lua51 has no portable exclusive-create mode.
 -- Existing files are checked before write; a competing external writer is unsupported.
 diagnostic.path=diagnostic.enabled and(root..id..".milestones.txt")or nil
 phase("allocate.trace_open.before")
 local f=assert(io.open(trace,"wb"),"capture directory unavailable")
 phase("allocate.trace_open.after")
 return{takeId=id,tracePath=trace,summaryPath=summary,
  write=function(chunk)
   phase("stream.write.before");local ok=f:write(chunk);phase("stream.write.after")
   -- Diagnostic0.1.2: no f:flush. Small writes may remain buffered until close.
   phase("stream.flush.skipped")
   return ok~=nil
  end,
  close=function()
   phase("stream.close.before");local ok=f:close();phase("stream.close.after");return ok~=nil
  end,
  summary=function(text)
   if exists(summary)then return false end
   local sf=io.open(summary,"wb");if not sf then return false end
   phase("summary.write.before");local ok=sf:write(text);local closed=sf:close()
   phase("summary.write.after");return ok~=nil and closed~=nil
  end}
end
local function ensure()
 if recorder then return recorder end
 core=assert(loadfile(InfCore.paths.mod.."nlab/ActionRecorderCore.lua"))()
 recorder=core.New{now=function()return Time.GetRawElapsedTimeSinceStartUp()end,
  context=context,phase=phase,sample=function()
   diagnostic.samples=(diagnostic.samples or 0)+1
   if diagnostic.samples==1 then phase("first_sample.before")end
   local value=sample()
   if diagnostic.samples==1 then phase("first_sample.after")end
   return value
  end,allocate=allocate,capabilities={
   position="vars.playerPosX/Y/Z (world root, not bones)",orientation="vars.playerRotY degrees only",
   appearance="exposed vars codes; no saved-staff identity",
   equipment="selection vars + observed equip/hold event IDs; initial held weapon may be unknown",
   state="selected PlayerInfo status flags; stance is labeled derivation",
   animationId="unavailable",motionFilename="unavailable",boneTransforms="unavailable",
   inputStream="not captured",directMotion="raw event hashes/stage only if emitted",
   events="12 Player + 2 CQC-victim lifecycle message types only",
   replay="unsupported; player controller is not Soldier2 or Hostage2"}}
 return recorder
end
local function notice(message)
 this.lastNotice=message:sub(1,180) -- Cached feedback; no native notification by default.
 phase("notice.before")
 if diagnostic.notifications and InfMenu and type(InfMenu.Print)=="function"then
  phase("notice.native.before");InfMenu.Print(message);phase("notice.native.after")
 else phase("notice.skipped")end
 phase("notice.after")
end
function this.GetStatus()
 local status=recorder and recorder.Status()or{active=false}
 status.lastNotice=this.lastNotice
 status.diagnostic={enabled=diagnostic.enabled,notifications=diagnostic.notifications,path=diagnostic.path,
  lines=diagnostic.lines,bytes=diagnostic.bytes,capped=diagnostic.capped,lastPhase=diagnostic.lastPhase,lastPersistedPhase=diagnostic.lastPersistedPhase,error=diagnostic.error}
 return status
end
function this.StartCapture(options)
 if recorder and recorder.active then return false,"capture already active"end
 diagnostic={enabled=type(options)=="table"and options.diagnostics==true,
  notifications=type(options)=="table"and options.notifications==true,lines=0,bytes=0,path=nil,lastPhase=nil}
 local ok,started,detail=pcall(function()return ensure().Start(options)end)
 if not ok then notice("Capture could not start: "..tostring(started));return false,tostring(started)end
 if started then
  held=nil;directMotion=nil;victims={};victimCount=0
  notice("Recording: "..recorder.Status().tracePath)
 else notice("Capture start rejected: "..tostring(detail))end
 phase("start.returning")
 return started,detail
end
function this.StopCapture(reason)
 if not recorder then return false,"no active capture"end
 local ok,value=recorder.Stop(type(reason)=="string"and reason or"manual stop")
 if ok then notice("Saved action trace: "..value.tracePath)end
 return ok,value
end
function this.MarkCapture(label)
 if not recorder then return false,"no active capture"end
 return recorder.Mark(type(label)=="string"and label or nil)
end
function this.ShowCaptureStatus()
 local s=this.GetStatus()
 notice(s.active and("Recording "..s.samples.." samples / "..s.events.." events: "..s.tracePath)
  or("Recorder idle"..(s.last and("; last: "..s.last.tracePath.." ("..s.last.reason..")")or"")))
 return s
end
function this.ObserveEvent(class,message,a,b,c,d)
 if not recorder or not recorder.active then return false end
 if class=="Player"then
  if not eventAllowed[message]then return false end
  if message=="CqcHoldStart"or message=="CqcThrowAction"then
   if type(b)=="number"and b>=0 and b<65535 and b==math.floor(b)and not victims[b]and victimCount<4 then
    victims[b]=true;victimCount=victimCount+1
   end
  elseif message=="PlayerHoldWeapon"then
   held={availability="observed event",equipId=scalar(a),equipType=scalar(b),sourceEvent=message,
    currentValueGuaranteed=false}
  elseif message=="OnEquipWeapon"or message=="OnEquipItem"then
   held={availability="observed equip event; not proof currently held",equipId=scalar(b),
    inventorySlot=scalar(c),sourceEvent=message}
  elseif message=="DirectMotion"then
   directMotion={nameHash=scalar(a),stageHash=scalar(b),finished=scalar(c),
    semantics="last raw event, not proof current clip/pose"}
  end
 elseif class=="GameObject"then
  if not victims[a]or(message~="Conscious"and message~="Unconscious")then return false end
 else return false end
 return recorder.Event(class,message,{arg0=a,arg1=b,arg2=c,arg3=d})
end
function this.Messages()
 local messages={Player={},GameObject={}}
 for _,name in ipairs(playerEvents)do
  local message=name
  messages.Player[#messages.Player+1]={msg=message,func=function(a,b,c,d)this.ObserveEvent("Player",message,a,b,c,d)end}
 end
 for _,name in ipairs({"Conscious","Unconscious"})do
  local message=name
  messages.GameObject[#messages.GameObject+1]={msg=message,func=function(a,b,c,d)this.ObserveEvent("GameObject",message,a,b,c,d)end}
 end
 return Tpp.StrCode32Table(messages)
end
function this.Init()this.messageExecTable=Tpp.MakeMessageExecTable(this.Messages())end
function this.OnMessage(sender,messageId,a,b,c,d,log)
 if not recorder or not recorder.active then return end
 Tpp.DoMessage(this.messageExecTable,TppMission.CheckMessageOption,sender,messageId,a,b,c,d,log)
end
function this.Update()
 if recorder and recorder.active then recorder.Tick()end
end
function this.OnAllocateTop()
 if recorder and recorder.active then recorder.Stop("mission allocation")end
end
function this.OnReload()
 if recorder and recorder.active then recorder.Stop("mission reload")end
 this.Init()
end
function this.PostModuleReload(previous)
 if previous and previous.StopCapture then previous.StopCapture("IH module reload")end
 this.Init() -- New module hot-reload also needs its own independent message table.
end
return this