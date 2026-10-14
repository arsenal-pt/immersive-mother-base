-- Relative CQC formations only; native support/routes must be validated by the port.
local M={version="0.2.0"}
local function copyPair(p,slot)
 return {slot=slot,sourceSlot=p.slot,initiator=p.initiator,receiver=p.receiver,
  initiatorIdentity=p.initiatorIdentity,receiverIdentity=p.receiverIdentity,reverse=p.reverse}
end
function M.Build(pairPlanner,actors,mode,options)
 mode=mode or"parallel";options=options or{}
 assert(mode=="parallel"or mode=="circle","unknown training formation")
 local policy=pairPlanner.Build(actors)
 local spacing=options.pairSpacing or 1.6
 local gap=options.pairGap or 5
 local radius=options.observerRadius or 4
 assert(type(spacing)=="number"and spacing>=.6 and spacing<=2,"bounded prototype pair spacing required")
 assert(type(gap)=="number"and gap>=2*spacing+1 and gap<=12,"separate pair spaces required")
 assert(type(radius)=="number"and radius>=spacing+1 and radius<=10,"separate observer space required")
 local ordered={};for _,a in ipairs(actors)do ordered[#ordered+1]={id=a.id,identity=a.identity}end
 table.sort(ordered,function(a,b)return a.identity<b.identity end)
 local plan={schema=1,participants=policy.participants,pairs=mode=="circle"and 1 or policy.pairs,
  mode=mode,fixedPartners=policy.fixedPartners,rounds={},placements={},requiresNativeSiteValidation=true,prototypeSpacing=true}
 local stationPlaces={}
  local function add(pairs)
  local places={};local active={}
  for slot,p in ipairs(pairs)do
   local x=(slot-(#pairs+1)/2)*gap
   local first,second=p.reverse and p.receiver or p.initiator,p.reverse and p.initiator or p.receiver
   if mode=="parallel"then
    stationPlaces[first]=stationPlaces[first]or{x=x,z=-spacing/2,headingDegrees=0,pair=slot}
    stationPlaces[second]=stationPlaces[second]or{x=x,z=spacing/2,headingDegrees=180,pair=slot}
   end
   for _,role in ipairs({"initiator","receiver"})do
    local id=p[role];local fixed=mode=="parallel"and stationPlaces[id]
    places[id]={x=fixed and fixed.x or x,z=fixed and fixed.z or(role=="initiator"and-spacing/2 or spacing/2),
     headingDegrees=fixed and fixed.headingDegrees or(role=="initiator"and 0 or 180),role=role,pair=slot}
   end
   active[p.initiator]=true;active[p.receiver]=true
  end
  local watchers={};for _,a in ipairs(ordered)do if not active[a.id]then watchers[#watchers+1]=a end end
  for i,a in ipairs(watchers)do
   local angle=(i-1)*2*math.pi/#watchers
   local x,z=radius*math.sin(angle),radius*math.cos(angle)
   places[a.id]={x=x,z=z,headingDegrees=math.atan2(-x,-z)*180/math.pi,role="observer"}
  end
  plan.rounds[#plan.rounds+1]=pairs;plan.placements[#plan.rounds]=places
 end
 for _,round in ipairs(policy.rounds)do
  if mode=="circle"then
   for _,p in ipairs(round)do add({copyPair(p,1)})end
  else
   local pairs={};for slot,p in ipairs(round)do pairs[slot]=copyPair(p,slot)end;add(pairs)
  end
 end
 return plan
end
return M
