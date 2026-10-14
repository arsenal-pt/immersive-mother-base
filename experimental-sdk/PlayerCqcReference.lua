-- Bounded read-only player CQC reference capture. No commands, camera or input mutations.
local P={};local run
local function encode(v)
 local t=type(v);if t=="nil"then return"null"end
 if t=="number"or t=="boolean"then return tostring(v)end
 if t=="string"then return'"'..v:gsub("\\","\\\\"):gsub('"','\\"'):gsub("\n","\\n")..'"'end
 local out={};for k,x in pairs(v)do out[#out+1]=encode(tostring(k))..":"..encode(x)end
 return"{"..table.concat(out,",").."}"
end
local function safe()return vars.missionCode==30050 and gvars.usingNormalMissionSlot==true and not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()end
local function publish(r)
 local f=assert(io.open(InfCore.paths.mod.."nlab_cqc_reference_status.json","w"));f:write(encode(r));f:close();return r
end
local function pos(id)local v=GameObject.SendCommand(id,{id="GetPosition"});return{x=v:GetX(),y=v:GetY(),z=v:GetZ()}end
function P.Status()
 return publish(run and{active=true,started=run.started,deadline=run.deadline,samples=#run.samples,events=#run.events}
  or{active=false,last=P.last})
end
function P.Stop(reason)
 if not run then return P.Status()end;local r=run;run=nil
 if NpcLife.Update==r.wrapper then NpcLife.Update=r.update end
 local detached=true
 for _,b in ipairs(r.listeners)do
  if b.class[b.message]==b.installed then b.class[b.message]=b.previous else detached=false end
 end
 local result={schema=1,started=r.started,ended=Time.GetRawElapsedTimeSinceStartUp(),reason=reason or"manual stop",
  events=r.events,samples=r.samples,participants=r.participants,cleanupComplete=detached and NpcLife.Update==r.update,
  readOnly=true,playerControlsUntouched=true,cameraUntouched=true,internalMotionFilenamesObserved=false}
 local f=assert(io.open(r.output,"w"));f:write(encode(result));f:close()
 P.last={output=r.output,events=#r.events,samples=#r.samples,cleanupComplete=result.cleanupComplete,reason=result.reason}
 return P.Status()
end
function P.Start(output,duration)
 assert(not run and safe(),"requires normal Mother Base and no active capture")
 assert(type(output)=="string"and not output:find("..",1,true),"invalid output path")
 duration=duration or 90;assert(duration>=10 and duration<=120,"capture is bounded to two minutes")
 local r={started=Time.GetRawElapsedTimeSinceStartUp(),samples={},events={},participants={},tracked={},listeners={},
  nextSample=0,nextStatus=0,update=NpcLife.Update,output=output}
 r.deadline=r.started+duration;run=r
 local candidates={}
 for _,a in ipairs(NpcSoldiers.GetRoster())do
  local p=pos(a.id);candidates[#candidates+1]={id=a.id,staff=a.nativeStaffId,name=a.codeName,
   distance=(p.x-vars.playerPosX)^2+(p.z-vars.playerPosZ)^2}
 end
 table.sort(candidates,function(a,b)return a.distance<b.distance end)
 for i=1,math.min(3,#candidates)do local a=candidates[i];r.tracked[a.id]=a.staff;r.participants[#r.participants+1]=a end
 local function record(class,message,a,b,c,d)
  if run~=r or #r.events>=128 then return end
  if class=="Player"and type(b)=="number"and b>0 and b<65535 and not r.tracked[b]then
   local ok,staff=pcall(GameObject.SendCommand,b,{id="GetStaffId"})
   if ok and type(staff)=="number"then r.tracked[b]=staff end
  end
  if class=="GameObject"and not r.tracked[a]then return end
  r.events[#r.events+1]={time=Time.GetRawElapsedTimeSinceStartUp(),class=class,message=message,a=a,b=b,c=c,d=d}
 end
 -- Preserve the whole dispatch entry and its sender callbacks; append only the general observer.
 local registry=assert(InfMain.messageExecTable)
 for className,names in pairs({Player={"CqcHoldStart","CqcThrowAction"},GameObject={"TapCqc","Damage","Unconscious","Conscious","SpecialActionEnd"}})do
  local classHash=InfCore.StrCode32(className);registry[classHash]=registry[classHash]or{};local class=registry[classHash]
  for _,name in ipairs(names)do
   local message=InfCore.StrCode32(name);local previous=class[message];local entry={}
   for k,v in pairs(previous or{})do entry[k]=v end
   local old=entry.func;local label,category=name,className
   entry.func=function(a,b,c,d)
    local ok,e=pcall(record,category,label,a,b,c,d);if not ok then r.observerError=tostring(e)end
    if old then return old(a,b,c,d)end
   end
   class[message]=entry;r.listeners[#r.listeners+1]={class=class,message=message,previous=previous,installed=entry}
  end
 end
 r.wrapper=function(checks,now)
  r.update(checks,now);if run~=r then return end
  local current=Time.GetRawElapsedTimeSinceStartUp()
  if not safe()or current>=r.deadline or #r.samples>=1200 or r.observerError then P.Stop(r.observerError or(not safe()and"context changed"or"deadline"));return end
  if current<r.nextSample then return end;r.nextSample=current+.1
  local row={time=current,player={x=vars.playerPosX,y=vars.playerPosY,z=vars.playerPosZ,yaw=vars.playerRotY},actors={}}
  local count=0
  for id,staff in pairs(r.tracked)do
   count=count+1;if count>6 then break end
   local ok,v=pcall(function()
    if GameObject.SendCommand(id,{id="GetStaffId"})~=staff then return{identityChanged=true}end
    return{position=pos(id),action=GameObject.SendCommand(id,{id="GetActionStatus"}),
     life=GameObject.SendCommand(id,{id="GetLifeStatus"}),flags=GameObject.SendCommand(id,{id="GetStateFlag"})}
   end)
   row.actors[tostring(id)]=ok and v or{error=tostring(v)}
  end
  r.samples[#r.samples+1]=row
  if current>=r.nextStatus then r.nextStatus=current+1;P.Status()end
 end
 NpcLife.Update=r.wrapper;return P.Status()
end
return P
