-- Authored deterministic CQC cohort policy. This module issues no engine commands.
-- A round is released only after both actors in every pair have completed recovery.
-- Animation/fixture bindings must be proven separately before a caller runs a drill.
local M={version="0.2.0",maximumPairs=3}
local function validId(id)
 return type(id)=="number" and id==math.floor(id) and id>=0 and id<65535
end
function M.Build(actors)
 assert(type(actors)=="table" and (#actors==4 or #actors==6),"CQC requires four or six soldiers")
 local ordered,seen,identities={},{},{}
 for _,a in ipairs(actors)do
  assert(type(a)=="table" and validId(a.id) and not seen[a.id],"invalid or duplicate physical actor")
  assert(a.native==true and a.role=="soldier" and a.available==true,"CQC requires available native soldiers")
  assert(type(a.identity)=="string" and #a.identity>0 and not identities[a.identity],"invalid or duplicate staff identity")
  seen[a.id]=true;identities[a.identity]=true
  ordered[#ordered+1]={id=a.id,identity=a.identity}
 end
 table.sort(ordered,function(a,b)return a.identity<b.identity end)
 local n=#ordered
 local plan={schema=2,participants=n,pairs=n/2,rounds={{},{}},fixedPartners=true,animationBindingRequired=true}
 -- Each station keeps the same two soldiers. Only their throw/receive roles reverse.
 for slot=1,n/2 do
  local a,b=ordered[slot*2-1],ordered[slot*2]
  plan.rounds[1][slot]={slot=slot,initiator=a.id,receiver=b.id,initiatorIdentity=a.identity,receiverIdentity=b.identity,reverse=false}
  plan.rounds[2][slot]={slot=slot,initiator=b.id,receiver=a.id,initiatorIdentity=b.identity,receiverIdentity=a.identity,reverse=true}
 end
 return plan
end
function M.CanAdvance(pairs,observations,drillId)
 if type(drillId)~="string" or #drillId==0 or #drillId>64 then return false end
 if type(pairs)~="table" or #pairs<2 or #pairs>3 or type(observations)~="table"then return false end
 local seen={}
 for _,p in ipairs(pairs)do
  if type(p)~="table"then return false end
  for _,role in ipairs({"initiator","receiver"})do
   local id=p[role];if not validId(id)then return false end;local o=observations[id]
   if seen[id] or type(o)~="table" or o.drillId~=drillId or o.identity~=p[role.."Identity"] or o.recovered~=true or o.available~=true then return false end
   seen[id]=true
  end
 end
 return true
end
return M
