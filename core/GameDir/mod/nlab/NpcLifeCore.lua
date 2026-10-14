-- Pure daily-life state machine. No engine calls, timers, files or player input.
local Life={}
Life.states={"ROAMING","MUSTER","GATHERING","FACILITY_QUEUE","FACILITY_USE","DUTY"}
Life.roles={
 contractor={duties={"logistics","maintenance"},civilian=true},
 doctor={duties={"clinic"},civilian=true},
 nurse={duties={"clinic"},civilian=true},
 soldier={duties={"guard","training","range","patrol","exercise"},civilian=false},
}
-- Binding status is explicit: defining a job does not create its room or animation.
Life.duties={
 patrol={label="Patrol",roles={soldier=true},binding="native_patrol",durationSeconds=120},
 guard={label="Guard duty",roles={soldier=true},binding="post",durationSeconds=120},
 training={label="CQC technique practice",roles={soldier=true},binding="external_session",requirement="native training coordinator; contact throws remain unverified"},
 range={label="Weapons training",roles={soldier=true},binding="pending",requirement="safe firing lane and shooting action"},
 exercise={label="Physical training",roles={soldier=true},binding="pending",requirement="exercise pad and physical-training action"},
 logistics={label="Logistics / supply",roles={soldier=true,contractor=true},binding="pending",requirement="depot and supply handling action"},
 maintenance={label="Maintenance / mechanics",roles={soldier=true,contractor=true},binding="pending",requirement="workshop or vehicle bay and repair action"},
 clinic={label="Medical duty",roles={doctor=true,nurse=true},binding="pending",requirement="staffed sick bay and treatment action"},
 research={label="R&D work",roles={soldier=true,contractor=true},binding="pending",requirement="R&D workstation"},
 engineering={label="Base development",roles={soldier=true,contractor=true},binding="pending",requirement="engineering/construction workstation"},
 intelligence={label="Intelligence work",roles={soldier=true,contractor=true},binding="pending",requirement="Intel workstation"},
 command={label="Command / administration",roles={soldier=true,contractor=true},binding="pending",requirement="office/TOC workstation"},
}
Life.duties.department_rounds={label="Department rounds",roles={doctor=true,nurse=true,contractor=true},binding="native_patrol",durationSeconds=120}
local function supports(a,key)return type(a.capabilities)~="table"or a.capabilities[key]~=false end
local rates={hunger=7,thirst=9,fatigue=4,hygiene=3,bladder=8,social=4}
local needFacility={hunger="mess",thirst="water",fatigue="bunk",hygiene="shower",bladder="toilet"}
local function clamp(x)return math.max(0,math.min(100,x))end
local function emit(w,id,kind,target)
 w.actions[#w.actions+1]={actor=id,kind=kind,target=target}
end
local function log(w,id,event,reason)
 w.events[#w.events+1]={time=w.absolute,actor=id,event=event,reason=reason}
 if #w.events>100 then table.remove(w.events,1)end
end
local function copyNeeds(n)
 local out={};for k in pairs(rates)do out[k]=clamp((n and n[k])or 20)end;return out
end
local function release(w,a)
 if a.activityOwner then w.externalActivities=math.max(0,(w.externalActivities or 0)-1)end
 for _,f in pairs(w.facilities)do
  for i=#f.queue,1,-1 do if f.queue[i]==a.id then table.remove(f.queue,i)end end
  for i,id in pairs(f.users)do if id==a.id then f.users[i]=nil end end
 end
 for _,post in pairs(w.workPosts or {})do if post.owner==a.id then post.owner=nil end end
 a.activityOwner=nil;a.activityPhase=nil;a.activityPrevious=nil;a.duty=nil;a.dutyLabel=nil;a.dutyPost=nil;a.dutyUntilReal=nil;a.dutyStartedReal=nil;a.dutyDurationSeconds=nil;a.dutyBinding=nil
 a.facility=nil;a.useSlot=nil;a.serviceUntil=nil;a.serviceStartedAbsolute=nil;a.target=nil;a.targetAssignedReal=nil;a.held=false;a.travelBand=nil;a.travelRoute=nil;a.rushEntry=nil;a.rushDone=nil;a.conversationGroup=nil
end
local function travelCommand(w,a,target)
 local command={};for k,v in pairs(target)do command[k]=v end
 local band="walk";local policy=w.config.muster.travel
 if a.state=="MUSTER"and policy and policy.enabled and policy.entries and policy.profileByKind[a.kind or (a.role=="soldier"and "soldier"or "civilian")]then
  local o=a.observation
  local distance=o and math.sqrt((o.x-target.x)^2+(o.y-target.y)^2+(o.z-target.z)^2)or math.huge
  local via=policy.via
  local nearExit=o and math.sqrt((o.x-via.x)^2+(o.y-via.y)^2+(o.z-via.z)^2)<1.8
  if distance<=policy.approachDistance or nearExit then a.rushDone=true end
  if not a.rushDone then
   if not a.rushEntry then
    local best=math.huge
    for i,e in ipairs(policy.entries)do
     local d=o and (o.x-e.x)^2+(o.z-e.z)^2+9*(o.y-e.y)^2 or i
     if d<best then best=d;a.rushEntry=i end
    end
   end
   band=distance>policy.farDistance and "double-time-far"or "double-time"
   local profile=policy.profileByKind[a.kind or (a.role=="soldier"and "soldier"or "civilian")]
   local suffix=profile and profile[distance>policy.farDistance and "dash"or "run"]
   if suffix then command.route=via.route.."_e"..(a.rushEntry-1).."_"..suffix;command.urgency="muster"end
  end
 end
 command.movementBand=band;return command,band
end
local function move(w,a,target)
 if a.target and a.target.route==target.route and (a.target.routePoint or 0)==(target.routePoint or 0) and a.target.x==target.x and a.target.y==target.y and a.target.z==target.z then return end
 a.target=target;a.phase="travelling";a.held=false;a.targetAssignedReal=w.realNow
 local command,band=travelCommand(w,a,target);a.travelBand=band;a.travelRoute=command.route;emit(w,a.id,"move",command)
end
local function transition(w,a,state,reason)
 release(w,a);a.state=state;a.phase="travelling";a.reason=reason;a.entered=w.absolute;a.enteredReal=w.realNow
 log(w,a.id,state,reason)
end
local function roam(w,a,reason)
 transition(w,a,"ROAMING",reason);a.phase="walking";a.cooldownUntil=w.absolute+300
 emit(w,a.id,"roam")
end
local removeMember
local function assignDuty(w,a,key,duration,reason)
 local job=Life.duties[key]
 if not job then return false,"unknown duty "..tostring(key)end
 if not job.roles[a.role]then return false,"duty excluded for role "..a.role end
 if a.available==false then return false,"native character unavailable"end
 if not supports(a,"nativeDuty")then return false,"duty not supported by actor engine"end
 if job.binding=="pending"or job.binding=="external_session"then return false,"binding requires coordinator: "..job.requirement end
 duration=duration or job.durationSeconds
 if type(duration)~="number"or duration~=duration or duration<5 or duration>3600 then return false,"invalid duty duration"end
 local chosen
 if job.binding=="post"then
  for _,post in ipairs(w.workPosts)do
   local c=post.config
   if c.duties[key]and(not post.owner or post.owner==a.id)and
    (not w.config.nativeMode or(a.pilotEligible and c.cluster==a.cluster and c.platform==a.platform))then chosen=post;break end
  end
  if not chosen then return false,"no reachable free work post"end
 end
 if w.group then removeMember(w.group,a.id);if #w.group.ids==0 then w.group=nil end end
 transition(w,a,"DUTY",reason or("assigned "..job.label))
 a.duty=key;a.dutyLabel=job.label;a.dutyBinding=job.binding;a.dutyDurationSeconds=duration
 if chosen then
  chosen.owner=a.id;a.dutyPost=chosen.config.id
  move(w,a,chosen.config.target)
 else
  a.phase="on_duty";a.dutyStartedReal=w.realNow;a.dutyUntilReal=w.realNow+duration
  emit(w,a.id,"nativeDuty",{duty=key});log(w,a.id,"DUTY_STARTED",job.label)
 end
 return true
end
local function allowed(a,facility,isDuty)
 if facility=="training"then return a.role=="soldier"end
 if isDuty and facility=="clinic"then return a.role=="doctor"or a.role=="nurse"end
 return true
end
local function finite(v)return type(v)=="number"and v==v and v~=math.huge and v~=-math.huge end
local function nativeReady(o)
 return o and o.real==true and o.available==true and o.alive~=false and finite(o.x)and finite(o.y)and finite(o.z)
end
local function facilityKind(key,f)return f.config.service or key end
local function validServiceTarget(p)
 if type(p)~="table"or not finite(p.x)or not finite(p.y)or not finite(p.z)then return false end
 local r=p.route
 if not((type(r)=="string"and #r>0)or(finite(r)and r>=0 and r<=4294967295 and r%1==0))then return false end
 if p.routePoint~=nil and(not finite(p.routePoint)or p.routePoint<0 or p.routePoint%1~=0)then return false end
 return p.yaw==nil or finite(p.yaw)
end
local function eligibleFacility(w,a,key,f,isDuty)
 if not supports(a,"services")then return false,"service action not supported by actor engine"end
 local c=f.config
 if c.enabled==false or f.retired then return false,"service binding unavailable"end
  if c.allowActors and c.allowActors[a.id]~=true then return false,"service reserved for controlled pilot"end
 if c.minimumGrade and c.completedGrade and c.completedGrade<c.minimumGrade then return false,"platform not completed"end
 if not allowed(a,facilityKind(key,f),isDuty)then return false,"duty excluded for role "..a.role end
 if c.cluster~=nil or c.platform~=nil then
  if c.cluster~=a.cluster or c.platform~=a.platform then return false,"service outside person's platform"end
 elseif w.config.nativeMode and not a.pilotEligible then return false,"facility outside current native pilot area"end
 if not finite(c.capacity)or c.capacity<1 or c.capacity%1~=0 or type(c.queue)~="table"or type(c.uses)~="table"or #c.queue<1 or #c.uses<c.capacity or not finite(c.serviceSeconds)or c.serviceSeconds<=0 then return false,"incomplete service binding"end
 for _,p in ipairs(c.queue)do if not validServiceTarget(p)then return false,"invalid service queue target"end end
 for _,p in ipairs(c.uses)do if not validServiceTarget(p)then return false,"invalid service use target"end end
 if type(c.relief)~="table"then return false,"missing service relief"end
 for need,value in pairs(c.relief)do if (need~="health"and not rates[need])or not finite(value)or value<0 then return false,"invalid service relief"end end
 return true
end
local function resolveFacility(w,a,key,isDuty,capacity)
 local exact=w.facilities[key];local keys={}
 if exact and exact.config.service and key~=exact.config.service then keys[1]=key
 else for candidate,f in pairs(w.facilities)do if facilityKind(candidate,f)==key then keys[#keys+1]=candidate end end;table.sort(keys)end
 local selected,best,reason=nil,math.huge,"no local service binding"
 for _,candidate in ipairs(keys)do
  local f=w.facilities[candidate];local ok,e=eligibleFacility(w,a,candidate,f,isDuty)
  if ok then
   local queued=#f.queue;for _,id in ipairs(f.queue)do if id==a.id then queued=queued-1;break end end
   if not capacity or queued<#f.config.queue then
    local p=f.config.queue[1];local o=a.observation
    local d=o and finite(o.x)and finite(o.z)and (o.x-p.x)^2+(o.z-p.z)^2 or 0
    if f.config.cluster==nil then d=d+1000000 end
    if d<best then selected=candidate;best=d end
   else reason="queue full"end
  else reason=e end
 end
 return selected,reason
end
local function coverage(w,a)
 local bindings,unserved={},{}
 for need,key in pairs(needFacility)do local instance=resolveFacility(w,a,key,false,false)
  if instance then bindings[need]=instance else unserved[#unserved+1]=need end
 end
 if w.config.nativeMode and not a.pilotEligible then unserved[#unserved+1]="social"end
 table.sort(unserved);return bindings,unserved
end
local function queue(w,a,key,reason,isDuty)
 if a.available==false or(w.config.strictNativeObservations and not nativeReady(a.observation))then return false,"native character unavailable"end
 local chosen,e=resolveFacility(w,a,key,isDuty,true)
 if not chosen then return false,e end
 local f=w.facilities[chosen]
 transition(w,a,"FACILITY_QUEUE",reason);a.facility=chosen;f.queue[#f.queue+1]=a.id
 move(w,a,f.config.queue[#f.queue]);return true
end
local function random(w)
 w.randomState=(w.randomState*48271)%2147483647;return w.randomState/2147483647
end
local function shuffle(w,rows)
 for i=#rows,2,-1 do local j=1+math.floor(random(w)*i);rows[i],rows[j]=rows[j],rows[i]end
end
removeMember=function(g,id)
 for i=#g.ids,1,-1 do if g.ids[i]==id then table.remove(g.ids,i)end end
 for _,c in ipairs(g.groups or {})do
  for i=#c.ids,1,-1 do if c.ids[i]==id then table.remove(c.ids,i)end end
 end
end
local function conversations(w,reason,ids,duration)
 if w.group then for _,id in ipairs(w.group.ids)do if w.actors[id]then roam(w,w.actors[id],"group interrupted")end end end
 local cfg=w.config.gather
 if duration then assert(type(duration)=="number"and duration>=cfg.duration.minimumSeconds and duration<=cfg.duration.maximumSeconds,"conversation duration outside configured bounds")end
 local pools={soldier={},civilian={}};local sites={}
 for _,site in ipairs(cfg.sites or {})do sites[#sites+1]=site end;shuffle(w,sites)
 local count=0;local capacity=#sites*cfg.maxGroupSize
 for _,id in ipairs(ids or w.order)do
  local a=w.actors[id]
  if a and a.available~=false and supports(a,"group")then
   if count<capacity then local key=a.role=="soldier"and "soldier"or "civilian";pools[key][#pools[key]+1]=id;count=count+1
   else log(w,id,"REJECTED","conversation area capacity; add more sites to expand")end
  end
 end
 shuffle(w,pools.soldier);shuffle(w,pools.civilian)
 local g={kind="GATHERING",reason=reason,ids={},groups={},startedReal=w.realNow,audioStarted=false}
 local siteIndex=0
 while count>=2 and siteIndex<#sites do
  local remainingSites=#sites-siteIndex;local minimum=math.max(cfg.minGroupSize,math.ceil(count/remainingSites))
  local size=math.min(count,cfg.maxGroupSize,minimum+math.floor(random(w)*(cfg.maxGroupSize-minimum+1)))
  if count-size==1 then if size<cfg.maxGroupSize then size=size+1 else size=size-1 end end
  local main=#pools.soldier>#pools.civilian and "soldier"or "civilian";local other=main=="soldier"and "civilian"or "soldier"
  siteIndex=siteIndex+1;local site=sites[siteIndex];local slots=site.formations[tostring(size)]
  local c={id=site.id,kind="GATHERING",ids={},slots=slots,site={x=site.x,y=site.y,z=site.z},startedReal=w.realNow,phase="assembling",durationSeconds=duration or cfg.duration.minimumSeconds+math.floor(random(w)*(cfg.duration.maximumSeconds-cfg.duration.minimumSeconds+1)),durationUnit=cfg.duration.unit}
  for i=1,size do
   local key=main
   if #pools[other]>0 and (#pools[main]==0 or (i>1 and random(w)<cfg.mixChance))then key=other end
   if #pools[key]==0 then key=other end
   local id=table.remove(pools[key]);local a=w.actors[id]
   transition(w,a,"GATHERING",reason);a.conversationGroup=c.id;move(w,a,slots[i]);c.ids[#c.ids+1]=id;g.ids[#g.ids+1]=id;count=count-1
  end
  g.groups[#g.groups+1]=c
 end
 if #g.ids>1 then w.group=g else w.group=nil end
end
local function group(w,kind,reason,ids,duration)
 if w.config.assembliesAvailable==false or w.assemblyReservation then return end
 if w.config.nativeMode and not ids then ids={};for _,id in ipairs(w.order)do if w.actors[id].pilotEligible then ids[#ids+1]=id end end end
 if ids and #ids==0 then return end
 if kind=="GATHERING"then return conversations(w,reason,ids,duration)end
 if w.group then for _,id in ipairs(w.group.ids)do roam(w,w.actors[id],"group interrupted")end end
 local g={kind=kind,ids={},reason=reason,startedReal=w.realNow,holdUntil=nil,completed=false}
 local layout=kind=="MUSTER"and w.config.muster or w.config.gather
 if kind=="MUSTER"and layout.formations then
  local n=#(ids or w.order);for _,f in ipairs(layout.formations)do if n<=#f.slots then layout=f;break end end
 end
 g.columns=layout.columns;g.rows=layout.rows;g.slots=layout.slots
 for i,id in ipairs(ids or w.order)do
  local a=w.actors[id];local target=layout.slots[i]
  if a and a.available~=false and target and supports(a,"group")then
   transition(w,a,kind,reason);move(w,a,target);g.ids[#g.ids+1]=id
  elseif a then log(w,id,"REJECTED","assembly layout capacity reached")end
 end
 if #g.ids>0 then w.group=g else w.group=nil end
end
local function record(a)return {needs=copyNeeds(a.needs),relationships=a.relationships,role=a.role,health=a.health,kind=a.kind,cluster=a.cluster,platform=a.platform,pilotEligible=a.pilotEligible,offlineAt=a.offlineAt,trainingCount=a.trainingCount or 0}end
function Life.Unregister(w,id,reason)
 local a=w.actors[id];if not a then return false end
 a.offlineAt=w.absolute;w.archive[a.name]=record(a);release(w,a)
 if w.group then removeMember(w.group,id);if #w.group.ids==0 then w.group=nil end end
 for i=#w.order,1,-1 do if w.order[i]==id then table.remove(w.order,i)end end
 w.actors[id]=nil;log(w,id,"DEPARTED",reason or "left active area");return true
end
function Life.Register(w,s)
 assert(Life.roles[s.role],"unknown role");assert(type(s.id)=="number"and type(s.name)=="string","invalid identity")
 local current=w.actors[s.id]
 if current and current.name==s.name then
  local scopeChanged=current.cluster~=s.cluster or current.platform~=s.platform or current.pilotEligible~=s.pilotEligible or current.role~=s.role
  if current.cluster~=s.cluster or current.platform~=s.platform then
   if current.facility then roam(w,current,"service interrupted by platform transfer")end
  end
  if s.simulationEligible==false then current.available=false end
  current.label=s.label;current.role=s.role;current.kind=s.kind;current.index=s.index;current.cluster=s.cluster;current.platform=s.platform;current.pilotEligible=s.pilotEligible;current.codeName=s.codeName;current.nameSource=s.nameSource;current.nativeStaffId=s.nativeStaffId;current.capabilities=s.capabilities;current.professionDuty=s.professionDuty
  if scopeChanged then current.serviceBindings,current.unservedNeeds=coverage(w,current)end
  return false end
 if current then Life.Unregister(w,s.id,"slot reassigned")end
 for id,a in pairs(w.actors)do if a.name==s.name then Life.Unregister(w,id,"identity moved to another slot");break end end
 local old=w.archive[s.name]
 local a={id=s.id,name=s.name,label=s.label,codeName=s.codeName,nameSource=s.nameSource,nativeStaffId=s.nativeStaffId,capabilities=s.capabilities,professionDuty=s.professionDuty,role=s.role,kind=s.kind,index=s.index,cluster=s.cluster,platform=s.platform,pilotEligible=s.pilotEligible,state="ROAMING",phase="walking",reason="base arrival",
  needs=copyNeeds(old and old.needs),relationships=(old and old.relationships)or {},health=clamp(old and old.health or 100),
  cooldownUntil=w.absolute+300,held=false,trainingCount=old and old.trainingCount or 0}
 if s.simulationEligible==false then a.available=false end
 if not old then for k in pairs(rates)do a.needs[k]=12+((s.index-1)%10)*2 end end
 if old and old.offlineAt then
  local elapsed=math.max(0,math.min(86400,w.absolute-old.offlineAt));local deferred={}
  if w.config.deferUnboundNeeds then local _,unserved=coverage(w,a);for _,need in ipairs(unserved)do deferred[need]=true end end
  for k,r in pairs(rates)do if not deferred[k]then a.needs[k]=clamp(a.needs[k]+r*elapsed/3600)end end
 end
 a.serviceBindings,a.unservedNeeds=coverage(w,a)
 w.actors[a.id]=a;w.order[#w.order+1]=a.id;log(w,a.id,"ARRIVED",old and "restored person"or "new person")
 emit(w,a.id,"roam");return true
end
-- Explicit manual preparation is synchronous; autonomous dispatch cannot interleave.
-- Validate the whole cohort before releasing any routine/resource.
function Life.PrepareActivity(w,participants,now)
 assert(not w.assemblyReservation,"Another activity reserves the assembly pad")
 assert(not w.group or w.group.kind=="GATHERING","finish muster before manual training")
 assert((w.externalActivities or 0)==0,"shared activity area already reserved")
 local selected={}
 for _,p in ipairs(participants)do
  local a=w.actors[p.id]
  assert(a and a.name==p.identity and a.role=="soldier"and a.available~=false and not a.activityOwner and not selected[p.id],"invalid manual cohort")
  assert(a.state=="ROAMING"or(a.state=="DUTY"and(a.duty=="patrol"or a.duty=="guard"))or
   a.state=="GATHERING"or a.state=="FACILITY_QUEUE"or(a.state=="FACILITY_USE"and a.phase=="travelling"),"routine cannot yield to manual training")
  selected[p.id]=true
 end
 w.actions={};w.realNow=now
 if w.group then
  for _,id in ipairs(w.group.ids)do if not selected[id]and w.actors[id]then roam(w,w.actors[id],"conversation area reserved for manual training")end end
  w.group=nil
 end
 for _,p in ipairs(participants)do
  local a=w.actors[p.id]
  if a.state~="ROAMING"and a.state~="DUTY"then roam(w,a,"prepared for manual training")end
 end
 return w.actions
end
-- External duties retain needs and identity, and yield to later priority orders.
function Life.BeginActivity(w,id,identity,epoch,now)
 local a=w.actors[id]
 assert(a and a.name==identity and a.role=="soldier"and a.available~=false and not a.activityOwner,"actor cannot enter training")
 assert(a.state=="ROAMING"or(a.state=="DUTY"and(a.duty=="patrol"or a.duty=="guard")),"finish existing routine before training")
 w.realNow=now
 local previous={duty=a.duty,remaining=a.dutyUntilReal and math.max(5,a.dutyUntilReal-now)or 120}
 transition(w,a,"DUTY","CQC technique practice")
 a.activityOwner=epoch;w.externalActivities=(w.externalActivities or 0)+1;a.activityPrevious=previous;a.activityPhase="assembling"
 a.phase="assembling";a.duty="training";a.dutyLabel="CQC technique practice";a.dutyBinding="external_session"
 return true
end
function Life.SetActivityPhase(w,id,epoch,phase)
 local a=w.actors[id];if not a or a.activityOwner~=epoch then return false end
 a.activityPhase=phase;a.phase=phase;return true
end
function Life.EndActivity(w,id,identity,epoch,reason,now)
 local a=w.actors[id]
 if not a or a.name~=identity or a.activityOwner~=epoch then return {}end -- a newer order owns this actor
 w.actions={};w.realNow=now;local previous=a.activityPrevious
 if reason=="complete"then a.trainingCount=(a.trainingCount or 0)+1 end
 release(w,a)
 local key=previous and previous.duty
 if a.available~=false and(key=="patrol"or key=="guard")then
  local ok=assignDuty(w,a,key,previous.remaining,"returned from CQC practice")
  if not ok then roam(w,a,"CQC practice ended; next routine")end
 else roam(w,a,"CQC practice ended; next routine")end
 return w.actions
end
function Life.SyncRoster(w,roster,now)
 w.actions={};w.realNow=now;local present={}
 for _,s in ipairs(roster)do assert(not present[s.id],"duplicate roster id");present[s.id]=s.name;Life.Register(w,s)end
 local departed={};for id,a in pairs(w.actors)do if present[id]~=a.name then departed[#departed+1]=id end end
 for _,id in ipairs(departed)do Life.Unregister(w,id)end
 table.sort(w.order,function(a,b)return w.actors[a].index<w.actors[b].index end)
 return w.actions
end
function Life.Create(config,roster,clock,saved)
 local w={config=config,actors={},order={},facilities={},workPosts={},clock=clock,day=(saved and saved.day)or 0,
  absolute=clock+((saved and saved.day)or 0)*86400,realNow=0,actions={},events={},group=nil,lastBell=nil,externalActivities=0,
  randomState=(saved and saved.randomState)or 76391,archive=(saved and saved.actors)or {},autonomousNeeds=config.autonomousNeeds~=false,autonomousSocial=config.autonomousSocial~=false}
 for key,c in pairs(config.facilities)do w.facilities[key]={config=c,queue={},users={},completed=0}end
 for _,c in ipairs(config.workPosts or {})do w.workPosts[#w.workPosts+1]={config=c}end
 for _,s in ipairs(roster)do Life.Register(w,s)end
 return w
end
local function sameTarget(a,b)
 return a and b and a.route==b.route and(a.routePoint or 0)==(b.routePoint or 0)and a.x==b.x and a.y==b.y and a.z==b.z and a.yaw==b.yaw
end
local function sameAccess(a,b)
 if (a==nil)~=(b==nil)then return false end
 for id,v in pairs(a or{})do if not b or b[id]~=v then return false end end
 for id,v in pairs(b or{})do if not a or a[id]~=v then return false end end
 return true
end
local function sameFacility(a,b)
 if not sameAccess(a.allowActors,b.allowActors)then return false end
 if a.service~=b.service or a.cluster~=b.cluster or a.platform~=b.platform or a.capacity~=b.capacity or a.enabled~=b.enabled or a.binding~=b.binding or a.fixtureBinding~=b.fixtureBinding or a.serviceSeconds~=b.serviceSeconds then return false end
 if type(a.queue)~="table"or type(b.queue)~="table"or type(a.uses)~="table"or type(b.uses)~="table"then return false end
 if #a.queue~=#b.queue or #a.uses~=#b.uses then return false end
 for i,p in ipairs(a.queue)do if not sameTarget(p,b.queue[i])then return false end end
 for i,p in ipairs(a.uses)do if not sameTarget(p,b.uses[i])then return false end end
 for k,v in pairs(a.relief or {})do if not b.relief or b.relief[k]~=v then return false end end
 for k,v in pairs(b.relief or {})do if not a.relief or a.relief[k]~=v then return false end end
 return true
end
function Life.SyncFacilities(w,definitions,now)
 w.actions={};w.realNow=now;local remove={};local added=false
 for key,f in pairs(w.facilities)do
  local c=definitions[key]
  if not c or c.enabled==false or(c.minimumGrade and c.completedGrade and c.completedGrade<c.minimumGrade)or not sameFacility(f.config,c)then
   local ids={};for _,id in ipairs(f.queue)do ids[id]=true end;for _,id in pairs(f.users)do ids[id]=true end
   for id in pairs(ids)do local a=w.actors[id];if a and a.facility==key then roam(w,a,"service binding changed or unavailable")end end
   remove[#remove+1]=key
  else f.config=c end
 end
 for _,key in ipairs(remove)do w.facilities[key]=nil end
 for key,c in pairs(definitions)do if not w.facilities[key]then w.facilities[key]={config=c,queue={},users={},completed=0};added=true end end
 if added or #remove>0 then for _,id in ipairs(w.order)do local a=w.actors[id];a.serviceBindings,a.unservedNeeds=coverage(w,a)end end
 w.config.facilities=definitions;return w.actions
end
function Life.ServiceCoverage(w,id)
 local a=w.actors[id];if not a then return nil end
 local bindings,unserved=coverage(w,a);return{bindings=bindings,unservedNeeds=unserved}
end
function Life.RebaseClock(w,clock)
 w.clock=clock;w.absolute=w.day*86400+clock
end
function Life.Request(w,request,clock,now)
 if request.kind=="muster"or request.kind=="gather"then assert(not w.assemblyReservation,"Another activity reserves the assembly pad")end
 w.actions={};w.realNow=now
 if clock~=w.clock then Life.RebaseClock(w,clock)end
 local kind=request.kind
 if kind=="muster"then group(w,"MUSTER",request.reason or "manual muster",request.actors)
 elseif kind=="gather"then group(w,"GATHERING",request.reason or "social gathering",request.actors,request.durationSeconds)
 elseif kind=="roam"then
  if w.group and request.actors then
   local selected={};for _,id in ipairs(request.actors)do selected[id]=true end
   for _,id in ipairs(w.group.ids)do if not selected[id]and w.actors[id]then roam(w,w.actors[id],"group interrupted by dismissal")end end
  end
  w.group=nil
  for _,id in ipairs(request.actors or w.order)do local a=w.actors[id];if a then roam(w,a,"activity cancelled")end end
 elseif kind=="facility"or kind=="duty"then
  if w.group then for _,id in ipairs(w.group.ids)do roam(w,w.actors[id],"group interrupted by facility request")end end
  w.group=nil
  for _,id in ipairs(request.actors or w.order)do
   local a=w.actors[id]
   if a then local ok,e=queue(w,a,request.facility,request.reason or ("visit "..request.facility),kind=="duty");if not ok then log(w,id,"REJECTED",e)end end
  end
 elseif kind=="native_duty"then
  for _,id in ipairs(request.actors or w.order)do local a=w.actors[id];if a then local ok,e=assignDuty(w,a,request.duty or "patrol",request.durationSeconds,request.reason);if not ok then log(w,id,"REJECTED",e)end end end
 elseif kind=="needs"then
  for _,id in ipairs(request.actors or w.order)do
   local a=w.actors[id];if a then for k,v in pairs(request.values or {})do if rates[k]then a.needs[k]=clamp(v)end end end
  end
 elseif kind=="health"then
  for _,id in ipairs(request.actors or w.order)do if w.actors[id]then w.actors[id].health=clamp(request.value or 100)end end
 elseif kind=="autonomy"then
  w.autonomousNeeds=request.enabled;w.autonomousSocial=request.enabled
 else error("unknown life request "..tostring(kind))end
 return w.actions
end
local function atTarget(a,o)
 if not o or o.real==false or o.available==false or o.alive==false or not a.target or not finite(o.x)or not finite(o.y)or not finite(o.z)then return false end
 local p=a.target
 return math.sqrt((o.x-p.x)^2+(o.z-p.z)^2)<.42 and math.abs(o.y-p.y)<.4
end
local function facing(a,o)
 if not o or not o.yaw then return true end
 local d=(o.yaw-a.target.yaw+180)%360-180
 return math.abs(d)<10
end
local function relationships(w,g)
 if g.kind~="GATHERING"then return end
 for i=1,#g.ids do for j=i+1,#g.ids do
  local a,b=w.actors[g.ids[i]],w.actors[g.ids[j]]
  for _,pair in ipairs({{a,b},{b,a}})do
   local x,y=pair[1],pair[2];local r=x.relationships[y.name]or {familiarity=0,affinity=0,meetings=0}
   r.meetings=r.meetings+1;r.familiarity=clamp(r.familiarity+8);r.affinity=clamp(r.affinity+3)
   r.kind=r.familiarity>=24 and "friend"or "acquaintance";x.relationships[y.name]=r
  end
 end end
 for _,id in ipairs(g.ids)do local a=w.actors[id];a.needs.social=clamp(a.needs.social-40)end
end
function Life.Step(w,clock,now,observations,availability)
 w.actions={};w.realNow=now
 for key,f in pairs(w.facilities)do f.blocked=availability and availability[key]==false or false end
 local delta=clock-w.clock
 if delta < -43200 then w.day=w.day+1;delta=delta+86400
 elseif delta<0 then delta=0 end
 local previous=w.absolute
 w.clock=clock;w.absolute=w.day*86400+clock
 if delta>7200 then delta=0 end -- Explicit test time jumps do not create fictitious need hours.
 for _,id in ipairs(w.order)do
  local a=w.actors[id];local o=observations[id];a.observation=o
  local bindings,unserved=coverage(w,a);a.serviceBindings=bindings;a.unservedNeeds=unserved
  local deferred={};if w.config.deferUnboundNeeds then for _,need in ipairs(unserved)do deferred[need]=true end end
  for k,rate in pairs(rates)do if not deferred[k]then a.needs[k]=clamp(a.needs[k]+rate*delta/3600)end end
  local strain=0;for _,k in ipairs({"hunger","thirst","fatigue","hygiene"})do if not deferred[k]then strain=strain+math.max(0,a.needs[k]-85)/15 end end
  if strain>0 then a.health=math.max(math.min(10,a.health),a.health-strain*3*delta/3600)
  elseif a.needs.hunger<40 and a.needs.thirst<40 and a.needs.fatigue<40 then a.health=clamp(a.health+delta/3600)end
  a.nativeLifeStatus=o and o.nativeLifeStatus or nil
  a.available=w.config.strictNativeObservations and not not nativeReady(o)or(not w.config.strictNativeObservations and not(o and(o.available==false or o.real==false or o.alive==false)))
  if not a.available and a.phase~="unavailable"and a.phase~="observed_only"then
   release(w,a);a.state="ROAMING";a.phase=o and o.observeOnly and"observed_only"or"unavailable";a.reason=o and o.unavailableReason or"native character incapacitated"
   if w.group then removeMember(w.group,id);if #w.group.ids==0 then w.group=nil end end
   log(w,id,"NATIVE_UNAVAILABLE",a.reason)
  elseif a.available and(a.phase=="unavailable"or a.phase=="observed_only")then roam(w,a,"native character recovered")end
 end
 for day=math.floor(previous/86400),math.floor(w.absolute/86400)do
  for _,hour in ipairs(w.config.muster.hours)do
   local bell=day*86400+hour*3600
   if previous<bell and w.absolute>=bell and w.lastBell~=bell then
    w.lastBell=bell;group(w,"MUSTER",hour==6 and "06:00 morning muster"or "18:00 evening muster")
   end
  end
 end
 for _,id in ipairs(w.order)do
  local a=w.actors[id];local o=observations[id]
  if a.facility then
   local f=w.facilities[a.facility]
   if not f or not eligibleFacility(w,a,a.facility,f,false)or(f.blocked and a.state=="FACILITY_USE")then
    roam(w,a,f and(f.blocked and "service interrupted: fixture busy"or "local service unavailable")or "service binding removed")
   end
  end
  if a.state=="DUTY"and now>=(a.dutyUntilReal or math.huge)then roam(w,a,"duty complete")end
   if a.state=="DUTY"and a.phase=="travelling"and now-(a.enteredReal or now)>600 then roam(w,a,"duty travel timeout")end
  if a.target and a.phase=="travelling"and not atTarget(a,o)then
   local command,band=travelCommand(w,a,a.target)
   if command.route~=a.travelRoute then a.travelRoute=command.route;emit(w,id,"move",command)end;a.travelBand=band
  end
  if a.target and atTarget(a,o)then
   if not a.held then emit(w,id,"hold",a.target);a.held=true;a.travelBand="standing"end
   if a.state=="MUSTER"then a.phase=facing(a,o)and "attention"or "aligning"
   elseif a.state=="GATHERING"then a.phase="gathered"
   elseif a.state=="DUTY"then
     a.phase=facing(a,o)and "on_duty"or "aligning"
     if a.phase=="on_duty"and not a.dutyStartedReal then
      a.dutyStartedReal=now;a.dutyUntilReal=now+a.dutyDurationSeconds
      log(w,id,"DUTY_STARTED",a.dutyLabel.." at "..a.dutyPost)
     end
    elseif a.state=="FACILITY_QUEUE"then a.phase="waiting"
   elseif a.state=="FACILITY_USE"and a.phase=="travelling"then
    a.phase="using";a.serviceStartedAbsolute=w.absolute;a.serviceUntil=w.absolute+w.facilities[a.facility].config.serviceSeconds
    log(w,id,"SERVICE_STARTED",a.facility)
   end
  elseif a.target and a.phase~="travelling"then
   if a.state=="FACILITY_USE"then a.serviceUntil=nil;a.serviceStartedAbsolute=nil end
   a.phase="travelling";a.held=false;local command,band=travelCommand(w,a,a.target);a.travelBand=band;a.travelRoute=command.route;emit(w,id,"move",command)
  end
 end
 if w.group then
  local g=w.group
  if g.kind=="MUSTER"then
   local all=true
   for _,id in ipairs(g.ids)do if w.actors[id].phase~="attention"then all=false end end
   if all and not g.holdUntil then
    g.holdUntil=w.absolute+w.config.muster.holdSeconds;log(w,0,"GROUP_ASSEMBLED",g.kind)
   end
   if g.holdUntil and w.absolute>=g.holdUntil then
    for _,id in ipairs(g.ids)do roam(w,w.actors[id],"muster dismissed")end
    log(w,0,"GROUP_DISMISSED",g.kind);w.group=nil
   elseif not g.holdUntil and now-g.startedReal>(w.config.musterTravelTimeoutReal or 360)then
    for _,id in ipairs(g.ids)do roam(w,w.actors[id],"assembly timeout")end
    log(w,0,"GROUP_TIMEOUT",g.kind);w.group=nil
   end
  else
   for _,c in ipairs(g.groups)do
    if c.phase~="finished"and c.phase~="cancelled"then
     local all=#c.ids>=2
     for _,id in ipairs(c.ids)do if not w.actors[id]or w.actors[id].phase~="gathered"then all=false end end
     if all and not c.holdUntilReal and not c.holdUntil then
      c.phase="talking";c.assembledReal=now
      if c.durationUnit=="real"then c.holdUntilReal=now+c.durationSeconds else c.holdUntil=w.absolute+c.durationSeconds end
      g.audioStarted=true;log(w,0,"CONVERSATION_ASSEMBLED","group "..c.id.."; "..c.durationSeconds.." "..c.durationUnit.." seconds")
     end
     local finished=(c.holdUntilReal and now>=c.holdUntilReal)or(c.holdUntil and w.absolute>=c.holdUntil)
     local timedOut=not c.assembledReal and now-c.startedReal>(w.config.musterTravelTimeoutReal or 360)
     if finished or timedOut or #c.ids<2 then
      if finished then relationships(w,c)end
      c.phase=finished and "finished"or "cancelled";c.finishedReal=now
      for _,id in ipairs(c.ids)do
       if w.actors[id]and w.actors[id].conversationGroup==c.id then roam(w,w.actors[id],finished and "conversation ended"or "conversation could not assemble")end
       for i=#g.ids,1,-1 do if g.ids[i]==id then table.remove(g.ids,i)end end
      end
      log(w,0,finished and "CONVERSATION_DISMISSED"or "CONVERSATION_CANCELLED","group "..c.id)
     end
    end
   end
   if #g.ids==0 then log(w,0,"GROUP_DISMISSED","GATHERING");w.group=nil end
  end
 end
 for _,id in ipairs(w.order)do
  local a=w.actors[id]
  if a.state=="FACILITY_USE"and a.phase=="using"and w.absolute>=(a.serviceUntil or math.huge)then
   local f=w.facilities[a.facility];local key=a.facility
   for need,value in pairs(f.config.relief)do if need=="health"then a.health=clamp(a.health+value)else a.needs[need]=clamp(a.needs[need]-value)end end
   f.completed=f.completed+1;roam(w,a,key.." completed")
  end
 end
 for key,f in pairs(w.facilities)do
  for slot=1,f.config.capacity do
   if not f.blocked and not f.users[slot]and f.queue[1]then
    local a=w.actors[f.queue[1]]
    if a and a.phase=="waiting"then
     table.remove(f.queue,1);f.users[slot]=a.id
     a.state="FACILITY_USE";a.useSlot=slot;a.phase="travelling";a.held=false
     move(w,a,f.config.uses[slot]);log(w,a.id,"FACILITY_USE",key)
    end
   end
  end
  for i,id in ipairs(f.queue)do local a=w.actors[id];if a then move(w,a,f.config.queue[i])end end
 end
 for _,id in ipairs(w.order)do
  local a=w.actors[id]
  if (a.state=="FACILITY_QUEUE"or a.state=="FACILITY_USE")and a.phase~="using"and now-(a.enteredReal or now)>((w.facilities[a.facility]and w.facilities[a.facility].config.travelTimeoutReal)or 600)then
   log(w,id,"TRAVEL_TIMEOUT",a.facility);roam(w,a,"facility travel timeout")
  end
 end
 if not w.group or w.config.allowConcurrentLocalServices then
  for _,id in ipairs(w.order)do
   local a=w.actors[id]
   if a.available~=false and not a.activityOwner and (a.state=="ROAMING"or a.state=="DUTY")and w.absolute>=(a.cooldownUntil or 0)then
    local selected,highest=nil,64
    local canVisit=not w.config.nativeMode or a.pilotEligible
    if w.autonomousNeeds then for need,key in pairs(needFacility)do if a.needs[need]>highest and resolveFacility(w,a,key,false,false)then selected=key;highest=a.needs[need]end end end
    if w.autonomousNeeds and a.health<65 and resolveFacility(w,a,"clinic",false,false)then selected="clinic"end
    if selected then local ok=queue(w,a,selected,"need: "..selected);if not ok then a.cooldownUntil=w.absolute+60 end
    elseif not w.group and(w.externalActivities or 0)==0 and canVisit and w.autonomousSocial and a.needs.social>60 then
     local members={id}
     for _,other in ipairs(w.order)do if other~=id and w.actors[other].state=="ROAMING"and(not w.config.nativeMode or w.actors[other].pilotEligible)then members[#members+1]=other;if #members==4 then break end end end
     if #members>1 then group(w,"GATHERING","social need",members);break end
    elseif w.config.autonomousDuties and a.professionDuty and a.state=="ROAMING"then
    assignDuty(w,a,a.professionDuty,120,"scheduled department rounds")
   elseif w.config.autonomousDuties and a.role=="soldier"and a.state=="ROAMING"then
     local duty=a.pilotEligible and a.index%4==0 and "guard"or "patrol"
      local ok=assignDuty(w,a,duty,90+(a.index%4)*20,"scheduled "..duty)
      if not ok then assignDuty(w,a,"patrol",120,"scheduled patrol; no free guard post")end
    end
   end
  end
 end
 return w.actions
end
function Life.Snapshot(w)
 local actors,facilities={},{}
 local muster={};for k,v in pairs(w.config.muster)do muster[k]=v end
 for _,f in ipairs(w.config.muster.formations or {})do if #w.order<=#f.slots then muster.slots=f.slots;muster.columns=f.columns;muster.rows=f.rows;break end end
 for _,id in ipairs(w.order)do
  local a=w.actors[id];local o=a.observation or {}
  actors[#actors+1]={id=id,name=a.name,label=a.label,index=a.index,codeName=a.codeName,nameSource=a.nameSource,nativeStaffId=a.nativeStaffId,role=a.role,state=a.state,phase=a.phase,reason=a.reason,
   cluster=a.cluster,platform=a.platform,pilotEligible=a.pilotEligible,serviceBindings=a.serviceBindings,unservedNeeds=a.unservedNeeds,deferredUnboundNeeds=w.config.deferUnboundNeeds or false,activityOwner=a.activityOwner,trainingCount=a.trainingCount or 0,duty=a.duty,dutyLabel=a.dutyLabel,dutyBinding=a.dutyBinding,dutyPost=a.dutyPost,dutyStartedReal=a.dutyStartedReal,dutyUntilReal=a.dutyUntilReal,conversationGroup=a.conversationGroup,movementBand=a.travelBand,needs=a.needs,health=a.health,healthSource="needs simulation; not native hitpoints",available=a.available,nativeLifeStatus=a.nativeLifeStatus,kind=a.kind,relationships=a.relationships,target=a.target,facility=a.facility,serviceStartedAbsolute=a.serviceStartedAbsolute,serviceUntil=a.serviceUntil,real=o.real,presenceSource=o.presenceSource,equip=o.equip,
   x=o.x,y=o.y,z=o.z,yaw=o.yaw}
 end
 for key,f in pairs(w.facilities)do
  local count=0;for _ in pairs(f.users)do count=count+1 end
  facilities[key]={label=f.config.label,capacity=f.config.capacity,queue=f.queue,users=f.users,occupied=count,
   service=f.config.service or key,cluster=f.config.cluster,platform=f.config.platform,enabled=f.config.enabled~=false,binding=f.config.binding or "legacy_prototype",minimumGrade=f.config.minimumGrade,completedGrade=f.config.completedGrade,completed=f.completed,blockedByPlayer=f.blocked or false,prototypePad=f.config.prototypePad,fixtureBinding=f.config.fixtureBinding,limitation=f.config.limitation}
 end
 return {version=w.config.version,clockSeconds=w.clock,day=w.day,absolute=w.absolute,realTime=w.realNow,
  actors=actors,facilities=facilities,events=w.events,group=w.group,externalActivities=w.externalActivities or 0,assemblyReservation=w.assemblyReservation,muster=muster,duties=Life.duties,
  states=Life.states,roles=Life.roles,deferUnboundNeeds=w.config.deferUnboundNeeds or false,strictNativeObservations=w.config.strictNativeObservations or false,autonomousDuties=w.config.autonomousDuties,autonomousNeeds=w.autonomousNeeds,autonomousSocial=w.autonomousSocial}
end
function Life.Save(w)
 local actors={};for name,r in pairs(w.archive)do actors[name]=r end
 for _,id in ipairs(w.order)do local a=w.actors[id];actors[a.name]=record(a)end
 return {day=w.day,randomState=w.randomState,actors=actors}
end
return Life
