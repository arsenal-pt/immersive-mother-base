-- Authored route-only IH pack callback REVIEW TEMPLATE; disabled by default.
-- No private Soldier2/Hostage2 allocation, model/motion pack, or FPKD dependency.
local this={VERSION="0.1.0-review",enabled=false}
function this.AddMissionPacks(missionCode,packPaths)
 if not this.enabled or missionCode~=30050 then return end
 packPaths[#packPaths+1]="/Assets/tpp/pack/mission2/imb/imb_life_routes.fpk"
end
function this.GetStatus()
 return {enabled=this.enabled,sourceOnly=true,nativeVerified=false,
  scope="250 authored target routes only; no template/inherited routes",
  reason="Root resource/package/notice/native review required before enablement"}
end
return this
