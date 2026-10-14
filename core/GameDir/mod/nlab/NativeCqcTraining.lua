-- Ambient native CQC rehearsal. No player/camera/pad calls, attacks, spawns or forced realization.
local M={version="0.2.3"}
function M.Create(core,world,layout,soldiers,proof)
 local root=InfCore.paths.mod.."nlab/"
 local policy=assert(loadfile(root.."CqcRosterPolicy.lua"))()
 local pairs=assert(loadfile(root.."CqcPairPlan.lua"))()
 local formation=assert(loadfile(root.."CqcTrainingPlan.lua"))()
 local drill=assert(loadfile(root.."CqcDrillSession.lua"))()
 local observer=assert(loadfile(root.."NativeMotionObserver.lua"))()
 local paired=proof.pairedPlaybackVerified==true
 local mode=paired and "paired"or "technique"
 local scheduleReady=proof.candidateResourcesAvailable==true and (paired and proof.fixedStationSessionVerified==true or not paired and proof.sessionVerified==true)and proof.rumbleVerifiedAbsent==true
 local api={scheduleReady=scheduleReady,automatic=proof.automatic==true and scheduleReady,ready=proof.candidateResourcesAvailable==true and (paired or proof.techniquePlaybackVerified==true)and proof.reversibleOwnershipVerified==true,
  contactThrowsReady=proof.candidateResourcesAvailable==true and paired,nextAutomatic=Time.GetRawElapsedTimeSinceStartUp()+1200,history={},serial=0}
 local run,last;local ending=false
 local function raw()return Time.GetRawElapsedTimeSinceStartUp()end
 local function safe()
  return vars.missionCode==30050 and gvars.usingNormalMissionSlot==true and MotherBaseStage.GetCurrentCluster()==0
   and MotherBaseStage.GetCurrentLayout()==3 and not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()
 end
 local function position(id)local v=GameObject.SendCommand(id,{id="GetPosition"});return{x=v:GetX(),y=v:GetY(),z=v:GetZ()}end
 local function same(a)
  return safe()and soldiers.GetNativeInfo()[a.id]==a.info and GameObject.SendCommand(a.id,{id="GetStaffId"})==a.staff
 end
 local function request(a,command)
  assert(same(a),"native identity changed");return GameObject.SendCommand(a.id,command)
 end
 local function setPhase(r,phase)
  for _,a in ipairs(r.actors)do core.SetActivityPhase(world,a.id,r.epoch,phase)end
 end
 function api.Stop(reason)
  if not run or ending then return false end;ending=true;local r=run
  r.session.Stop(reason or"manual cancellation")
  if r.listener then local ok=r.listener.Detach();if not ok then r.session.cleanupErrors[#r.session.cleanupErrors+1]={error="message registry changed"}end end
  run=nil
  last={state=r.session.state,reason=r.session.reason,participants={},completedRounds=r.session.completedRounds,
   completedCycles=r.session.completedCycles,trainingStarted=r.session.trainingStarted,trainingEnded=r.session.trainingEnded,
   ended=raw(),cleanupComplete=#r.session.cleanupErrors==0,cleanupErrors=r.session.cleanupErrors,mode=mode,assemblyMoves=r.assemblyMoves,fixedPartners=true,
   validationOnly=r.validation,contactThrows=paired,nativeAttacks=false}
  for _,a in ipairs(r.actors)do last.participants[#last.participants+1]={id=a.id,identity=a.identity,label=a.label}end
  if not last.cleanupComplete then last.state="INTERRUPTED"end
  api.history[#api.history+1]={state=last.state,reason=last.reason,ended=last.ended,cleanupComplete=last.cleanupComplete}
  if #api.history>12 then table.remove(api.history,1)end
  api.nextAutomatic=raw()+1200;ending=false;return last.cleanupComplete
 end
 function api.CancelForAction(action)
  if not run or ending then return end
  for _,a in ipairs(run.actors)do if action.actor==a.id then api.Stop("priority routine: "..tostring(action.kind));return end end
 end
 function api.Start(roster,observations,limit,validation,manual)
  assert(proof.candidateResourcesAvailable==true,"CQC route/motion build pending; historical proof is not candidate proof")
  assert(not world.assemblyReservation,"Another activity reserves the assembly pad")
  local prepare=manual==true and validation~=true
  assert(not run,"training session already active")
  assert(safe()and(not world.group or(prepare and world.group.kind=="GATHERING")),"training requires normal Command; finish muster or the active assembly first")
  assert(api.ready or validation==true,"training still requires native verification")
  local site={cluster=1,platform=0,x=14.5,y=0,z=-21}
  local selected,reason=policy.Select(roster,world.actors,observations,site,limit or 6,world.config.deferUnboundNeeds,prepare)
  assert(selected,reason);api.serial=api.serial+1
  local epoch="cqc_"..tostring(math.floor(raw()*1000)).."_"..api.serial
  local r={actors=selected,byId={},epoch=epoch,events=0,validation=validation==true,pairs={}}
  for _,a in ipairs(selected)do
   a.staff=world.actors[a.id].nativeStaffId;a.info=soldiers.GetNativeInfo()[a.id]
   assert(a.info and not a.info.activityOwner,"native actor already reserved");r.byId[a.id]=a
  end
  local port={}
  port.ContextSafe=function()return safe()and not world.group and not(r.listener and r.listener.handlerErrors>0)end
  port.Observe=function(id,identity,phase)
   local a=r.byId[id];local actor=world.actors[id]
   if not a or not actor or actor.name~=identity or not same(a)then return nil end
   local p=position(id);local life=GameObject.SendCommand(id,{id="GetLifeStatus"})
   local status=GameObject.SendCommand(id,{id="GetStatus"})
   local supported=math.abs(p.y-site.y)<.4 and(p.x-site.x)^2+(p.z-site.z)^2<1600
   -- Capture may begin upstairs; alignment still requires the surveyed ground deck.
   if phase=="capture"and not a.info.activityOwner then supported=true end
   if a.info.activityOwner and actor.activityOwner~=epoch then return nil end
   local target=a.target
   local aligned=paired and a.prepared==true or not paired and target and(p.x-target.x)^2+(p.z-target.z)^2<.25 and math.abs(p.y-target.y)<.25
   local allowed=status~=TppGameObject.NPC_STATE_DISABLE and life==TppGameObject.NPC_LIFE_STATE_NORMAL
   return{identity=identity,available=allowed,supported=supported or(phase=="align"and not a.played),
    aligned=aligned==true,recovered=a.ended==true and supported}
  end
  port.Capture=function(id,identity)
   local a=r.byId[id];assert(same(a),"stale native actor")
   assert(GameObject.SendCommand(id,{id="GetStateFlag"})==0,"non-default native flags")
   return{controlled=a.info.lifeControlled,target=a.info.target,detour=a.info.detourUntil,
    route=a.info.route,point=a.info.routePoint,identity=identity,equip=GameObject.SendCommand(id,{id="GetCurrentEquipId"})}
  end
  port.Acquire=function(id,identity,saved)
   local a=r.byId[id];assert(same(a),"identity changed before acquisition")
   core.BeginActivity(world,id,identity,epoch,world.realNow)
   a.info.activityOwner=epoch;a.info.lifeControlled=true;a.info.target=nil;a.info.detourUntil=nil
    -- Vanilla Mother Base soldiers salute the player until explicitly released.
    -- Suppress that response only for this lease; restore it on every exit.
    a.saluteTouched=true;request(a,{id="SetSaluteDisable",enabled=true})
     a.moraleTouched=true;request(a,{id="SetSaluteMoraleDisable",enabled=true})
     a.cqcSaluteTouched=true;request(a,{id="SetSaluteToCqc",enabled=false})
     a.chatTouched=true;request(a,{id="SetDisableOccasionalChat",disable=true})
    if paired and type(saved.equip)=="number"and saved.equip>0 then a.unarmedTouched=true;request(a,{id="SetUnarmed",enabled=true})end
    return true
  end
  port.Arrange=function(round,leases,places,mode)
   assert(mode=="parallel","circle layout is not yet surveyed")
   local firstAssembly=not r.stations;r.stations=r.stations or{}
   setPhase(r,firstAssembly and "assembling"or "practising");r.pairs={}
   for slot,pair in ipairs(round)do
    local siteConfig=assert(layout.gather.sites[slot])
    local origin=assert(siteConfig.formations["2"][1])
    local first=pair.reverse and pair.receiver or pair.initiator
    local second=pair.reverse and pair.initiator or pair.receiver
    local station=r.stations[slot]
    if not station then
     station={first=first,second=second,anchor=origin};r.stations[slot]=station
    end
    assert(station.first==first and station.second==second,"training partners or station changed")
    local active={initiator=pair.initiator,receiver=pair.receiver,anchor=station.anchor,
     heading=origin.yaw*math.pi/180+(pair.reverse and math.pi or 0),slot=slot,reverse=pair.reverse}
    r.pairs[slot]=active
    for index,id in ipairs({station.first,station.second})do
     local a=r.byId[id];a.target=assert(siteConfig.formations["2"][index])
     a.ended=false;a.played=false;a.prepared=not firstAssembly;a.motionStage=nil;a.pair=active
     a.alignCommand=InfCore.StrCode32(epoch..":align:"..r.session.roundSerial..":"..a.id)
     if firstAssembly then
      request(a,{id="SpecialAction",action="PlayMotion",isDisable=true})
      soldiers.ApplyLifeAction({actor=a.id,kind="move",target=a.target},world.realNow)
      r.assemblyMoves=(r.assemblyMoves or 0)+1
     end
    end
    active.preparing=not firstAssembly
   end
   return true
  end
  port.CommandId=function(epoch,round,id)return InfCore.StrCode32(epoch..":"..round..":"..id)end
  port.Play=function(id,identity,role,partner,command)
   local a=r.byId[id];a.command=command;a.ended=false;a.played=true;a.motionOwned=true;a.info.target=nil
    a.motionStage=role=="receiver"and paired and "receive"or "throw"
    a.recoveryCommand=InfCore.StrCode32(epoch..":recover:"..r.session.roundSerial..":"..a.id)
     a.settleCommand=InfCore.StrCode32(epoch..":settle:"..r.session.roundSerial..":"..a.id)
   setPhase(r,"practising")
   -- Paired body playback has no damage, native attacks, player camera or pad commands.
   request(a,{id="SpecialAction",action="PlayMotion",path=paired and role=="receiver"and proof.receiverPath or proof.techniquePath,
     startPos=paired and Vector3(a.pair.anchor.x,a.pair.anchor.y,a.pair.anchor.z)or nil,
     startRot=paired and a.pair.heading or nil,autoFinish=not paired,override=true,enableMessage=true,enableFinishInterrupted=false,
    enableGravity=false,enableCollision=false,interpFrame=0,startFrame=0,commandId=command})
   return true
  end
  port.Release=function(id,identity,saved,reason)
   local a=r.byId[id];local identityOk,current=pcall(same,a);local errors={}
   local function attempt(fn)local ok,e=pcall(fn);if not ok then errors[#errors+1]=tostring(e)end end
   if a.info.activityOwner==epoch then
    a.info.activityOwner=nil;a.info.lifeControlled=saved.controlled;a.info.target=saved.target;a.info.detourUntil=saved.detour
   end
   if identityOk and current then
    if a.motionOwned or a.played then attempt(function()request(a,{id="SpecialAction",action="PlayMotion",isDisable=true})end)end
     if a.unarmedTouched then attempt(function()request(a,{id="SetUnarmed",enabled=false})end)end
     if a.saluteTouched then attempt(function()request(a,{id="SetSaluteDisable",enabled=false})end)end
      if a.moraleTouched then attempt(function()request(a,{id="SetSaluteMoraleDisable",enabled=false})end)end
      if a.cqcSaluteTouched then attempt(function()request(a,{id="SetSaluteToCqc",enabled=true})end)end
      if a.chatTouched then attempt(function()request(a,{id="SetDisableOccasionalChat",disable=false})end)end
    local orders=core.EndActivity(world,id,identity,epoch,reason,world.realNow)
    -- EndActivity emits nothing when a newer priority order has already taken ownership.
    if #orders==0 then
     local actor=world.actors[id]
     if actor and actor.name==identity and actor.activityOwner==nil then
      if actor.target then orders={{actor=id,kind="move",target=actor.target}}
      elseif actor.state=="ROAMING"then orders={{actor=id,kind="roam"}}
      elseif actor.duty=="patrol"then orders={{actor=id,kind="nativeDuty",target={duty="patrol"}}}end
     end
    end
    for _,order in ipairs(orders)do attempt(function()soldiers.ApplyLifeAction(order,world.realNow)end)end
   else
    -- Do not command a recycled or unloaded physical slot. Clear only the captured logical lease.
    attempt(function()core.EndActivity(world,id,identity,epoch,"native actor departed",world.realNow)end)
   end
   if #errors>0 then error(table.concat(errors,"; "))end
   return true
  end
  if prepare then
   -- Read-only native checks for every participant precede all logical/engine mutations.
   for _,a in ipairs(selected)do
    assert(same(a),"native identity changed before preparation")
    assert(GameObject.SendCommand(a.id,{id="GetStateFlag"})==0,"non-default native flags")
    assert(GameObject.SendCommand(a.id,{id="GetLifeStatus"})==TppGameObject.NPC_LIFE_STATE_NORMAL and
     GameObject.SendCommand(a.id,{id="GetStatus"})~=TppGameObject.NPC_STATE_DISABLE,"native actor unavailable before preparation")
   end
   local orders=core.PrepareActivity(world,selected,world.realNow)
   for _,order in ipairs(orders)do soldiers.ApplyLifeAction(order,world.realNow)end
  end
  if validation==true then
   local saved,touched,failures={},{},{}
   local ok,e=pcall(function()
    for _,a in ipairs(selected)do saved[a.id]=port.Capture(a.id,a.identity)end
    for _,a in ipairs(selected)do touched[a.id]=true;assert(port.Acquire(a.id,a.identity,saved[a.id]))end
   end)
   if not ok then failures[#failures+1]=tostring(e)end
   for _,a in ipairs(selected)do if touched[a.id]then
    local released,err=pcall(port.Release,a.id,a.identity,saved[a.id],"ownership validation")
    if not released then failures[#failures+1]=tostring(err)end
   end end
   api.lastOwnershipTest={passed=#failures==0,participants=#selected,errors=failures,time=raw(),
    forcedRealizationUsed=false,playerCommandsUsed=false}
   assert(api.lastOwnershipTest.passed,"ownership validation failed")
   return api.lastOwnershipTest
  end
  local planner={Build=function(actors,mode)return formation.Build(pairs,actors,mode)end}
  r.session=drill.New(planner,selected,port,{drillId=epoch,motionMode=mode,pairedPlaybackVerified=paired,
   techniquePlaybackVerified=proof.techniquePlaybackVerified==true,reversibleOwnershipVerified=proof.reversibleOwnershipVerified==true,
   clockKind="monotonic-real-seconds",layoutMode="parallel",alignSeconds=180,playSeconds=12,restSeconds=5,
   trainingSeconds=300,totalSeconds=1200})
  run=r
  local subscriptions={}
  for _,actor in ipairs(selected)do local a=actor
   subscriptions[#subscriptions+1]={class=InfCore.StrCode32("GameObject"),message=InfCore.StrCode32("SpecialActionEnd"),sender=a.id,
    handler=function(id,action,command)
     if run~=r or id~=a.id then return end
     if command==a.alignCommand and a.motionStage=="prepare"then a.prepared=true;r.events=r.events+1
     elseif command==a.command and a.motionStage=="receive"then
      a.motionStage="recovery_pending";a.recoveryAfter=raw()+.15;r.events=r.events+1
     elseif paired and command==a.command and a.motionStage=="throw"then
      a.motionStage="settle_pending";a.settleAfter=raw()+.1;r.events=r.events+1
     elseif(command==a.settleCommand and a.motionStage=="settle")or(command==a.recoveryCommand and a.motionStage=="recovery")or(not paired and command==a.command and a.motionStage=="throw")then
      a.ended=true;a.motionStage="complete";r.events=r.events+1;r.session.OnEnd(id,a.command)
     end
    end}
  end
  for _,a in ipairs(selected)do
    for _,message in ipairs({"Damage","Unconscious"})do
     local actor=a
     subscriptions[#subscriptions+1]={class=InfCore.StrCode32("GameObject"),message=InfCore.StrCode32(message),sender=a.id,
      handler=function(id)if run==r and id==actor.id then r.cancelReason="participant injured or interrupted"end end}
    end
   end
   local ok,e=pcall(function()r.listener=observer.Attach(assert(InfMain.messageExecTable),subscriptions);assert(r.session.Start(raw()))end)
  if not ok then api.Stop("start failed");error(e)end
  return true
 end
 function api.Update(roster,observations)
  if run then
   local r=run;local now=raw()
    if r.cancelReason then api.Stop(r.cancelReason);return end
    -- All engine mutations are deferred to this update, never issued from message callbacks.
    local ok,e=pcall(function()
     for _,a in ipairs(r.actors)do
      local actor=world.actors[a.id]
      assert(actor and same(a),"participant identity changed")
      assert(not policy.UrgentNeed(actor,world.config.deferUnboundNeeds),"urgent personal need")
      if a.motionStage=="recovery_pending"and now>=a.recoveryAfter then
       a.motionStage="recovery";a.motionOwned=true
       request(a,{id="SpecialAction",action="PlayMotion",path=proof.recoveryPath,autoFinish=false,override=true,
        enableMessage=true,enableFinishInterrupted=false,enableGravity=false,enableCollision=false,interpFrame=0,startFrame=0,
        commandId=a.recoveryCommand})
      elseif a.motionStage=="settle_pending"and now>=a.settleAfter then
       -- Leave the throw's final body pose through a standing tail, rather than
       -- resuming native patrol/salute AI between alternating turns.
       a.motionStage="settle";a.motionOwned=true
       request(a,{id="SpecialAction",action="PlayMotion",path=proof.recoveryPath,autoFinish=false,override=true,
        enableMessage=true,enableFinishInterrupted=false,enableGravity=false,enableCollision=false,interpFrame=8,startFrame=179,
        commandId=a.settleCommand})
      end
     end
     if paired and r.session.state=="ALIGNING"then
      for _,pair in ipairs(r.pairs)do
       local first,second=r.byId[pair.initiator],r.byId[pair.receiver]
       local function arrived(a)
        local p=position(a.id);local t=a.target
        return t and(p.x-t.x)^2+(p.z-t.z)^2<.25 and math.abs(p.y-t.y)<.25
       end
       if not pair.preparing and arrived(first)and arrived(second)then
        pair.preparing=true
        for _,a in ipairs({first,second})do
         a.motionOwned=true;a.motionStage="prepare";a.info.target=nil
         request(a,{id="SpecialAction",action="PlayMotion",path=proof.recoveryPath,autoFinish=false,override=true,
          enableMessage=true,enableFinishInterrupted=false,enableGravity=false,enableCollision=false,interpFrame=0,startFrame=179,
          startPos=Vector3(pair.anchor.x,pair.anchor.y,pair.anchor.z),startRot=pair.heading,commandId=a.alignCommand})
        end
       end
      end
     end
    end)
    if not ok then api.Stop("training update failed: "..tostring(e));return end
    r.session.Tick(now)
   if r.session.state=="FINISHED"or r.session.state=="INTERRUPTED"then api.Stop(r.session.reason)
   elseif r.session.state=="RESTING"then setPhase(r,"training_rest")end
  elseif api.automatic and api.ready and world.config.autonomousDuties and not world.group and not world.assemblyReservation and raw()>=api.nextAutomatic then
   api.nextAutomatic=raw()+60
   local ok,e=pcall(api.Start,roster,observations,6,false)
   if not ok then api.lastAutomaticReason=tostring(e)end
  end
 end
 function api.ToggleAutomatic()assert(api.scheduleReady,"scheduled training requires session and rumble verification");api.automatic=not api.automatic;api.nextAutomatic=raw()+1200;return api.automatic end
 function api.Snapshot()
  local s={version=M.version,ready=api.ready,scheduleReady=api.scheduleReady,rumbleVerifiedAbsent=proof.rumbleVerifiedAbsent==true,automatic=api.automatic,contactThrowsReady=proof.candidateResourcesAvailable==true and paired,mode=mode,
   label=paired and "Paired CQC practice (animation only)"or "CQC technique practice (no contact throws)",minimumSeconds=300,clock="real seconds",fixedPartners=true,fixedStations=true,manualPreparesRoutine=true,lastOwnershipTest=api.lastOwnershipTest,nextAutomatic=api.nextAutomatic,
   scope="Current streamed Command platform soldiers; new eligible staff join the next cohort",last=last,history=api.history}
  if run then local r=run;local d=r.session
   s.active={state=d.state,participants={},round=d.round,completedRounds=d.completedRounds,completedCycles=d.completedCycles,
    trainingStarted=d.trainingStarted,deadline=d.trainingDeadline,remaining=d.trainingDeadline and math.max(0,d.trainingDeadline-raw())or nil,
    phaseDeadline=d.phaseDeadline,assemblyMoves=r.assemblyMoves,stations={},events=r.events,validationOnly=r.validation,epoch=r.epoch}
   for slot,station in ipairs(r.stations or{})do s.active.stations[#s.active.stations+1]={slot=slot,first=station.first,second=station.second,anchor=station.anchor}end
   for _,a in ipairs(r.actors)do s.active.participants[#s.active.participants+1]={id=a.id,identity=a.identity,label=a.label,motionStage=a.motionStage,role=a.pair and(a.pair.initiator==a.id and "initiator"or "receiver")or nil}end
  end
  return s
 end
 return api
end
return M
