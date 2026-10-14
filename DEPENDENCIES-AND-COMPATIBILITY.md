# Dependencies and compatibility for the scoped alpha

Creator/maintainer: **arsenal-pt**. **Codex is credited as an implementation contributor**, including the original AI/LLM-developed code and this readiness audit. Eligible original project source remains GPL-3.0-only. The game, Infinite Heaven/IHHook and external tools belong to their respective authors.

The default core can be packaged as loose Lua files without a new native route, service or motion archive. It contains six IH modules and fourteen helper modules. A working external IH installation discovers the six files in mod/modules, loads each returned Lua table, and registers their declared menus. No edit to an IH module-list file is required. The helper files go in mod/nlab. Retain the action-recordings directory for the experimental recorder.

Runtime requirements are a locally owned MGSV TPP installation and separately acquired Infinite Heaven/IHHook. Python and Lupa are not in-game runtime requirements: Python is used by the optional companion, and Lupa/Lua5.1 by offline development tests. FoxLib, FSharp.Core, CityHash and a C# compiler are needed only for the separate authored-route build work; those binaries are not bundled or needed by this scoped core alpha.

The inspected local Infinite Heaven package identifies itself as r267, targets MGSV 1.0.15.4 and declares IHHook r24 or later compatible. Its loader/menu functions were replayed offline with the actual copied core in both discovery orders. This establishes the inspected source interface, not a completed fresh native installation or a promise for all later framework/game versions.

## IHHook performance boundary

The public core does not call IHH or create/connect IHHook named pipes. The optional companion uses status files and atomic text command mailboxes; it does not use those named pipes. Therefore the local output-pipe repair is not a hard load-time dependency of these modules.

However, **stock IHHook r25 is not performance-validated for this new alpha**, and it has a known shared transport defect. In the inspected pinned r25 source, an output worker starts after paired client connections, busy-polls an empty queue and checks disconnection only while processing a message. Repeated paired client sessions can retain workers and collapse FPS. Missing route/service guards do not fix this. Other tools, legacy IHExt or another pipe client can exercise the shared defect.

The stock r25 DINPUT8.dll hash in the inspected publisher package is:

    b205cc363eb6af6ab449ec5a2fc08702094a462ef606a7177e83cd54c9a48935

The historical native performance/reconnect reference used a separate local r25 repair, output-pipe-lifecycle-1:

    d81ebb830404e9fb6454e7142520b3ed00e73720449f79bd439855610bd18e42

Its pinned upstream source revision is 924278894bab056e7d035abc3fbfe4bd726ad4ce. Historical verification passed 14 focused real-pipe cases and 80 native reconnects without thread growth, followed by a roughly15-second foreground frame sample. Those results belong to that exact repaired external build and the then-tested private mod stack. They are not native proof for stock r25 or this new alpha.

Treat the repaired hash as the tested reference, and stock r25/unknown hashes as unverified compatibility states with the known IPC hazard. A future supported upstream equivalent needs its own audit and acceptance. No third-party replacement DLL is bundled here. Whole input/server shutdown, safe DLL unloading, independent concurrent clients and long endurance remain outside the old repair's measured contract.

## What this alpha actually enables

The core observes currently available regular native Soldier2 actors, tracks stable staff identities, local persistent simulated needs/health and rank hierarchy, and dispatches ordinary patrol/roam using routes already provided by the game. Military appointment ceilings remain; simulated health is not native combat HP. Native name catalogs are absent, so labels use the existing generic fallback.

Service-dependent hunger/thirst/fatigue/hygiene/bladder needs are deferred while their services are unavailable. Social need is still a logical measure; no new gathering is available to satisfy it. The IH menu provides basic counts/availability and exposes existing API actions, rather than a finished native personnel dossier/map UI. Snapshot files and the optional companion provide fuller inspection.

Muster, gatherings, fixed guard posts, native water/mess/bunk/toilet/shower services and CQC starts remain unavailable. All authored route/service/motion proof flags stay false. Stop/cleanup and ordinary patrol remain available in a ready normal Mother Base context. No new personnel, test pool, IH-extra adoption, specialist routines, full sleep/shower action or automatic CQC are supplied.

Recorder012 remains experimental and read-only. Its prior native evidence is a short inert take; human menu interaction, gameplay events, manual/context stop, long capture and FPS endurance for this build are pending. Default recorder notifications are off and its status function caches/returns feedback; a complete visible recorder UX is not claimed. No animation-ID/bone/input capture or replay is supplied.

The optional v9.1 geometry reconstruction is separate, carries known collision/render defects and must not be included in the default core install.

## Readiness checks and next steps

The scoped context fix prevents cached commands/requests and provider actions in non-normal, loading/activating, different-mission or unsupported-cluster contexts. Portable tests/test_readiness.py tests patched contexts directly with an authored IH-contract/native/file fixture. It ships no upstream framework source, opens no real pipes and runs no game. The separate audit replay used the inspected local IH source functions in memory.

Two snapshots each passed the existing94core checks and31pure life cases. The focused actual-IH audit passed25checks. The portable patched-only regression passes16checks and fails against the original published context behavior. These are offline evidence. Fresh install/restore, human IH menu interaction, actual game/framework FPS and endurance remain separate native gates.

Later resource work should package only the authored empty-set route output, audit its pack admission, and validate Command-layout/grade/location/navigation before enabling assemblies. Service catalogs need local owned-resource generation and endpoint/queue/use/exit proof. CQC needs a clean owned-motion adaptation recipe and fresh session/interruption/performance proof. Do not enable historical flags merely because serialization or installation succeeds.

Run the portable regression from the repository root with existing Lupa, optionally specifying its directory:

    python -B tests/test_readiness.py --library-dir <existing-lupa-directory>

Tool credits: Infinite Heaven by TinManTex, inspected fork by caplag; IHHook by TinManTex/its maintainers; Python and Lupa/Lua5.1 for offline checks; FoxLib/FoxKit, FSharp.Core and CityHash for the separate resource tooling. This audit supplies no upstream implementation or dependency binary.
