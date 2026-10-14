-- Persistent simulated ranks. Appointments require eligibility; vacancies never promote staff.
local H={version="0.2.0"}
H.ranks={Private=1,Corporal=2,Sergeant=3,Lieutenant=4,Captain=5,Major=6}
local minimum={["Team leader"]=2,["Squad leader"]=3,["Platoon leader"]=4}
function H.CanLead(p,appointment)
 return p.kind=="military"and p.active==true and p.available==true
  and(H.ranks[p.rank]or 0)>=(minimum[appointment]or math.huge)
end
function H.Create(saved)return {people=saved and saved.people or{},units={},teamSize=4,squadSize=8,platoonSize=24}end
local function senior(a,b)
 if (a.seniority or 0)~=(b.seniority or 0)then return(a.seniority or 0)<(b.seniority or 0)end
 return a.name<b.name
end
local function better(a,b)
 if not b then return true end
 local ar,br=H.ranks[a.rank]or 0,H.ranks[b.rank]or 0
 if ar~=br then return ar>br end
 local as,bs=tonumber(a.skillRating)or 0,tonumber(b.skillRating)or 0
 if as~=bs then return as>bs end
 return senior(a,b)
end
local function choose(people,appointment,excluded)
 local selected
 for _,p in ipairs(people)do
  if not(excluded and excluded[p.name])and H.CanLead(p,appointment)and better(p,selected)then selected=p end
 end
 return selected
end
function H.Sync(h,roster,observations)
 local groups,ordered={},{}
 -- Saved appointments are historical; current availability determines current leaders.
 for _,p in pairs(h.people)do
  p.active=false;p.available=false;p.id=nil;p.actingLeader=false
  p.appointment=p.kind=="civilian"and"Staff"or"Soldier";p.reportsTo=nil
 end
 for _,s in ipairs(roster)do
  local p=h.people[s.name]
  if not p then
   p={name=s.name,rank="Private",seniority=s.index or 0,
    rankSource="simulation rank; MGSV ability grade remains unchanged"}
   h.people[s.name]=p
  end
  local o=observations[s.id]
  p.active=true;p.id=s.id;p.label=s.label;p.skillRating=s.skillRating or p.skillRating
  p.available=o~=nil and o.real==true and o.available==true and o.alive~=false
  p.cluster=s.cluster or p.cluster or 1;p.platform=s.platform or p.platform or 0
  p.kind=s.role=="soldier"and"military"or"civilian"
  p.appointment=p.kind=="military"and"Soldier"or"Staff"
  p.department="department_"..p.cluster
  if p.kind=="military"then
   local key=tostring(p.cluster)..":"..tostring(p.platform)
   groups[key]=groups[key]or{};groups[key][#groups[key]+1]=p;ordered[#ordered+1]=p
  else p.team=nil;p.squad=nil;p.platoon=nil;p.commandChain=nil;p.reportsTo=p.department end
 end
 h.units={};h.platoonLeaders={}
 for _,p in ipairs(ordered)do
  local key=tostring(p.cluster);local current=h.platoonLeaders[key]
  if H.CanLead(p,"Platoon leader")and better(p,current)then h.platoonLeaders[key]=p end
 end
 local keys={};for key in pairs(groups)do keys[#keys+1]=key end;table.sort(keys)
 for _,key in ipairs(keys)do
  local people=groups[key];table.sort(people,senior)
  local squad="squad_"..key;local platoon="platoon_"..people[1].cluster
  local officer=h.platoonLeaders[tostring(people[1].cluster)]
  local excluded={};if officer then excluded[officer.name]=true end
  local leader=choose(people,"Squad leader",excluded)
  if leader then excluded[leader.name]=true end
  local unit={id=squad,label="Platform "..(people[1].platform+1).." squad",parent=platoon,
   members={},leader=leader and leader.name or"unfilled",cluster=people[1].cluster,platform=people[1].platform}
  h.units[#h.units+1]=unit
  for teamIndex=1,math.ceil(#people/h.teamSize)do
   local first=(teamIndex-1)*h.teamSize+1;local members={}
   for j=first,math.min(#people,first+h.teamSize-1)do members[#members+1]=people[j]end
   local team=squad.."_team_"..teamIndex;local teamLeader=choose(members,"Team leader",excluded)
   local teamUnit={id=team,label="Team "..teamIndex,parent=squad,leader=teamLeader and teamLeader.name or"unfilled",members={}}
   h.units[#h.units+1]=teamUnit
   for _,p in ipairs(members)do
    p.team=team;p.squad=squad;p.platoon=platoon
    p.commandChain={"Big Boss","Miller / Ocelot",p.department,platoon,squad,team}
    if officer and p.name==officer.name then
     p.appointment="Platoon leader";p.reportsTo=p.department;p.actingLeader=true
    elseif leader and p.name==leader.name then
     p.appointment="Squad leader";p.reportsTo=officer and officer.name or platoon;p.actingLeader=true
    elseif teamLeader and p.name==teamLeader.name then
     p.appointment="Team leader";p.reportsTo=leader and leader.name or(officer and officer.name or platoon);p.actingLeader=true
    else p.reportsTo=teamLeader and teamLeader.name or(leader and leader.name or(officer and officer.name or platoon))end
    unit.members[#unit.members+1]=p.name;teamUnit.members[#teamUnit.members+1]=p.name
   end
  end
 end
 table.sort(h.units,function(a,b)return a.id<b.id end);return h
end
function H.SetRank(h,name,rank)assert(H.ranks[rank],"unknown rank");local p=assert(h.people[name],"unknown staff member");p.rank=rank;p.rankLocked=true end
function H.Save(h)
 local people={}
 for name,p in pairs(h.people)do
  local c={};for k,v in pairs(p)do if k~="id"and k~="active"and k~="available"then c[k]=v end end;people[name]=c
 end
 return {version=2,people=people}
end
function H.Snapshot(h)
 local units={}
 for i=1,7 do
  units[#units+1]={id="department_"..i,label=({"Command","Combat","R&D","Support","Medical","Intel","Base Development"})[i],
   parent=i==2 and"Ocelot"or"Miller",leader="unfilled",appointment="Department head"}
  local p=h.platoonLeaders and h.platoonLeaders[tostring(i)]
  units[#units+1]={id="platoon_"..i,label="Department "..i.." platoon",parent="department_"..i,
   leader=p and p.name or"unfilled",appointment="Platoon leader (officer required)"}
 end
 for _,u in ipairs(h.units)do units[#units+1]=u end
 return {version=H.version,commanders={{id="Big Boss",parent=false,role="Commander",physical="player"},
  {id="Miller",parent="Big Boss",role="XO: personnel and administration",physical="logical command role; no duplicate character spawned"},
  {id="Ocelot",parent="Big Boss",role="XO: operations and training",physical="native named character when loaded"}},units=units,people=h.people,
  rankSystem="Simulated military ranks, separate from E-S++ ability ratings",
  unfilledPositions="Leadership stays vacant without a present, available, qualified person"}
end
return H
