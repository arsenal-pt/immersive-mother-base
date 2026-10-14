# In-game core — pre-alpha

Original implementation developed entirely using AI/LLMs via Codex under arsenal-pt's direction/testing. Eligible original code: GPL-3.0-only; see ../LICENSE-SCOPE.md. External Infinite Heaven/IHHook remain requirements, not included implementations.

`GameDir/mod` contains 20 authored Lua modules. `ImmersiveMotherBase.lua` is the only owned top-level IH menu; daily life, regular soldiers/hierarchy, training and diagnostics sit below it. The optional browser server is not required to calculate needs or duties.

The public core excludes our IH-extra-NPC adoption/controller/inspection experiment. It observes available regular Soldier2 actors, tracks persistent identity/needs and rank ceilings, retains native patrol dispatch, bounded updates, reservations and recorder012. Corporals can lead teams at most, sergeants can lead squads, privates remain soldiers.

Missing clean route/service/motion resources intentionally keep muster, gathering, shower/rest and CQC starts unavailable. A button or historical private test is not new-build gameplay acceptance. `resources-authored` is an unregistered route source template; experimental-sdk is not loaded. See ../INSTALL.md and ../ROADMAP.md.

Offline checks exercise actual Lua 5.1 syntax, one-menu wiring, inactive/throttled work, regular actor initialization, unavailable-resource gates, patrol/cleanup, recorder sample closure and pure behavior/rank/reservation cases. They do not prove native installation or performance.
