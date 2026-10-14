-- Bounded CQC sessions. The caller supplies monotonic real seconds, never TppClock.
-- Native placement, motion chains and duty restoration belong to a verified port.
local M={version="0.3.0",maximumPairs=3,minimumTrainingSeconds=300}
local function invoke(port,name,...)
 local ok,value=pcall(port[name],...)
 if not ok then return nil,name..": "..tostring(value)end
 return value
end
local function finite(v)return type(v)=="number"and v==v and math.abs(v)<math.huge end
function M.New(planner,actors,port,config)
 config=config or{}
 local technique=config.motionMode=="technique"
 assert((technique and config.techniquePlaybackVerified==true or(not technique and config.pairedPlaybackVerified==true))
  and config.reversibleOwnershipVerified==true,
  "the selected motion mode and reversible ownership must be verified before running")
 assert(config.clockKind=="monotonic-real-seconds","unscaled real clock required")
 assert(type(config.drillId)=="string"and #config.drillId>0 and #config.drillId<=48,"bounded unique drill epoch required")
 for _,name in ipairs({"ContextSafe","Observe","Capture","Acquire","Arrange","Play","Release","CommandId"})do
  assert(type(port[name])=="function","missing port: "..name)
 end
 local plan=planner.Build(actors,config.layoutMode or"parallel")
 assert(plan.mode==(config.layoutMode or"parallel")and type(plan.placements)=="table"and #plan.placements==#plan.rounds,
  "training formation planner required")
 local roster={};for _,a in ipairs(actors)do roster[#roster+1]={id=a.id,identity=a.identity}end
 actors=roster
 local session={state="IDLE",round=0,roundSerial=0,completedRounds=0,completedCycles=0,plan=plan,
  leases={},commands={},usedCommands={},ends={},cleanupErrors={},nextPoll=0}
 local alignSeconds=config.alignSeconds or 90;local playSeconds=config.playSeconds or 12
 local restSeconds=config.restSeconds or 1;local trainingSeconds=config.trainingSeconds or 300
 assert(finite(alignSeconds)and alignSeconds>=1 and alignSeconds<=180 and finite(playSeconds)and playSeconds>=3 and playSeconds<=12
  and finite(restSeconds)and restSeconds>=0 and restSeconds<=5,"bounded phase timing required")
 assert(finite(trainingSeconds)and trainingSeconds>=300 and trainingSeconds<=900,"training requires at least five real minutes")
 local totalSeconds=config.totalSeconds or(alignSeconds+trainingSeconds+300)
 assert(finite(totalSeconds)and totalSeconds>=alignSeconds+trainingSeconds+playSeconds and totalSeconds<=1800,
  "separate assembly/training/recovery deadline required")
 session.trainingSeconds=trainingSeconds
 local function observe(phase)
  local all=true
  for _,a in ipairs(actors)do
   local o,e=invoke(port,"Observe",a.id,a.identity,phase)
   if type(o)~="table"or o.identity~=a.identity or o.available~=true or o.supported~=true then return false,e or"actor unavailable or unsupported"end
   if phase=="align"then all=all and o.aligned==true
   elseif phase=="recover"and session.commands[a.id]~=nil then all=all and session.ends[a.id]==true and o.recovered==true end
  end
  return all
 end
 function session.Stop(reason)
  if session.state=="FINISHED"or session.state=="INTERRUPTED"then return #session.cleanupErrors==0 end
  if reason=="complete"and not(session.trainingEnded and session.trainingDeadline
   and session.trainingEnded>=session.trainingDeadline and session.completedCycles>=1)then reason="premature completion"end
  session.state=reason=="complete"and"FINISHED"or"INTERRUPTED";session.reason=reason
  for _,a in ipairs(actors)do
   local l=session.leases[a.id]
   if l and l.touched then
    local ok,e=invoke(port,"Release",a.id,a.identity,l.saved,reason)
    if ok~=true then session.cleanupErrors[#session.cleanupErrors+1]={id=a.id,error=e or"release not confirmed"}end
   end
  end
  if #session.cleanupErrors>0 then session.state="INTERRUPTED";session.reason="cleanup incomplete: "..tostring(reason)end
  return #session.cleanupErrors==0
 end
 local function arrange(now)
  session.roundSerial=session.roundSerial+1
  session.round=((session.roundSerial-1)%#plan.rounds)+1
  session.commands={};session.ends={}
  session.state="ALIGNING";session.phaseDeadline=now+alignSeconds
  local ok,e=invoke(port,"Arrange",plan.rounds[session.round],session.leases,plan.placements[session.round],plan.mode)
  if ok~=true then session.Stop(e or"alignment request failed");return false end
  return true
 end
 function session.Start(now)
  assert(session.state=="IDLE"and finite(now),"idle session and valid real clock required")
  session.started=now;session.lastTime=now;session.totalDeadline=now+totalSeconds
  local safe,e=invoke(port,"ContextSafe")
  if safe~=true then session.Stop(e or"unsafe context");return false end
  local _,invalid=observe("capture")
  if invalid then session.Stop(invalid);return false end
  -- Capture the previous duty/route for every member before any mutation.
  for _,a in ipairs(actors)do
   local saved,err=invoke(port,"Capture",a.id,a.identity)
   if type(saved)~="table"then session.Stop(err or"capture failed");return false end
   session.leases[a.id]={saved=saved,touched=false}
  end
  for _,a in ipairs(actors)do
   local l=session.leases[a.id];l.touched=true
   local ok,err=invoke(port,"Acquire",a.id,a.identity,l.saved)
   if ok~=true then session.Stop(err or"acquisition failed");return false end
  end
  return arrange(now)
 end
 function session.OnEnd(id,commandId)
  if session.state~="PLAYING"or session.commands[id]==nil or session.commands[id]~=commandId then return false end
  session.ends[id]=true;return true
 end
 local function play(now)
  for _,pair in ipairs(plan.rounds[session.round])do
   for _,role in ipairs({"initiator","receiver"})do
    local id=pair[role];local commandId,e=invoke(port,"CommandId",config.drillId,session.roundSerial,id)
    if type(commandId)~="number"or commandId~=math.floor(commandId)or commandId<0 or commandId>4294967295 or session.usedCommands[commandId]then
     session.Stop(e or"invalid or duplicate command id");return
    end
    session.usedCommands[commandId]=true;session.commands[id]=commandId
   end
  end
  -- All members, including spectators, have arrived before the real-time clock begins.
  if not session.trainingStarted then session.trainingStarted=now;session.trainingDeadline=now+trainingSeconds end
  session.state="PLAYING";session.phaseDeadline=now+playSeconds
  for _,pair in ipairs(plan.rounds[session.round])do
   for _,role in ipairs({"initiator","receiver"})do
    local id=pair[role];local partner=pair[role=="initiator"and"receiver"or"initiator"]
    local ok,e=invoke(port,"Play",id,pair[role.."Identity"],role,partner,session.commands[id],session.leases[id].saved)
    if ok~=true then session.Stop(e or"motion request failed");return end
   end
  end
 end
 function session.Tick(now)
  if session.state=="IDLE"or session.state=="FINISHED"or session.state=="INTERRUPTED"then return end
  if not finite(now)or now<session.lastTime then session.Stop("invalid real clock");return end
  session.lastTime=now
  if now<session.nextPoll then return end;session.nextPoll=now+.5
  local safe,e=invoke(port,"ContextSafe")
  if safe~=true then session.Stop(e or"context changed");return end
  if now>=session.totalDeadline then session.Stop("session deadline");return end
  if session.state=="RESTING"then
   local _,invalid=observe("capture");if invalid then session.Stop(invalid);return end
   if now>=session.restUntil then arrange(now)end
   return
  end
  local ready,invalid=observe(session.state=="ALIGNING"and"align"or"recover")
  if invalid then session.Stop(invalid);return end
  if ready then
   if session.state=="ALIGNING"then play(now)
   else
    session.completedRounds=session.completedRounds+1
    session.completedCycles=math.floor(session.completedRounds/#plan.rounds)
    if now>=session.trainingDeadline and session.completedCycles>=1 then
     session.trainingEnded=now;session.Stop("complete")
    else session.state="RESTING";session.restUntil=now+restSeconds end
   end
  elseif now>=session.phaseDeadline then session.Stop("phase deadline")end
 end
 return session
end
return M
