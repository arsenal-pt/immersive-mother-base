local this={updateRate=0,execState={nextUpdate=0}}
local actors,routes,errors={},{},{}
local nextStatus,cid=0,-1
local staffNames,nextNameRefresh={},0
local function refreshNames(now)
 if now<nextNameRefresh then return end;nextNameRefresh=now+5
 -- Private native name dumps excluded; existing unresolved-name fallback retained.
 staffNames={}
end
local config=assert(loadfile(InfCore.paths.mod.."nlab/StaffConfig.lua"))()
local identity=assert(loadfile(InfCore.paths.mod.."nlab/NpcRegistry.lua"))().StaffIdentity
local function send(id,c)local ok,v=pcall(GameObject.SendCommand,id,c);if not ok and #errors<32 then errors[#errors+1]=c.id..": "..tostring(v)end;return ok,v end
local function active()
 return vars.missionCode==30050 and gvars.usingNormalMissionSlot==true
  and MotherBaseStage.GetCurrentCluster()<7
  and not MotherBaseStage.IsLoading()and not MotherBaseStage.IsActivating()
end
local function fnAssets()return TppEnemy.GetMBEnemyAssetTable or mvars.mbSoldier_funcGetAssetTable end
local function refresh()
 actors={};routes={};cid=MotherBaseStage.GetCurrentCluster()+1
 local fn=fnAssets();if not fn then return end;local assets=fn(cid)
 for p=0,TppLocation.GetMbStageClusterGrade(cid)-1 do
  routes[p]={};local seen={};local a=assets and assets['plnt'..p]
  for _,category in ipairs({'Sneak','Night'})do
   for _,g in ipairs(a and a.soldierRouteList[category]or{})do
    for _,name in ipairs(g.inPlnt or{})do if not seen[name]then seen[name]=true;routes[p][#routes[p]+1]=name end end
   end
  end
 end
end
local function assign(id,a,name,now,urgent,routePoint)
 if not name then return end
 a.route=name;a.routePoint=routePoint or 0;a.assignedAt=now;a.lastMoved=now
 send(id,{id='SetSneakRoute',route=name,point=a.routePoint,isRelaxed=not urgent})
end
local function roam(id,a,now)
 local list=routes[a.platform]or{};if #list==0 then return end
 local n=math.random(1,#list);if list[n]==a.route and #list>1 then n=n%#list+1 end
 a.lifeControlled=false;a.target=nil;a.reason='native patrol';a.nextChange=now+math.random(90,180)
 assign(id,a,list[n],now);a.routeChanges=a.routeChanges+1
end
local function discover(now)
 local fn=fnAssets();local assets=fn and fn(cid)
 for p=0,TppLocation.GetMbStageClusterGrade(cid)-1 do
  for i,name in ipairs(assets and assets['plnt'..p]and assets['plnt'..p].soldierList or{})do
   local id=GameObject.GetGameObjectId('TppSoldier2',name)
   if id~=GameObject.NULL_ID and not actors[id]then
    local status=GameObject.SendCommand(id,{id='GetStatus'})
    local v=GameObject.SendCommand(id,{id='GetPosition'})
    if status~=TppGameObject.NPC_STATE_DISABLE and math.abs(v:GetX())+math.abs(v:GetY())+math.abs(v:GetZ())>.1 then
     actors[id]={name=name,index=(cid-1)*100+p*20+i,platform=p,cluster=cid,active=true,existing=true,x=v:GetX(),y=v:GetY(),z=v:GetZ(),minY=v:GetY(),maxY=v:GetY(),travelled=0,lastMoved=now,assignedAt=now,nextChange=now+60,routeChanges=0,reason='native staff enrolled',route='native initial duty'}
    end
   end
  end
 end
end
function this.OnAllocateTop()actors={};routes={};errors={};cid=-1;nextStatus=0;nextNameRefresh=0 end
function this.SetCount(n)assert(n==0,'Native profile uses existing staff; extra lab soldiers are disabled')end
function this.GetRoster()
 local out={};if not active()then return out end
 for id,a in pairs(actors)do
  if a.cluster==MotherBaseStage.GetCurrentCluster()+1 and GameObject.SendCommand(id,{id='GetStatus'})~=TppGameObject.NPC_STATE_DISABLE and GameObject.SendCommand(id,{id='GetLifeStatus'})~=TppGameObject.NPC_LIFE_STATE_DEAD then
   local staff=GameObject.SendCommand(id,{id='GetStaffId'})
   local staffKey=identity(staff,a.name);local codeName=staffNames[staffKey]
   local ok,ability=pcall(TppMotherBaseManagement.GetMbsStaffCombatRank,{staffId=staff});if not ok then ability=nil end
   out[#out+1]={id=id,name=staffKey,codeName=codeName,nameSource=codeName and 'native codename + owned English language data' or 'unresolved native name',locator=a.name,label=codeName or 'DD soldier',role='soldier',kind='soldier',index=a.index,nativeStaffId=staff,skillRating=ability,cluster=a.cluster,platform=a.platform,pilotEligible=a.cluster==1 and a.platform==0,native=true}
  end
 end
 table.sort(out,function(a,b)return a.locator<b.locator end);return out
end
function this.GetObservations()
 local out={};if not active()then return out end
 for id,a in pairs(actors)do
  local v=GameObject.SendCommand(id,{id='GetPosition'});local life=GameObject.SendCommand(id,{id='GetLifeStatus'})
  out[id]={x=v:GetX(),y=v:GetY(),z=v:GetZ(),real=GameObject.SendCommand(id,{id='GetStatus'})~=TppGameObject.NPC_STATE_DISABLE,presenceSource='enabled native staff; streamed normally',alive=life~=TppGameObject.NPC_LIFE_STATE_DEAD,available=life==TppGameObject.NPC_LIFE_STATE_NORMAL,nativeLifeStatus=life,equip=GameObject.SendCommand(id,{id='GetCurrentEquipId'})}
 end;return out
end
function this.ApplyLifeAction(action,now)
 if not active()then return end
 local a=actors[action.actor];if not a or GameObject.SendCommand(action.actor,{id='GetStatus'})==TppGameObject.NPC_STATE_DISABLE or GameObject.SendCommand(action.actor,{id='GetLifeStatus'})~=TppGameObject.NPC_LIFE_STATE_NORMAL then return end
 if action.kind=='roam'then roam(action.actor,a,now)
 elseif action.kind=='move'then
  if not(action.target and action.target.route)then return end
  a.lifeControlled=true;a.target=action.target;a.reason='ordered destination';a.detourUntil=nil
  assign(action.actor,a,action.target.route,now,action.target.urgency=='muster',action.target.routePoint)
 elseif action.kind=='hold'then a.lifeControlled=true;a.target=nil;a.reason='native standing wait'
 elseif action.kind=='nativeDuty'then a.lifeControlled=true;a.target=nil;a.reason='duty: '..tostring(action.target and action.target.duty or 'patrol');a.dutyUntil=now+120;roam(action.actor,a,now);a.reason='duty patrol';a.lifeControlled=true
 end
end
function this.GetNativeInfo()return actors end
function this.Update(checks,now)
 if not active()or not checks.inGame or not checks.missionCanStart then return end
 if cid~=MotherBaseStage.GetCurrentCluster()+1 then refresh()end
 if now<nextStatus then return end;nextStatus=now+.5;refreshNames(now);discover(now)
 local rows={}
 for id,a in pairs(actors)do
  local v=GameObject.SendCommand(id,{id='GetPosition'});local x,y,z=v:GetX(),v:GetY(),v:GetZ()
  local d=math.sqrt((x-a.x)^2+(y-a.y)^2+(z-a.z)^2);a.travelled=a.travelled+d;if d>.03 then a.lastMoved=now end
  a.x=x;a.y=y;a.z=z;a.minY=math.min(a.minY,y);a.maxY=math.max(a.maxY,y)
  local status=GameObject.SendCommand(id,{id='GetStatus'});local life=GameObject.SendCommand(id,{id='GetLifeStatus'})
   a.nativeStatus=status;a.nativeLifeStatus=life;a.active=status~=TppGameObject.NPC_STATE_DISABLE
   local available=a.active and life==TppGameObject.NPC_LIFE_STATE_NORMAL
  -- End a navigation detour by its deadline, even when the soldier is moving.
  if not a.activityOwner and available and a.target and a.detourUntil and now>=a.detourUntil then
   assign(id,a,a.target.route,now,a.target.urgency=='muster',a.target.routePoint);a.detourUntil=nil;a.reason='ordered destination after navigation retry'
  elseif not a.activityOwner and available and a.target and not a.detourUntil and now-a.lastMoved>30 and now-a.assignedAt>30 then
   local target=a.target;roam(id,a,now);a.target=target;a.lifeControlled=true;a.detourUntil=now+15;a.reason='native navigation retry'
  elseif not a.activityOwner and available and not a.lifeControlled and now>=a.nextChange then roam(id,a,now)end
   rows[#rows+1]=string.format('{"id":%d,"name":"%s","active":%s,"native":true,"cluster":%d,"platform":%d,"route":"%s","travelled":%.3f,"x":%.3f,"y":%.3f,"z":%.3f,"minY":%.3f,"maxY":%.3f,"reason":"%s","nativeStatus":%d,"nativeLifeStatus":%d,"available":%s,"assignedAt":%.3f,"lastMoved":%.3f,"routeChanges":%d}',id,a.name,tostring(a.active),a.cluster,a.platform,a.route,a.travelled,x,y,z,a.minY,a.maxY,a.reason,status,life,tostring(available),a.assignedAt,a.lastMoved,a.routeChanges)
 end
 local ee={};for _,e in ipairs(errors)do ee[#ee+1]='"'..e:gsub('"',"'")..'"'end
 local f=io.open(InfCore.paths.mod..'nlab_soldier_status.json','w');if f then f:write('{"version":"0.1.19","count":0,"nativeMode":true,"cluster":'..cid..',"time":'..now..',"actors":['..table.concat(rows,',')..'],"errors":['..table.concat(ee,',')..']}');f:close()end
end
return this
