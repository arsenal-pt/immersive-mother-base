# Runtime ownership and performance budgets

## Keep the simulation separate from the engine population

An authored life record is not a native soldier. Logical staff identity, rank, appointments, needs, social history and planned duty can persist when an actor is not present or streamed. Native movement, collision, animation, rendering, pathfinding and game-object calls still cost engine resources. A future virtual population can reduce physical-actor demand only if it never invents a native ID or reports arrival without observing it.

The development design uses three conceptual levels: active physical actors receive the existing 4 Hz behavior update and fresh native checks; nearby or relevant actors can use slower staggered decisions; distant records advance analytically and stay virtual. Promotions can follow player proximity, alarms, muster or facility transfer, with hysteresis and bounded work per tick. This is a proposal, not an engine feature exposed by MGSV.

Keep one authority for each state and one owner for each native movement/action. Activity leases should carry actor identity, generation and session epoch; they end on completion, interruption, departure or a higher-priority order. Muster, urgent needs and danger must release reservations cleanly. A stale session must never release or overwrite a newer command. A future process boundary should exchange compact observations carrying epoch, tick, actor generation and timestamp. Commands need sequence, expiry and acknowledgement. The game-thread adapter validates native life/status immediately before actions. Backend loss must suppress stale commands and leave a safe native route active.

## Measured cost and what it means

Offline profiling of the authored Lua core tested 18 through 1,000 **logical records** with Lua 5.1. State stepping stayed relatively small while full JSON snapshot generation grew from about 1.85 ms at 18 actors to 40.84 ms at 1,000; an eight-neighbor-per-person stress fixture reached 136.77 ms. The fixture intentionally stresses telemetry and is not a claim about live relationship density. The harness has no game actors, engine calls, rendering, file writes, IPC or FPS measurement.

A candidate retained 4 Hz behavior and 30-second persistence but built dashboard snapshots at 2 Hz. In a 160-second isolated trace, 641 state snapshots and 234 action/dialogue events matched the pinned baseline; status writes fell from 1,282 to 321. A bounded live file sample later confirmed roughly 0.5-second publication with 18 actors and no script errors. It measured publication behavior only, not frame-time or CPU improvement.

Source query counting found duplicated polling in the soldier adapter: for each enabled ordinary-life actor, the audited steady state issued 34 SendCommand getters/s, four combat-rank reads/s and two discovery-ID reads/s, plus two diagnostic status writes globally. These are counts, not durations. The next useful optimization is one shared observation capture per 4 Hz tick and slower/dirty refresh of identity and rank, with cache invalidation on actor generation, mission, cluster or ownership changes.

## Diagnose the reported slowdown before optimizing

Capture the exact triggering scene, foreground process, actor count, module flags, time since load, dashboard state and installed hashes. Measure the same scene and view with a red-capable interval metric; average FPS can hide short 1–5 FPS stalls. Inspect one-second present cadence, long gaps and p95/max intervals as well as averages. Compare the game render counter and simulation publication separately. A healthy renderer can coexist with stale simulation, and an os.clock wrapper is not a GPU or render-thread profiler.

Change one subsystem boundary at a time and retain the failing trace. Disable/update modes may leave native routes and pathfinding running, so they do not isolate all actor costs. Restore diagnostic wrappers and confirm ordinary publication in a cleanup path. If the trigger does not recur, report the healthy sample and keep the cause unresolved.

Historical short captures measured roughly 59 FPS during baseline and 58.9 during a gathering/movement sample, with a 135.9 ms hitch. Neither reproduced the reported 1–5 FPS episode. A later background-focus sample is explicitly inconclusive. Do not claim a fix or FPS benefit from these results.

## Scheduling and telemetry guidance

- Keep the active model in memory; batch persistence and measure serializer and consumer parsing separately.
- Publish a compact active-map feed at a fixed low rate; page history and relationships on demand.
- Bound group operations and relationship growth; mark derived group state dirty when membership changes.
- Do not move scheduling to SQLite, a spreadsheet engine or another process before measuring transfer, synchronization and failure-recovery cost.
- Use spreadsheets as authoring input for validated versioned tables, not as a runtime dependency.
- Treat Unity/Epic population scheduling material as design analogy only. FOX Engine does not expose Unity or MassGameplay through these notes.

## References and provenance

Private development evidence summarized from the performance plan, isolated 160-second equivalence report, native query audit and interval-replay notes. These reports are not included in this package. The archived baseline hash starts 9ddd39ba; exact report hashes should be re-collected if rebuilding the current public branch.

- [Unity update manager guidance](https://docs.unity3d.com/2018.4/Documentation/Manual/BestPracticeUnderstandingPerformanceInUnity8.html)
- [Unreal MassGameplay overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine)
- [Unreal Significance Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/significance-manager-in-unreal-engine)
- [Lua 5.1 manual: garbage collection](https://www.lua.org/manual/5.1/manual.html#2.10)
- [SQLite appropriate uses](https://sqlite.org/whentouse.html)

