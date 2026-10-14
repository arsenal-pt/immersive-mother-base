-- One-actor native bed prototype. Manual only; no camera, player, rumble or needs relief.
local M={}
function M.Create(core,world,soldiers)
 local api={active=false,last=nil};local run;local nextTick=0
 local function now()return Time.GetRawElapsedTimeSinceStartUp()end
 local function safe()return vars.missionCode==30050 and gvars.usingNormalMissionSlot and MotherBaseStage.GetCurrentCluster()==0 and MotherBaseStage.GetCurrentLayout()==3 and not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()end
 local function same(r)return safe()and soldiers.GetNativeInfo()[r.id]==r.info and GameObject.SendCommand(r.id,{id="GetStaffId"})==r.staff end
 local function request(r,c)assert(same(r),"native soldier identity changed");return GameObject.SendCommand(r.id,c)end
 function api.Stop(reason)
  if not run then return false end
  local r=run;run=nil;api.active=false;local errors={}
  if same(r)then
   local ok,e=pcall(function()
    if r.sleepProbe and GameObject.SendCommand(r.id,{id="GetLifeStatus"})==TppGameObject.NPC_LIFE_STATE_SLEEP then request(r,{id="RecoveryStamina",isDelay=false})end
    if r.clock then local t=math.floor(r.clock)%86400;core.RebaseClock(world,t);TppClock.SetTime(string.format("%02d:%02d:%02d",math.floor(t/3600),math.floor(t/60)%60,t%60))end
    if r.fieldBrain then TppEnemy.SetSoldierType(r.id,EnemyType.TYPE_DD)end
    if r.unarmed then request(r,{id="SetUnarmed",enabled=false})end
    request(r,{id="SetSaluteDisable",enabled=false});request(r,{id="SetSaluteMoraleDisable",enabled=false});request(r,{id="SetDisableOccasionalChat",disable=false})
    r.info.activityOwner=nil;r.info.lifeControlled=false;r.info.target=nil
    local orders=core.EndActivity(world,r.id,r.identity,r.epoch,reason or"outdoor rest test ended",world.realNow)
    for _,a in ipairs(orders)do soldiers.ApplyLifeAction(a,world.realNow)end
   end)
   if not ok then errors[#errors+1]=tostring(e)end
  end
  api.last={id=r.id,label=r.label,reason=reason,seconds=now()-r.started,cleanupErrors=errors,needsReliefApplied=false,staff=r.staff}
  return #errors==0
 end
 function api.Start(yaw,seconds)
  assert(not run and safe(),"one outdoor rest pilot requires normal Command platform")
  assert(not world.group or world.group.kind=="GATHERING","finish muster first")
  yaw=yaw or 0;assert(yaw==0 or yaw==90 or yaw==180 or yaw==270,"unsupported bed direction")
  local best,score
  for _,p in ipairs(soldiers.GetRoster())do
   local a=world.actors[p.id];local info=soldiers.GetNativeInfo()[p.id]
   if p.cluster==1 and p.platform==0 and a and a.available~=false and not a.activityOwner and info and not info.activityOwner and(a.state=="ROAMING"or a.state=="DUTY"and(a.duty=="patrol"or a.duty=="guard")or a.state=="FACILITY_QUEUE"or a.state=="GATHERING")then
    local v=GameObject.SendCommand(p.id,{id="GetPosition"});local distance=(v:GetX()-24.05)^2+(v:GetZ()+15)^2
    if GameObject.SendCommand(p.id,{id="GetLifeStatus"})==TppGameObject.NPC_LIFE_STATE_NORMAL and GameObject.SendCommand(p.id,{id="GetStateFlag"})==0 and math.abs(v:GetY())<.5 and(not score or distance<score)then best=p;score=distance end
   end
  end
  assert(best,"No available ground-deck soldier; finish their current routine first")
  local r={id=best.id,identity=best.name,label=best.label,info=soldiers.GetNativeInfo()[best.id],staff=best.nativeStaffId,started=now(),deadline=now()+math.min(300,math.max(20,seconds or 120)),epoch="outdoor_rest_"..math.floor(now()*1000),route="nlab_outdoor_sleep_"..yaw}
  local orders=core.PrepareActivity(world,{{id=r.id,identity=r.identity}},world.realNow)
  for _,a in ipairs(orders)do soldiers.ApplyLifeAction(a,world.realNow)end
  core.BeginActivity(world,r.id,r.identity,r.epoch,world.realNow);run=r;api.active=true
  r.info.activityOwner=r.epoch;r.info.lifeControlled=true;r.info.target=nil;r.info.detourUntil=nil
  local a=world.actors[r.id];a.duty="rest";a.dutyLabel="Outdoor mattress sleep test";a.dutyBinding="native_bed_route"
  local ok,e=pcall(function()
   request(r,{id="SetSaluteDisable",enabled=true});request(r,{id="SetSaluteMoraleDisable",enabled=true});request(r,{id="SetDisableOccasionalChat",disable=true})
   request(r,{id="SetSneakRoute",route=r.route,point=0,isRelaxed=true})
   core.SetActivityPhase(world,r.id,r.epoch,"rest_approach")
  end)
  if not ok then api.Stop("start failed");error(e)end
  return r.label
 end
 function api.Update()
  if now()<nextTick then return end;nextTick=now()+.5
  local r=run;if not r then return end
  if not same(r)or not world.actors[r.id]or world.actors[r.id].activityOwner~=r.epoch then api.Stop("priority routine or context changed");return end
  local ok,e=pcall(function()
   local life=GameObject.SendCommand(r.id,{id="GetLifeStatus"});r.nativeLifeStatus=life
   if life~=TppGameObject.NPC_LIFE_STATE_NORMAL and not(r.sleepProbe and life==TppGameObject.NPC_LIFE_STATE_SLEEP)then api.Stop("soldier unavailable");return end
   local v=GameObject.SendCommand(r.id,{id="GetPosition"});r.position={x=v:GetX(),y=v:GetY(),z=v:GetZ()}
   r.onRoute=GameObject.SendCommand(r.id,{id="IsOnRoute",route=r.route})==true
   r.atSite=(v:GetX()-24.05)^2+(v:GetZ()+15)^2<.5 and math.abs(v:GetY())<.5
   if r.atSite then core.SetActivityPhase(world,r.id,r.epoch,"native_bed_action_test")end
   if r.sleepProbe and now()>=r.probeUntil then api.Stop("native sleep pose probe finished")
   elseif now()>=r.deadline then api.Stop("bounded rest test finished")end
  end)
  if not ok then api.Stop("update failed: "..tostring(e))end
 end
 function api.OwnedSleepId()
  local r=run;if not(r and r.sleepProbe)then return end
  local ok,v=pcall(function()
   return same(r)and GameObject.SendCommand(r.id,{id="GetLifeStatus"})==TppGameObject.NPC_LIFE_STATE_SLEEP and r.id
  end)
  if ok and v then return v end
 end
 function api.TryNativeSleep()
  assert(run and same(run)and run.atSite,"reserved actor must reach mattress first")
  assert(type(TppGameObject.NPC_LIFE_STATE_SLEEP)=="number","native sleep enum missing")
  assert(GameObject.SendCommand(run.id,{id="GetLifeStatus"})==TppGameObject.NPC_LIFE_STATE_NORMAL,"healthy awake actor required")
  run.sleepProbe=true;run.probeUntil=now()+45
  request(run,{id="ChangeLifeState",state=TppGameObject.NPC_LIFE_STATE_SLEEP})
 end
 function api.TryNight()
  assert(run and same(run),"active rest test required")
  run.clock=run.clock or vars.clock;core.RebaseClock(world,82800);TppClock.SetTime("23:00:00")
  request(run,{id="SetSneakRoute",route=run.route,point=0,isRelaxed=true})
 end
 function api.TryUnarmed()
  assert(run and same(run),"active rest test required");run.unarmed=true
  request(run,{id="SetUnarmed",enabled=true})
  request(run,{id="SetSneakRoute",route=run.route,point=0,isRelaxed=true})
 end
 function api.TryFieldBrain()
  assert(run and same(run),"active rest test required");run.fieldBrain=true
  TppEnemy.SetSoldierType(run.id,EnemyType.TYPE_SOVIET)
  request(run,{id="SetFriendly",enabled=true});request(run,{id="SetSneakRoute",route=run.route,point=0,isRelaxed=true})
 end
 function api.Snapshot()
  if not run then return{active=false,last=api.last,manualOnly=true}end
  return{active=true,id=run.id,label=run.label,route=run.route,nativeLifeStatus=run.nativeLifeStatus,sleepProbe=run.sleepProbe,position=run.position,onRoute=run.onRoute,atSite=run.atSite,remaining=run.deadline-now(),needsReliefApplied=false}
 end
 return api
end
return M
