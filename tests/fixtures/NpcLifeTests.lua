-- Behavioral tests exercise the same pure core interface used by the live adapter.
local Tests={}
function Tests.Run(Life,config,Registry)
 config.autonomousNeeds=false;config.autonomousSocial=false
 local results={}
 local roster={}
 local roles={"contractor","contractor","doctor","doctor","contractor","contractor","nurse","nurse"}
 for i=1,8 do roster[i]={id=i,name="test_"..i,label="Test "..i,role=roles[i],index=i}end
 local function create(clock)return Life.Create(config,roster,clock or 43200)end
 local function obs(w)
  local o={}
  for _,id in ipairs(w.order)do
   local t=w.actors[id].target or {x=0,y=0,z=0,yaw=0}
   o[id]={x=t.x,y=t.y,z=t.z,yaw=t.yaw,real=true,equip=0}
  end
  return o
 end
 local function step(w,t,r)return Life.Step(w,t,r or (w.realNow+1),obs(w))end
 local function test(name,fn)local ok,e=pcall(fn);assert(ok,name..": "..tostring(e));results[#results+1]="PASS "..name end
 test("06:00 / 18:00 muster, exactly two game minutes, no duplicate bell",function()
  local w=create(21599);step(w,21600);assert(w.group and w.group.kind=="MUSTER")
  step(w,21601);assert(w.group.holdUntil==21721)
  step(w,21720);assert(w.group);step(w,21721);assert(not w.group)
  for _,id in ipairs(w.order)do assert(w.actors[id].state=="ROAMING")end
  step(w,21722);assert(not w.group)
  step(w,64799);assert(not w.group);step(w,64800);assert(w.group.reason=="18:00 evening muster")
 end)
 test("midnight calendar preserves next morning bell",function()
  local w=create(86399);step(w,0);assert(w.day==1);step(w,21599);assert(not w.group)
  step(w,21600);assert(w.group);assert(w.lastBell==86400+21600)
 end)
 test("single toilet, FIFO ordering, queue advances and needs relieved",function()
  local w=create();Life.Request(w,{kind="facility",facility="toilet"},43200,0)
  for _,id in ipairs(w.order)do w.actors[id].needs.bladder=95 end
  step(w,43201);local f=w.facilities.toilet
  assert(f.users[1]==1 and #f.queue==7 and f.queue[1]==2)
  step(w,43202);assert(w.actors[1].phase=="using")
  step(w,43322);assert(w.actors[1].state=="ROAMING"and w.actors[1].needs.bladder<1)
  assert(f.users[1]==2 and #f.queue==6 and f.completed==1)
 end)
 test("muster interrupts queues/use without leaking reservations",function()
  local w=create();Life.Request(w,{kind="facility",facility="shower"},43200,0);step(w,43201)
  assert(w.facilities.shower.users[1]==1)
  Life.Request(w,{kind="muster"},43201,2)
  for _,f in pairs(w.facilities)do assert(#f.queue==0 and next(f.users)==nil)end
  for _,id in ipairs(w.order)do assert(w.actors[id].state=="MUSTER")end
 end)
 test("partial facility request safely cancels the previous group",function()
  local w=create();Life.Request(w,{kind="gather"},43200,0)
  Life.Request(w,{kind="facility",facility="toilet",actors={1}},43200,1)
  assert(not w.group and w.actors[1].state=="FACILITY_QUEUE")
  for i=2,8 do assert(w.actors[i].state=="ROAMING")end
 end)
 test("civilian excluded from soldier training; nurse/doctor medical duties",function()
  local rr={{id=1,name="civilian",label="Nurse",role="nurse",index=1},{id=2,name="soldier",label="Soldier",role="soldier",index=2}}
  local w=Life.Create(config,rr,43200);Life.Request(w,{kind="duty",facility="training"},43200,0)
  assert(w.actors[1].state=="ROAMING"and w.actors[2].facility=="training")
  Life.Request(w,{kind="roam"},43200,1);Life.Request(w,{kind="duty",facility="clinic"},43200,2)
  assert(w.actors[1].facility=="clinic"and w.actors[2].state=="ROAMING")
 end)
 test("three same-group conversations create reciprocal friendship and preserve records",function()
  local w=create();local clock=43200;local real=1
  for n=1,3 do
   Life.Request(w,{kind="gather",actors={1,2}},clock,real);step(w,clock+1,real+1)
   local c=w.group.groups[1];assert(c.holdUntilReal==real+1+c.durationSeconds)
   real=c.holdUntilReal;step(w,clock+2,real);assert(not w.group)
   clock=clock+3;real=real+1
  end
  local a,b=w.actors[1],w.actors[2]
  assert(a.relationships[b.name].kind=="friend"and b.relationships[a.name].kind=="friend")
  local restored=Life.Create(config,roster,clock,Life.Save(w))
  assert(restored.actors[1].relationships[b.name].meetings==3 and restored.randomState==w.randomState)
 end)
 test("needs stay bounded and unavailable/full facilities reject cleanly",function()
  local w=create()
  Life.Request(w,{kind="needs",actors={1},values={hunger=150,thirst=-10}},43200,0)
  assert(w.actors[1].needs.hunger==100 and w.actors[1].needs.thirst==0)
  local count=#w.events;Life.Request(w,{kind="facility",facility="missing"},43200,1)
  assert(#w.events>count and w.actors[1].state=="ROAMING")
 end)
 test("unreachable facility safely releases its queue reservation",function()
  local w=create();Life.Request(w,{kind="autonomy",enabled=false},43200,0)
  Life.Request(w,{kind="facility",facility="toilet",actors={1}},43200,1)
  Life.Step(w,43201,602,{[1]={x=100,y=0,z=100,real=true}})
  assert(w.actors[1].state=="ROAMING"and #w.facilities.toilet.queue==0 and next(w.facilities.toilet.users)==nil)
 end)
 test("real shower is single capacity and respects the player's entrance",function()
  local w=create();local f=w.facilities.shower;assert(f.config.capacity==1 and #f.config.uses==1)
  Life.Request(w,{kind="facility",facility="shower"},43200,0)
  Life.Step(w,43201,1,obs(w),{shower=false})
  assert(next(f.users)==nil and #f.queue==8 and f.blocked)
  Life.Step(w,43202,2,obs(w),{shower=true})
  assert(f.users[1]==1 and #f.queue==7 and not f.blocked)
  step(w,43203);assert(w.actors[1].phase=="using")
  step(w,43323);assert(f.completed==1 and f.users[1]==2 and #f.queue==6)
 end)

 local function expanded()
  local rr={};for _,s in ipairs(roster)do rr[#rr+1]=s end
  for i=9,18 do rr[#rr+1]={id=i,name="soldier_"..i,label="Soldier "..i,role="soldier",kind="soldier",index=i}end
  return rr
 end
 test("eight to eighteen auto-enrolls without resetting existing needs or relationships",function()
  local w=create();w.actors[1].needs.hygiene=77;w.actors[1].health=83
  w.actors[1].relationships.test_2={kind="friend",meetings=4}
  Life.SyncRoster(w,expanded(),1);assert(#w.order==18)
  assert(w.actors[1].needs.hygiene==77 and w.actors[1].health==83 and w.actors[1].relationships.test_2.meetings==4)
  for i=9,18 do local a=w.actors[i];assert(a.role=="soldier"and a.health==100);for k in pairs(a.needs)do assert(a.needs[k]>=0 and a.needs[k]<=100)end end
  local n=#w.events;Life.SyncRoster(w,expanded(),2);assert(#w.order==18 and #w.events==n and #w.actions==0)
 end)
 test("eighteen muster positions form six across and three deep",function()
  local w=Life.Create(config,expanded(),43200);Life.Request(w,{kind="muster"},43200,0)
  assert(#w.group.ids==18 and w.group.columns==6 and w.group.rows==3)
  local routes={};for _,id in ipairs(w.order)do local a=w.actors[id];assert(a.state=="MUSTER"and a.target);assert(not routes[a.target.route]);routes[a.target.route]=true end
  step(w,43201);assert(w.group.holdUntil==43321);step(w,43321);assert(not w.group)
  for _,id in ipairs(w.order)do assert(w.actors[id].state=="ROAMING")end
  assert(Life.Snapshot(w).muster.columns==6)
 end)
 test("departure releases occupied facility and returning identity restores records on a new id",function()
  local w=create();w.actors[1].needs.thirst=93;w.actors[1].health=71;w.actors[1].relationships.test_2={kind="friend",meetings=8}
  Life.Request(w,{kind="facility",facility="toilet",actors={1}},43200,0);step(w,43201);assert(w.facilities.toilet.users[1]==1)
  local priorHealth=w.actors[1].health;Life.Unregister(w,1);assert(#w.order==7 and next(w.facilities.toilet.users)==nil and #w.facilities.toilet.queue==0)
  Life.Register(w,{id=99,name="test_1",label="Returned",role="contractor",index=1})
  assert(w.actors[99].needs.thirst>93 and w.actors[99].health==priorHealth and w.actors[99].relationships.test_2.meetings==8)
 end)
 test("group departure and roster slot reuse cannot duplicate or transfer identities",function()
  local w=create();Life.Request(w,{kind="muster"},43200,0);Life.Unregister(w,8);assert(#w.group.ids==7)
  w.actors[1].needs.hygiene=99;Life.Register(w,{id=1,name="new_person",label="New",role="soldier",index=1})
  assert(w.actors[1].needs.hygiene~=99 and w.archive.test_1.needs.hygiene==99 and #w.order==7)
  Life.Register(w,{id=88,name="new_person",label="Same",role="soldier",index=1});assert(not w.actors[1]and w.actors[88]and #w.order==7)
 end)
 test("saved records survive departure, restart and re-enrollment",function()
  local w=create();w.actors[3].needs.hunger=88;w.actors[3].health=62;Life.Unregister(w,3)
  local restored=Life.Create(config,{},43200,Life.Save(w));assert(#restored.order==0)
  Life.Register(restored,{id=50,name="test_3",label="Doctor",role="doctor",index=3})
  assert(restored.actors[50].needs.hunger==88 and restored.actors[50].health==62)
 end)
 test("common facilities and clinical care accept soldiers while medical duty stays role-specific",function()
  local w=Life.Create(config,expanded(),43200)
  for _,key in ipairs({"mess","water","bunk","shower","toilet","clinic"})do
   Life.Request(w,{kind="facility",facility=key,actors={9}},43200,0);assert(w.actors[9].facility==key);Life.Request(w,{kind="roam"},43200,1)
  end
  Life.Request(w,{kind="duty",facility="clinic",actors={9}},43200,2);assert(w.actors[9].state=="ROAMING")
 end)
 test("simulated health is bounded, responds to severe unmet needs and improves at clinic",function()
  local w=create();Life.Request(w,{kind="needs",actors={1},values={hunger=100,thirst=100,fatigue=100,hygiene=100}},43200,0)
  step(w,46800);assert(w.actors[1].health<100 and w.actors[1].health>=10)
  Life.Request(w,{kind="health",actors={1},value=-50},46800,1);assert(w.actors[1].health==0)
  Life.Request(w,{kind="health",actors={1},value=150},46800,2);assert(w.actors[1].health==100)
  Life.Request(w,{kind="needs",actors={1},values={hunger=0,thirst=0,fatigue=0,hygiene=0}},46800,3);Life.Request(w,{kind="health",actors={1},value=40},46800,3);Life.Request(w,{kind="facility",facility="clinic",actors={1}},46800,4)
  step(w,46801);step(w,46802);assert(w.actors[1].phase=="using")
  step(w,46802+config.facilities.clinic.serviceSeconds);assert(w.actors[1].health>59 and w.actors[1].health<61)
  assert(Life.Snapshot(w).actors[1].healthSource:match("not native"))
 end)
 test("eighteen people split into bounded unique conversation groups and local relationships",function()
  local w=Life.Create(config,expanded(),43200);Life.Request(w,{kind="gather"},43200,0)
  assert(#w.group.ids==18 and #w.group.groups>=5)
  local seen={};local first=w.group.groups[1];local last=w.group.groups[#w.group.groups]
  for _,c in ipairs(w.group.groups)do
   assert(#c.ids>=2 and #c.ids<=4 and #c.slots==#c.ids)
   for _,id in ipairs(c.ids)do assert(not seen[id]and w.actors[id].conversationGroup==c.id);seen[id]=true end
  end
  step(w,43201,1);assert(w.group.audioStarted)
  step(w,43202,302);assert(not w.group)
  local a,b=w.actors[first.ids[1]],w.actors[first.ids[2]]
  assert(a.relationships[b.name].meetings==1 and b.relationships[a.name].meetings==1)
  assert(not a.relationships[w.actors[last.ids[1]].name])
 end)
 if Registry then
  test("registry deduplicates ids and names and dispatches only to the owning adapter",function()
   local called={};local rr={{id=1,name="person_a",role="contractor"}}
   local a={GetRoster=function()return rr end,GetObservations=function()return {[1]={x=1,y=0,z=1}}end,ApplyLifeAction=function(x)called[#called+1]="a"end}
   local b={GetRoster=function()return {{id=1,name="conflict",role="soldier"},{id=2,name="person_b",role="soldier"},{id=3,name="person_a",role="soldier"}}end,GetObservations=function()return {[1]={x=99},[2]={x=2}}end,ApplyLifeAction=function(x)called[#called+1]="b"end}
   local reg=Registry.Create();Registry.AddProvider(reg,"a",a);Registry.AddProvider(reg,"b",b)
   local r,o=Registry.Collect(reg);assert(#r==2 and o[1].x==1 and o[2].x==2)
   Registry.Apply(reg,{actor=2,kind="roam"},1);Registry.Apply(reg,{actor=1,kind="roam"},1);assert(called[1]=="b"and called[2]=="a")
  end)
  test("registry preserves person numbering across arrival, departure and return",function()
   local rr={{id=1,name="a",role="contractor"}};local adapter={GetRoster=function()return rr end,GetObservations=function()return {}end,ApplyLifeAction=function()end}
   local reg=Registry.Create();Registry.AddProvider(reg,"people",adapter);local r=Registry.Collect(reg);assert(r[1].index==1)
   rr={{id=5,name="b",role="soldier"}};r=Registry.Collect(reg);assert(r[1].index==2)
   rr={{id=9,name="a",role="contractor"},{id=5,name="b",role="soldier"}};r=Registry.Collect(reg);assert(r[1].index==1 and r[2].index==2)
  end)
 end


 test("native incapacitation releases facilities without fake service or animation commands",function()
  local w=create();Life.Request(w,{kind="facility",facility="shower",actors={1}},43200,0);step(w,43201);step(w,43202);assert(w.actors[1].phase=="using")
  local o=obs(w);o[1].available=false;o[1].nativeLifeStatus=4
  Life.Step(w,43350,3,o);assert(w.actors[1].phase=="unavailable"and w.facilities.shower.completed==0 and next(w.facilities.shower.users)==nil)
  for _,a in ipairs(w.actions)do assert(a.actor~=1)end
  Life.Request(w,{kind="facility",facility="shower",actors={1}},43350,4);assert(w.actors[1].phase=="unavailable")
  o[1].available=true;o[1].nativeLifeStatus=0;Life.Step(w,43351,5,o);assert(w.actors[1].phase=="walking")
 end)
 if Registry then test("large native staff ids preserve distinct identities and unsupported ids fall back to locators",function()
  assert(Registry.StaffIdentity(6707201550846201,"a")~="mb_staff_"..tostring(6707201550846201))
  assert(Registry.StaffIdentity(6707201550846201,"a")=="mb_staff_6707201550846201")
  assert(Registry.StaffIdentity(6707201550846201,"a")~=Registry.StaffIdentity(6707201550846202,"b"))
  assert(Registry.StaffIdentity(nil,"fallback")=="fallback"and Registry.StaffIdentity(9007199254740992,"wide")=="wide")
 end)end

 test("muster fast route retains its nearby entry and slows for the final approach",function()
  local policy=config.muster.travel;local prior=policy.enabled;policy.enabled=true
  local w=create();w.actors[1].role="soldier";w.actors[1].kind="soldier";local target=config.muster.formations[1].slots[1];local o=obs(w)
  o[1]={x=target.x+35,y=target.y+8,z=target.z,yaw=target.yaw,real=true}
  Life.Step(w,43200,1,o);Life.Request(w,{kind="muster",actors={1}},43200,2)
  assert(w.actions[1].target.movementBand=="double-time-far"and w.actions[1].target.urgency=="muster")
  local entry=w.actors[1].rushEntry;assert(entry and w.actions[1].target.route:find("_e"..(entry-1).."_"))
  o[1].x=target.x+10;o[1].y=target.y;Life.Step(w,43201,3,o)
  assert(w.actors[1].travelBand=="double-time"and w.actors[1].rushEntry==entry)
  o[1].x=target.x+2;Life.Step(w,43202,4,o);assert(w.actors[1].travelBand=="walk")
  o[1].x=target.x;Life.Step(w,43203,5,o);assert(w.actors[1].phase=="attention"and w.actions[1].kind=="hold")
  policy.enabled=prior
 end)
 test("gatherings and facility visits retain their ordinary movement",function()
  local w=create();Life.Request(w,{kind="gather",actors={1,2}},43200,1)
  assert(w.actions[1].target.movementBand=="walk"and not w.actions[1].target.urgency)
  Life.Request(w,{kind="facility",facility="shower",actors={1}},43200,2)
  local action=w.actions[#w.actions];assert(action.kind=="move"and not action.target.urgency)
 end)
 test("muster cancellation removes urgency and reservations",function()
  local w=create();Life.Request(w,{kind="muster",actors={1}},43200,1)
  Life.Request(w,{kind="roam",actors={1}},43200,2)
  assert(w.actions[1].kind=="roam"and w.actors[1].target==nil and w.actors[1].travelBand==nil)
 end)
 test("each conversation waits for its own last arrival and dismisses independently",function()
  local w=Life.Create(config,expanded(),43200);Life.Request(w,{kind="gather"},43200,0)
  local early,late=w.group.groups[1],w.group.groups[2];local o=obs(w);local delayed=late.ids[1]
  o[delayed].x=o[delayed].x+20;Life.Step(w,43201,1,o)
  assert(early.assembledReal==1 and not late.assembledReal)
  local earlyEnd=early.holdUntilReal;Life.Step(w,43202,earlyEnd,o)
  assert(early.phase=="finished"and late.phase=="assembling")
  o=obs(w);Life.Step(w,43203,earlyEnd+1,o)
  assert(late.assembledReal==earlyEnd+1 and late.holdUntilReal==earlyEnd+1+late.durationSeconds)
  Life.Step(w,43204,late.holdUntilReal,obs(w));assert(late.phase=="finished")
 end)
 test("real durations vary within sixty to three hundred seconds and ignore game-time jumps",function()
  local w=create();local durations={}
  for n=1,20 do
   Life.Request(w,{kind="gather",actors={1,2}},43200,n);step(w,43201,n+1)
   local c=w.group.groups[1];assert(c.durationSeconds>=60 and c.durationSeconds<=300);durations[c.durationSeconds]=true
   step(w,50000,n+2);assert(w.group and c.phase=="talking")
  end
  local count=0;for _ in pairs(durations)do count=count+1 end;assert(count>5)
 end)
 test("group membership changes while preserving a majority of same-role encounters",function()
  local w=Life.Create(config,expanded(),43200);local same,mixed=0,0;local signatures={}
  for n=1,60 do
   Life.Request(w,{kind="gather"},43200,n)
   local signature={}
   for _,c in ipairs(w.group.groups)do
    for i=1,#c.ids do
     signature[#signature+1]=c.ids[i]
     for j=i+1,#c.ids do
      if (w.actors[c.ids[i]].role=="soldier")== (w.actors[c.ids[j]].role=="soldier")then same=same+1 else mixed=mixed+1 end
     end
    end
   end
   signatures[table.concat(signature,",")]=true
  end
  local count=0;for _ in pairs(signatures)do count=count+1 end
  assert(count>40 and mixed>0 and same>mixed*2)
 end)
 test("conversation departure and interruption clear memberships and native targets",function()
  local w=create();Life.Request(w,{kind="gather",actors={1,2}},43200,0)
  Life.Unregister(w,1);step(w,43201,1);assert(not w.group and w.actors[2].state=="ROAMING"and not w.actors[2].conversationGroup)
  Life.Request(w,{kind="gather"},43200,2);Life.Request(w,{kind="muster"},43200,3)
  for _,id in ipairs(w.order)do assert(w.actors[id].state=="MUSTER"and not w.actors[id].conversationGroup)end
 end)
 test("new arrivals join the next gathering and overflow remains bounded by configured sites",function()
  local w=create();Life.SyncRoster(w,expanded(),1);Life.Request(w,{kind="gather"},43200,2);assert(#w.group.ids==18)
  for i=19,40 do Life.Register(w,{id=i,name="extra_"..i,label="Extra",role="soldier",kind="soldier",index=i})end
  Life.Request(w,{kind="gather"},43200,3);assert(#w.group.ids==#config.gather.sites*config.gather.maxGroupSize and #w.group.groups==#config.gather.sites)
  local seen={};for _,c in ipairs(w.group.groups)do assert(#c.ids<=4);for _,id in ipairs(c.ids)do assert(not seen[id]);seen[id]=true end end
  assert(w.actors[40].state=="ROAMING")
 end)
 test("bounded duration override and individual dismissal cannot strand other group members",function()
  local w=create();Life.Request(w,{kind="gather",durationSeconds=60},43200,0);step(w,43201,1)
  for _,c in ipairs(w.group.groups)do assert(c.holdUntilReal==61)end
  Life.Request(w,{kind="roam",actors={1}},43200,2);assert(not w.group)
  for _,id in ipairs(w.order)do assert(w.actors[id].state=="ROAMING"and not w.actors[id].conversationGroup)end
  local ok=pcall(Life.Request,w,{kind="gather",durationSeconds=10},43200,3);assert(not ok)
 end)
 return table.concat(results,"\n").."\nALL "..#results.." BEHAVIORAL TESTS PASSED\n"
end
return Tests
