local Registry={}
function Registry.StaffIdentity(id,locator)
 if type(id)=="number"and id>0 and id<9007199254740992 then return "mb_staff_"..string.format("%.0f",id)end
 return locator
end
function Registry.Create()return {providers={},owners={},indices={},nextIndex=1}end
function Registry.AddProvider(r,key,adapter)
 assert(type(key)=="string"and type(adapter)=="table"and adapter.GetRoster and adapter.GetObservations and adapter.ApplyLifeAction,"provider requires roster, observations and actions")
 r.providers[key]=adapter
end
function Registry.Collect(r)
 local roster,observations,owners,seen={},{},{},{}
 local names={}
 local keys={};for key in pairs(r.providers)do keys[#keys+1]=key end;table.sort(keys)
 for _,key in ipairs(keys)do
  local adapter=r.providers[key]
  for _,spec in ipairs(adapter.GetRoster())do
   assert(type(spec.id)=="number"and type(spec.name)=="string","invalid person identity")
   if not seen[spec.id]and not names[spec.name]then
    seen[spec.id]=true;names[spec.name]=true
    if not r.indices[spec.name]then r.indices[spec.name]=r.nextIndex;r.nextIndex=r.nextIndex+1 end
    local s={};for k,v in pairs(spec)do s[k]=v end
    s.index=r.indices[s.name];s.label=s.codeName or (s.role=="soldier"and "DD soldier"or s.role).." "..string.format("%02d",s.index)
    s.provider=key;roster[#roster+1]=s;owners[s.id]=adapter
   end
  end
  for id,o in pairs(adapter.GetObservations())do if owners[id]==adapter then observations[id]=o end end
 end
 table.sort(roster,function(a,b)return a.index<b.index end);r.owners=owners
 return roster,observations
end
function Registry.Apply(r,action,now)
 local owner=r.owners[action.actor];if owner then owner.ApplyLifeAction(action,now)end
end
return Registry
