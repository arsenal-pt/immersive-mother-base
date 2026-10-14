-- Temporary measurement harness. Restores original module functions on Finish.
-- Uses exported native engine frame/time counters; rendering is cross-checked externally.
local P={version="0.1.0"}
local refs,original,stats,mode,started,frames
local function modules()
 return {life=NpcLife,soldiers=NpcSoldiers,civilians=NpcCivilians,
  training=NpcTraining,map=NpcBaseMap,staff=NpcStaffControl}
end
local function json(v)
 local t=type(v)
 if t=="nil"then return"null"end
 if t=="number"then return(v==v and math.abs(v)<math.huge)and tostring(v)or"null"end
 if t=="boolean"then return tostring(v)end
 if t=="string"then return'"'..v:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r')..'"'end
 if t~="table"then return json(tostring(v))end
 local rows={};for k,x in pairs(v)do rows[#rows+1]=json(tostring(k))..":"..json(x)end
 return"{"..table.concat(rows,",").."}"
end
local function write(s)
 local f=assert(io.open(InfCore.paths.mod.."nlab_perf_probe.json","w"));f:write(json(s));f:close();return s
end
function P.Begin(requested)
 assert(vars.missionCode==30050,"FPS test requires normal Mother Base")
 assert(gvars.usingNormalMissionSlot==true,"FPS test requires normal mission slot")
 assert(not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating(),"base loading")
 assert(requested=="full"or requested=="paused"or requested=="life"or requested=="soldiers"or requested=="map"or requested=="staff","unknown FPS mode")
 if not original then
  refs=modules();original={}
  for key,m in pairs(refs)do if type(m.Update)=="function"then original[key]=m.Update end end
 end
 for key,fn in pairs(original)do refs[key].Update=fn end
 mode=requested;stats={};started=Time.GetRawElapsedTimeSinceStartUp();frames=Time.GetFrameIndex()
 for key,fn in pairs(original)do
  local k=key;local call=fn;stats[k]={calls=0,clockMilliseconds=0,maxClockMilliseconds=0,errors=0}
  if mode=="full"or mode==k then
   refs[k].Update=function(checks,now)
    local before=os.clock();local ok,e=pcall(call,checks,now);local dt=math.max(0,os.clock()-before)*1000
    local row=stats[k];row.calls=row.calls+1;row.clockMilliseconds=row.clockMilliseconds+dt
    row.maxClockMilliseconds=math.max(row.maxClockMilliseconds,dt)
    if not ok then row.errors=row.errors+1;error(e)end
   end
  else refs[k].Update=function()end end
 end
 return P.Sample()
end
function P.Sample()
 assert(started,"measurement not started")
 local now=Time.GetRawElapsedTimeSinceStartUp();local n=Time.GetFrameIndex()
 local elapsed=now-started;local count=n-frames
 local frameTime=Time.GetFrameTime()
 return write({schema=1,mode=mode,missionCode=vars.missionCode,normalSlot=gvars.usingNormalMissionSlot,
  realTime=now,elapsedSeconds=elapsed,engineFrames=count,engineUpdateFps=elapsed>0 and count/elapsed or 0,
  rawFrameTime=frameTime,frameTimeMeaning="exported native Time.GetFrameTime; unit cross-check pending",
  fpsMeaning="engine frame counter divided by native elapsed time; not yet a rendering measurement",
  moduleClockMeaning="os.clock intervals around original Update calls; diagnostic, not a calibrated GPU or CPU profiler",
  modules=stats,playerInputSent=false})
end
function P.Finish()
 local s=P.Sample()
 for key,fn in pairs(original or{})do refs[key].Update=fn end
 s.restored=true;return write(s)
end
return P
