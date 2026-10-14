-- Read-only native Mother Base map observer. No game/save/player commands.
local this={updateRate=0,execState={nextUpdate=0}}
local nextSample=0
local function query(fn)
 local ok,value=pcall(fn)
 if ok then return value end
 return nil,tostring(value)
end
local function finite(v)return type(v)=="number"and v==v and math.abs(v)<1e9 end
local function json(v)
 local t=type(v)
 if t=="nil"then return "null"end
 if t=="number"then return finite(v)and tostring(v)or "null"end
 if t=="boolean"then return tostring(v)end
 if t=="string"then return '"'..v:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r'):gsub('\t','\\t')..'"'end
 if t~="table"then return json(tostring(v))end
 local count,max,array=0,0,true
 for k in pairs(v)do count=count+1;if type(k)~="number"or k<1 or k%1~=0 then array=false else max=math.max(max,k)end end
 array=array and count==max
 local rows={}
 if array then for i=1,count do rows[#rows+1]=json(v[i])end
 else for k,val in pairs(v)do rows[#rows+1]=json(tostring(k))..":"..json(val)end end
 return(array and "["or "{")..table.concat(rows,",")..(array and "]"or "}")
end
function this.Capture(now)
 local s={schema=1,version="0.1.18",missionCode=vars.missionCode,realTime=now,
  source="native MotherBaseStage + TppLocation completed grades",clusters={},errors={},
  yawUnit="degrees",playerYawUnit="degrees",cameraYawUnit="degrees",coordinateSystem="Fox world X/Z; metres"}
 s.capturedUnix=query(function()return os.time()end)
 s.inMotherBase=vars.missionCode==30050
 if not s.inMotherBase then return s end
 local function stageQuery(key,fn,valid)
  local value,err=query(fn)
  if err or not valid(value)then
   s.errors[#s.errors+1]=err or("invalid native stage "..key)
  else s[key]=value end
 end
 stageQuery("layoutCode",function()return MotherBaseStage.GetCurrentLayout()end,function(v)return finite(v)and v>=0 and v%1==0 end)
 stageQuery("cluster0",function()return MotherBaseStage.GetCurrentCluster()end,function(v)return finite(v)and v>=0 and v<=7 and v%1==0 end)
 stageQuery("loading",function()return MotherBaseStage.IsLoading()end,function(v)return type(v)=="boolean"end)
 stageQuery("activating",function()return MotherBaseStage.IsActivating()end,function(v)return type(v)=="boolean"end)
 s.player={x=vars.playerPosX,y=vars.playerPosY,z=vars.playerPosZ,yaw=vars.playerRotY}
 for i=1,7 do
  local grade,err=query(function()return TppLocation.GetMbStageClusterGrade(i)end)
  local c={cluster0=i-1,category=TppDefine.CLUSTER_NAME[i],grade=grade,platforms={}}
  if not finite(grade)or grade<0 or grade>4 or grade%1~=0 then
   s.errors[#s.errors+1]=err or("invalid completed grade for cluster "..(i-1));c.grade=nil
  else
   for p=0,grade-1 do
    local pos,e=query(function()
     local v=MotherBaseStage.GetDemoCenter(i-1,p)
     local x,y,z=v:GetX(),v:GetY(),v:GetZ()
     assert(finite(x)and finite(y)and finite(z),"invalid native platform centre")
     return {plant0=p,x=x,y=y,z=z}
    end)
    if pos then c.platforms[#c.platforms+1]=pos
    else s.errors[#s.errors+1]=e end
   end
  end
  s.clusters[#s.clusters+1]=c
 end
 s.complete=#s.errors==0 and finite(s.layoutCode)and not s.loading and not s.activating
 return s
end
function this.Update(checks,now)
 if now<nextSample then return end
 nextSample=now+2
 local ok,s=pcall(this.Capture,now)
 if not ok then s={schema=1,inMotherBase=false,realTime=now,errors={tostring(s)}}end
 local f=io.open(InfCore.paths.mod.."nlab_base_map.json","w")
 if f then f:write(json(s));f:close()end
end
function this.OnAllocateTop()nextSample=0 end
return this
