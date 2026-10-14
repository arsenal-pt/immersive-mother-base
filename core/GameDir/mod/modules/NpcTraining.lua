-- Owned CQC menu facade. The previous private lab mission/controller is excluded.
local this={}
this.registerMenus={"npcTrainingMenu"}
this.npcTrainingMenu={parentRefs={"ImmersiveMotherBase.immersiveMotherBaseMenu"},options={
 "NpcTraining.StartFour","NpcTraining.StartSix","NpcTraining.Stop","NpcTraining.ShowStatus"}}
this.langStrings={eng={npcTrainingMenu="Soldier training",startFour="CQC practice: four soldiers",startSix="CQC practice: six soldiers",stop="Stop CQC practice",showStatus="Training availability"},help={eng={npcTrainingMenu="Existing regular soldiers only. Resource build pending; this candidate rejects starts."}}}
function this.StartFour()return NpcLife.Command("cqc_four")end
function this.StartSix()return NpcLife.Command("cqc")end
function this.Stop()return NpcLife.Command("cqc_stop")end
function this.ShowStatus()
 local s=NpcLife.GetSnapshot();local t=s and s.cqcTraining or {ready=false,reason="Existing staff not initialized"}
 if InfMenu and InfMenu.Print then InfMenu.Print("CQC available: "..tostring(t.ready).."; route/motion build pending")end
 return t
end
return this
