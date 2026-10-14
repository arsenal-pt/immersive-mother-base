-- One owned Infinite Heaven root. Framework and original IH menus remain external.
local this={VERSION="0.1.0-alpha.1",owner="arsenal-pt",license="GPL-3.0-only"}
this.registerMenus={"immersiveMotherBaseMenu","imbStaffMenu","imbTestingMenu"}
this.immersiveMotherBaseMenu={parentRefs={"InfMenuDefs.inMissionMenu"},options={"ImmersiveMotherBase.ShowAvailability"}}
this.imbStaffMenu={parentRefs={"ImmersiveMotherBase.immersiveMotherBaseMenu"},options={"ImmersiveMotherBase.ShowStaff","ImmersiveMotherBase.ShowHierarchy"}}
this.imbTestingMenu={parentRefs={"ImmersiveMotherBase.immersiveMotherBaseMenu"},options={"ImmersiveMotherBase.ShowAvailability","ImmersiveMotherBase.ShowMap"}}
this.langStrings={eng={immersiveMotherBaseMenu="Immersive Mother Base",imbStaffMenu="Staff and hierarchy",imbTestingMenu="Testing and diagnostics",showAvailability="Candidate feature availability",showStaff="Observed regular soldiers",showHierarchy="Simulated military hierarchy",showMap="Read-only native platform snapshot"},help={eng={immersiveMotherBaseMenu="Installable alpha foundation; GPL-3.0-only; service/group/CQC resources and native acceptance pending.",imbTestingMenu="On-demand diagnostics; companion HTTP service is optional."}}}
local function feedback(s)
 this.lastStatus=s
 if InfMenu and type(InfMenu.Print)=="function"then InfMenu.Print(s)end
 return s
end
function this.ShowAvailability()
 return feedback("Native staff/needs/rank rules/patrol retained. Route assemblies/CQC and measured services need resource build review. Recorder012: inert capture evidence only.")
end
function this.ShowStaff()
 local roster=NpcSoldiers and NpcSoldiers.GetRoster and NpcSoldiers.GetRoster()or{}
 feedback("Observed regular soldiers: "..#roster.."; native name catalog excluded");return roster
end
function this.ShowHierarchy()
 local s=NpcLife and NpcLife.GetSnapshot and NpcLife.GetSnapshot()
 feedback(s and"Simulated ranks; vacancies never promote staff"or"No active staff snapshot");return s and s.hierarchy
end
function this.ShowMap()
 if not NpcBaseMap or not NpcBaseMap.Capture then return nil,"Map observer unavailable"end
 return NpcBaseMap.Capture(Time.GetRawElapsedTimeSinceStartUp())
end
return this
