-- Roster policy shared by manual and scheduled training. No physical actor is created.
local M={version="0.1.2"}
function M.UrgentNeed(actor,deferUnboundNeeds)
 local deferred={}
 if deferUnboundNeeds==true then for _,need in ipairs(actor.unservedNeeds or{})do deferred[need]=true end end
 for _,need in ipairs({"fatigue","hunger","thirst","bladder"})do
  if not deferred[need]and((actor.needs or{})[need]or 0)>=85 then return need end
 end
 return nil
end
function M.Select(roster,actors,observations,site,limit,deferUnboundNeeds,prepareManual)
 assert(limit==4 or limit==6,"training cohort cap must be four or six")
 local candidates,seen,names={},{},{}
 for _,s in ipairs(roster)do
  local a,o=actors[s.id],observations[s.id]
  if s.native==true and s.role=="soldier"and s.cluster==site.cluster and s.platform==site.platform
   and a and a.name==s.name and a.available~=false and not a.activityOwner
   and(a.state=="ROAMING"or(a.state=="DUTY"and(a.duty=="patrol"or a.duty=="guard"))
    or(prepareManual==true and(a.state=="GATHERING"or a.state=="FACILITY_QUEUE"or(a.state=="FACILITY_USE"and a.phase=="travelling"))))
   and o and o.real==true and o.available==true and o.alive~=false
   and type(o.x)=="number"and type(o.y)=="number"and type(o.z)=="number"
   and o.x==o.x and o.y==o.y and o.z==o.z
   and math.abs(o.x)<math.huge and math.abs(o.y)<math.huge and math.abs(o.z)<math.huge
   and not seen[s.id]and not names[s.name]then
    local urgent=M.UrgentNeed(a,deferUnboundNeeds)
    if not urgent then
     seen[s.id]=true;names[s.name]=true
     candidates[#candidates+1]={id=s.id,identity=s.name,native=true,role="soldier",available=true,
      count=a.trainingCount or 0,distance=(o.x-site.x)^2+(o.z-site.z)^2+16*(o.y-site.y)^2,label=s.label}
    end
  end
 end
 table.sort(candidates,function(a,b)
  if a.count~=b.count then return a.count<b.count end
  if a.distance~=b.distance then return a.distance<b.distance end
  return a.identity<b.identity
 end)
 local n=math.min(limit,#candidates);n=n>=6 and 6 or(n>=4 and 4 or 0)
 if n==0 then return nil,"Four nonurgent available local soldiers are needed; active services, other reservations, muster and civilians are excluded"end
 local out={};for i=1,n do out[i]=candidates[i]end;return out
end
return M