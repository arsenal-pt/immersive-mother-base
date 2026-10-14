-- Actor-specific listeners for MGSV's mutable message registry.
-- No polling, engine commands, player input, save access or activity-success inference.
local M={}
local function copy(t)local x={};for k,v in pairs(t or{})do x[k]=v end;return x end
function M.Attach(registry,subscriptions)
 assert(type(registry)=="table"and type(subscriptions)=="table","message registry and subscriptions required")
 assert(#subscriptions>0 and #subscriptions<=32,"bounded subscription list required")
 local seen={}
 for _,s in ipairs(subscriptions)do
  assert(type(s.class)=="number"and type(s.message)=="number"and type(s.sender)=="number"and type(s.handler)=="function","invalid subscription")
  local key=tostring(s.class)..":"..tostring(s.message)..":"..tostring(s.sender)
  assert(not seen[key],"duplicate subscription");seen[key]=true
 end
 local lease={active=true,callbackCount=0,handlerErrors=0,entries={}}
 local buckets={}
 for _,subscription in ipairs(subscriptions)do
  local s=subscription
  registry[s.class]=registry[s.class]or{}
  local class=registry[s.class];local key=tostring(s.class)..":"..tostring(s.message)
  local bucket=buckets[key]
  if not bucket then
   local previous=class[s.message];local installed=copy(previous)
   installed.sender=copy(previous and previous.sender)
   installed.senderOption=copy(previous and previous.senderOption)
   bucket={class=class,message=s.message,previous=previous,installed=installed}
   buckets[key]=bucket;lease.entries[#lease.entries+1]=bucket
   class[s.message]=installed
  end
  local old=bucket.installed.sender[s.sender]
  bucket.installed.sender[s.sender]=function(a0,a1,a2,a3)
   if lease.active then
    lease.callbackCount=lease.callbackCount+1
    local ok=pcall(s.handler,a0,a1,a2,a3)
    if not ok then lease.handlerErrors=lease.handlerErrors+1 end
   end
   if old then return old(a0,a1,a2,a3)end
  end
 end
 function lease.Detach()
  lease.active=false;local conflicts=0
  for _,e in ipairs(lease.entries)do
   if e.class[e.message]==e.installed then e.class[e.message]=e.previous
   else conflicts=conflicts+1 end
  end
  return conflicts==0,conflicts
 end
 return lease
end
return M
