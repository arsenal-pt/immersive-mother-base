-- Pure bounded recorder; injected readers/sink. No engine/controller dependency.
local M={VERSION="0.1.2",SCHEMA=1}
local hard={sampleHz=5,durationSeconds=120,maxSamples=1200,maxEvents=512,maxMarks=32,
 maxBytes=2097152,maxBufferBytes=65536,maxRecordBytes=8192,flushSeconds=1}
local function finite(n)return type(n)=="number"and n==n and n~=math.huge and n~=-math.huge end
local function quote(s)
 return '"'..s:gsub('[%z\1-\31\\"]',function(c)
  if c=='"'then return '\\"'elseif c=='\\'then return '\\\\'end
  return string.format('\\u%04x',c:byte())
 end)..'"'
end
local function encode(v,depth)
 depth=depth or 0;assert(depth<=10,"JSON nesting limit")
 local t=type(v)
 if t=="nil"then return"null"elseif t=="boolean"then return tostring(v)
 elseif t=="number"then return finite(v)and string.format("%.17g",v)or"null"
 elseif t=="string"then return quote(v)end
 assert(t=="table","unsupported JSON type")
 local keys,out={},{};local max,numeric=0,true
 for k in pairs(v)do
  if type(k)=="number"and k>=1 and k==math.floor(k)then max=math.max(max,k)else numeric=false end
  keys[#keys+1]=k
 end
 if #keys>0 and numeric and max==#keys then
  for i=1,max do out[#out+1]=encode(v[i],depth+1)end
  return"["..table.concat(out,",").."]"
 end
 table.sort(keys,function(a,b)return tostring(a)<tostring(b)end)
 for _,k in ipairs(keys)do out[#out+1]=quote(tostring(k))..":"..encode(v[k],depth+1)end
 return"{"..table.concat(out,",").."}"
end
M.Encode=encode
function M.Scalar(v)
 if finite(v)or type(v)=="boolean"then return v end
 if type(v)=="string"then return v:sub(1,128)end
 return nil
end
local function bound(v,default,low,high,integer)
 if v==nil then return default end
 assert(finite(v)and v>=low and v<=high,"invalid recorder limit")
 if integer then assert(v==math.floor(v),"integer recorder limit required")end
 return v
end
function M.New(env)
 assert(type(env)=="table"and type(env.now)=="function"and type(env.context)=="function"
  and type(env.sample)=="function"and type(env.allocate)=="function","recorder environment required")
 local P={active=false,last=nil};local r
 local function phase(name)if type(env.phase)=="function"then pcall(env.phase,name)end end
 local function clock()
  local ok,n=pcall(env.now);if not ok or not finite(n)then return nil,"clock unavailable"end
  return n
 end
 local function flush()
  if r.bufferBytes==0 then return true end
  local ok,value=pcall(r.sink.write,table.concat(r.buffer))
  if not ok or value==false or value==nil then r.ioFailure=true;return false,"trace write failed"end
  r.writtenBytes=r.writtenBytes+r.bufferBytes;r.buffer={};r.bufferBytes=0
  return true
 end
 local function queue(row,footer)
  local ok,line=pcall(encode,row);if not ok then return false,"record encoding failed"end
  line=line.."\n"
  if #line>r.config.maxRecordBytes then return false,"record byte limit"end
  local reserve=footer and 0 or 4096
  if r.writtenBytes+r.bufferBytes+#line>r.config.maxBytes-reserve then return false,"file byte limit"end
  -- Callbacks never write. Tick/Stop flush; reserve buffer room for terminal footer.
  if r.bufferBytes+#line>r.config.maxBufferBytes-reserve then return false,"buffer byte limit"end
  r.buffer[#r.buffer+1]=line;r.bufferBytes=r.bufferBytes+#line
  return true
 end
 local function finish(reason,now)
  if not r then return P.last end
  local ended=r;now=now or ended.lastTime
  local summary={schema=M.SCHEMA,version=M.VERSION,takeId=ended.takeId,tracePath=ended.tracePath,
   summaryPath=ended.summaryPath,startedRawSeconds=ended.started,endedRawSeconds=now,
   elapsedSeconds=math.max(0,now-ended.started),reason=reason or"manual stop",samples=ended.samples,
   events=ended.events,marks=ended.marks,droppedEvents=ended.droppedEvents,droppedMarks=ended.droppedMarks,
   readOnly=true,nativeGameplayVerified=false,replaySupported=false,config=ended.config}
  local qok,qerr=false,"trace write failed"
  local fok,ferr=false,"trace write failed"
  -- A failed write may be partial: never retry the same buffer or claim a complete trace.
  if not ended.ioFailure then
   qok,qerr=queue({kind="stop",t=now-ended.started,summary=summary},true)
   fok,ferr=flush()
  end
  local cok,cvalue=pcall(ended.sink.close)
  summary.traceComplete=qok and fok and cok and cvalue~=false and cvalue~=nil
  summary.traceBytes=ended.writtenBytes
  summary.error=not qok and qerr or not fok and ferr or not cok and"trace close failed"or nil
  if not summary.traceComplete and not summary.error then summary.error="trace close failed"end
  P.active=false;r=nil;P.last=summary
  local sok,svalue=pcall(ended.sink.summary,encode(summary).."\n")
  summary.summarySaved=sok and svalue~=false and svalue~=nil
  return summary
 end
 function P.Status()
  if not r then return{active=false,last=P.last}end
  phase("core.status.before")
  local value={active=true,takeId=r.takeId,tracePath=r.tracePath,summaryPath=r.summaryPath,
   samples=r.samples,events=r.events,marks=r.marks,droppedEvents=r.droppedEvents,
   bufferBytes=r.bufferBytes,traceBytes=r.writtenBytes+r.bufferBytes,deadlineRawSeconds=r.deadline}
  phase("core.status.after")
  return value
 end
 function P.Start(options)
  if r then return false,"capture already active"end
  local now,err=clock();if not now then return false,err end
  local ok,ctx=pcall(env.context);if not ok or not ctx then return false,"requires ready normal Mother Base"end
  local o=options or{};local c={}
  local bok,berr=pcall(function()
   c.sampleHz=bound(o.sampleHz,hard.sampleHz,1,10)
   c.durationSeconds=bound(o.durationSeconds,hard.durationSeconds,5,120)
   c.maxSamples=bound(o.maxSamples,hard.maxSamples,1,hard.maxSamples,true)
   c.maxEvents=bound(o.maxEvents,hard.maxEvents,1,hard.maxEvents,true)
   c.maxMarks=bound(o.maxMarks,hard.maxMarks,1,hard.maxMarks,true)
   c.maxBytes=bound(o.maxBytes,hard.maxBytes,8192,hard.maxBytes,true)
   c.maxBufferBytes=bound(o.maxBufferBytes,hard.maxBufferBytes,8192,hard.maxBufferBytes,true)
   c.maxRecordBytes=bound(o.maxRecordBytes,hard.maxRecordBytes,512,hard.maxRecordBytes,true)
   c.flushSeconds=bound(o.flushSeconds,hard.flushSeconds,0.2,1)
  end)
  if not bok then return false,tostring(berr)end
  local aok,sink=pcall(env.allocate,now)
  if not aok or not sink then return false,"could not reserve a new trace"end
  r={sink=sink,takeId=sink.takeId,tracePath=sink.tracePath,summaryPath=sink.summaryPath,
   config=c,started=now,lastTime=now,deadline=now+c.durationSeconds,nextSample=now,
   nextFlush=now+c.flushSeconds,samples=0,events=0,marks=0,droppedEvents=0,droppedMarks=0,
   buffer={},bufferBytes=0,writtenBytes=0}
  P.active=true
  local qok,qerr=queue({kind="header",schema=M.SCHEMA,version=M.VERSION,takeId=r.takeId,
   startedRawSeconds=now,context=ctx,config=c,capabilities=env.capabilities or{},
   readOnly=true,replaySupported=false,format="timestamped observations; no motion/input replay"})
  if not qok then finish(qerr,now);return false,qerr end
  local fok,ferr=flush();if not fok then finish(ferr,now);return false,ferr end
  return true,P.Status()
 end
 function P.Stop(reason)
  if not r then return false,"no active capture"end
  local now=clock();return true,finish(reason,now or r.lastTime)
 end
 function P.Mark(label)
  if not r then return false,"no active capture"end
  if r.marks>=r.config.maxMarks then r.droppedMarks=r.droppedMarks+1;return false,"mark limit"end
  local now=clock();if not now then r.stopRequested="clock unavailable";return false,"clock unavailable"end
  if now>=r.deadline then r.stopRequested="duration limit";return false,"duration limit"end
  if type(label)~="string"or label==""then label="mark "..(r.marks+1)end
  local ok,err=queue({kind="mark",t=math.max(0,now-r.started),label=label:sub(1,128)})
  if ok then r.marks=r.marks+1 else r.stopRequested=err end
  return ok,err
 end
 function P.Event(class,message,args)
  if not r or r.stopRequested then return false end
  if r.events>=r.config.maxEvents then r.droppedEvents=r.droppedEvents+1;return false end
  local now=clock();if not now then r.stopRequested="clock unavailable";return false end
  if now>=r.deadline then r.stopRequested="duration limit";return false end
  local clean={};for i=0,3 do clean["arg"..i]=M.Scalar(args and args["arg"..i])end
  local ok,err=queue({kind="event",t=math.max(0,now-r.started),class=class,message=message,args=clean})
  if ok then r.events=r.events+1 else r.stopRequested=err end
  return ok
 end
 function P.Tick()
  if not r then return end -- Inactive: no clocks, readers or IO.
  local now,err=clock();if not now then finish(err,r.lastTime);return end
  if now<r.lastTime then finish("clock moved backwards",r.lastTime);return end
  r.lastTime=now
  if r.stopRequested or now>=r.deadline then finish(r.stopRequested or"duration limit",now);return end
  if now>=r.nextSample then
   r.nextSample=now+1/r.config.sampleHz -- no catch-up after stalls
   local cok,ctx=pcall(env.context)
   if not cok or not ctx then finish("context changed",now);return end
   local sok,sample=pcall(env.sample)
   if not sok or type(sample)~="table"then finish("sample reader failed",now);return end
   local qok,qerr=queue({kind="sample",t=now-r.started,player=sample})
   if not qok then finish(qerr,now);return end
   r.samples=r.samples+1
   if r.samples>=r.config.maxSamples then finish("sample limit",now);return end
  end
  if now>=r.nextFlush then
   r.nextFlush=now+r.config.flushSeconds
   local fok,ferr=flush();if not fok then finish(ferr,now)end
  end
 end
 return P
end
return M