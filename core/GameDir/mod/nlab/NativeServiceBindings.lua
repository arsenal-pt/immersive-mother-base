-- Authored service binding policy. No engine calls or geometry extraction.
-- Catalog data is private and measured from the user's owned native assets.
-- Build(context, catalog) returns definitions, status. Definitions are detached copies.
local M={version="0.1.0"}
local services={water=true,mess=true,bunk=true,shower=true,toilet=true,clinic=true}
local idleActs={StandActNormal=true,StandActIdleStill=true}
local function integer(v,lo,hi)
 return type(v)=="number" and v==v and v==math.floor(v) and v>=lo and v<=hi
end
local function finite(v)return type(v)=="number" and v==v and math.abs(v)<math.huge end
local function clone(v)
 if type(v)~="table" then return v end
 local out={};for k,x in pairs(v)do out[k]=clone(x)end;return out
end
local function fail(status,reason)
 status.ready=false;status.reason=reason;return {},status
end
local function validTarget(t)
 if type(t)~="table" then return false,"target missing" end
 if not integer(t.routeHash,1,4294967295)then return false,"route hash invalid"end
 if not integer(t.routePoint,0,65535)then return false,"route point invalid"end
 if not finite(t.x)or not finite(t.y)or not finite(t.z)or not finite(t.yaw)then return false,"coordinates invalid"end
 if t.nodeCount~=1 or t.routePoint~=0 then return false,"route is not a one-node endpoint"end
 if t.nodeEvent~="RelaxedStandIdle"and not(t.nodeEvent=="RelaxedIdleAct"and idleActs[t.idleAct])then
  return false,"endpoint does not have a supported stationary event"
 end
 if t.coordinateSpace~="mission_world"then return false,"endpoint coordinates are not world space"end
 return true
end
local function target(t)
 return {route=t.routeHash,routePoint=t.routePoint,x=t.x,y=t.y,z=t.z,yaw=t.yaw}
end
local function contextAllows(c,cat)
 if c.ready~=true then return false,"native location not ready"end
 if c.missionCode~=cat.missionCode or c.normalSlot~=true then return false,"not normal Mother Base free roam"end
 if c.cluster~=cat.cluster then return false,"different active cluster"end
 if c.layoutCode~=cat.layoutCode then return false,"layout has no measured service catalog"end
 if not integer(c.completedGrade,0,4)then return false,"completed grade unavailable"end
 if c.completedGrade<cat.minimumGrade then return false,"platform not completed"end
 return true
end
function M.Build(context,catalog)
 local c=context or{};local cat=catalog
 local status={schema=1,ready=false,enabledCount=0,candidateCount=0,facilities={},validationMode=c.validationMode==true,unboundServices={}}
 if type(cat)~="table"or cat.schema~=1 or type(cat.facilities)~="table"then return fail(status,"catalog unavailable")end
 if cat.missionCode~=30050 or not integer(cat.layoutCode,0,3)or not integer(cat.cluster,1,7)
  or not integer(cat.platform,0,3)or not integer(cat.minimumGrade,1,4)or cat.minimumGrade~=cat.platform+1 then
  return fail(status,"catalog scope invalid")
 end
 if type(cat.source)~="table"or type(cat.source.sha256)~="string"or #cat.source.sha256~=64 or not cat.source.sha256:match("^%x+$") then
  return fail(status,"catalog provenance unavailable")
 end
 status.unboundServices=clone(cat.unboundServices or {shower="unbound",toilet="unbound",clinic="unbound"})
 local allowed,reason=contextAllows(c,cat);if not allowed then return fail(status,reason)end
 local keys={};for k in pairs(cat.facilities)do keys[#keys+1]=k end;table.sort(keys)
 local defs,occupied={},{}
 for _,service in ipairs(keys)do
  local cfg=cat.facilities[service];local ok=true;local why
  if not services[service]or type(cfg)~="table"or cfg.capacity~=1 or type(cfg.queue)~="table"
   or #cfg.queue<1 or type(cfg.uses)~="table"or #cfg.uses~=1 or not finite(cfg.serviceSeconds)
   or cfg.serviceSeconds<=0 or type(cfg.relief)~="table"then
   ok=false;why="facility policy invalid"
  end
  local claimed={}
  local routeVerified=c.routeHashValidated==true
  local validatedRoutes=c.validatedRoutes or cat.validatedRoutes
  local missingRoute=false;local unverifiedEndpoint=false
  if ok then
   for _,points in ipairs({cfg.queue,cfg.uses})do
    for _,t in ipairs(points)do
     local valid,err=validTarget(t)
     if not valid then ok=false;why=err;break end
     local pointKey=t.routeHash..":"..t.routePoint
     if occupied[pointKey]or claimed[pointKey]then ok=false;why="endpoint reused by another service or slot";break end
     claimed[pointKey]=true
     if c.availableRoutes and c.availableRoutes[t.routeHash]~=true then missingRoute=true end
     if not(validatedRoutes and validatedRoutes[t.routeHash]==true)then unverifiedEndpoint=true end
    end
    if not ok then break end
   end
  end
  local state="invalid"
  local id="command_"..(cat.platform+1).."_"..service
  if ok then
   for pointKey in pairs(claimed)do occupied[pointKey]=true end
   status.candidateCount=status.candidateCount+1
   local enabled=not missingRoute and ((routeVerified and not unverifiedEndpoint)or c.validationMode==true)
   local limit="Prototype service pad: no physical room, fixture interaction, or service-specific animation."
   if missingRoute then state="route_unavailable";why="native route unavailable"
   elseif not enabled and not routeVerified then state="hash_unverified";why="numeric route lookup unsupported until native verification"
   elseif not enabled then state="endpoint_unverified";why="stationary endpoint reachability awaits native verification"
   elseif c.validationMode then state="validation_only";why="controlled native validation only"
   else state="verified";why="verified native standing pad"end
   local out={service=service,label=cfg.label or ("Command platform "..(cat.platform+1).." "..service),
    cluster=cat.cluster,platform=cat.platform,minimumGrade=cat.minimumGrade,layoutCode=cat.layoutCode,
    enabled=enabled,prototypePad=true,fixtureBinding="native stationary route pad",
    limitation=limit,capacity=1,maxQueue=#cfg.queue,serviceSeconds=cfg.serviceSeconds,
    relief=clone(cfg.relief),queue={},uses={},bindingVersion=cat.version or "private-native-v1"}
   for _,t in ipairs(cfg.queue)do out.queue[#out.queue+1]=target(t)end
   for _,t in ipairs(cfg.uses)do out.uses[#out.uses+1]=target(t)end
   defs[id]=out
   if enabled then status.enabledCount=status.enabledCount+1 end
  end
  status.facilities[id]={enabled=ok and defs[id].enabled or false,reason=why,
   bindingState=state,hashVerified=routeVerified,endpointVerified=not unverifiedEndpoint,routeUnavailable=missingRoute}
 end
 status.ready=status.enabledCount>0
 status.reason=status.ready and "local native prototype services available"or "no verified local services"
 status.layoutCode=cat.layoutCode;status.cluster=cat.cluster;status.platform=cat.platform
 status.minimumGrade=cat.minimumGrade
 status.unboundNeeds={hygiene=status.unboundServices.shower,bladder=status.unboundServices.toilet,health=status.unboundServices.clinic}
 return defs,status
end
return M
