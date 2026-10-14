# Contribution guide

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

Credit to **arsenal-pt**, a mention of **Immersive Mother Base**, and a link back to the official repository would be appreciated. This is a community request for prominent project credit, not an additional license restriction. Applicable license, copyright and third-party notices must still be preserved as required by their terms.

Eligible original contributions use GPL-3.0-only, the same selected code license as the project; full provenance/combined-distribution review remains pending. Prefer issues and pull requests to the official repository. Forks are welcome; the official repository is maintained by arsenal-pt.

## First priority: usable platforms at every construction stage

Pick one department, platform and build/upgrade variant; keep originals immutable and edit copies. Supply a coverage matrix and capability/facility resolver. A small base needs smaller shared/fallback facilities; do not enumerate one fixed final layout or assume one upgrade order.

| Department/area | Target spaces |
| --- | --- |
| Command | Command center, SCIF/TOC, offices and briefing areas |
| Combat | Unit HQs, weapons/CQC/tactics training and drill areas |
| Support | Logistics/supply/QM, depots, motor pool and maintenance |
| R&D | Laboratories, development workspaces and engineering |
| Base Development | Construction/engineering planning, maintenance and workshops |
| Intel | Analysis, communications and operations workspaces |
| Medical | Triage, clinic, treatment/recovery and medical support |
| Lower decks/bays | Barracks/quarters, supplies, vehicles/mechanics; connected large bays where appropriate |
| Open decks | Training, helos/vehicles, ceremonies and drills |

Protect story/FOB entry doors, Paz's Medical space, Huey's office/Battle Gear hangar and other conditional assets. Resolve source versus gameplay placement before integrating loaded rooms. Command1 dimensions/methods are not defaults for other platforms.

Preserve native resource identities, transforms/coordinate conventions, UV/materials, LOD/streaming, stairs/bridges and structural support. Backface shading is separate from floor/wall collision. Blanket no-cull or preview visibility does not prove correct native materials or contact.

Submit independently authored geometry/layout/definitions/code/tests/local-build recipes with source/tool revisions and provenance. Recipes can reference installed-game resources under applicable rights; do not upload copied models/textures/motions/archives, embedded-original Blender files, game/decompiled Lua, saves, dumps, proprietary tools or secrets. Game ownership alone does not grant redistribution rights.

## Specialist personnel

Independent doctor/nurse, researcher, ground-crew, logistics, intel, engineering and command profiles are wanted. Reuse permitted local game resources through authored definitions; do not wholesale copy IH NPC systems. Use one shared registry/life system. Prove each actor/controller's loading, identity/addressability, appearance, walk/hold/return and interruptions before services/groups. Regular-soldier capability is not proof for another family. Protect named/story actors and children.

Retain rank ceilings: privates are soldiers, corporals at most team leaders, sergeants may lead squads; higher appointments require qualified ranks. Appointments do not automatically promote people or alter MGSV ability ratings.

## Acceptance and review

A PR states problem, exact variants, origin/revisions, authored changes, evidence, limits and reversible install/restore. Separate offline and native proof.

Spaces need inward/outward rendering, floor support, upright door passage, navigation, LOD/streaming, progression/story and frame-time tests. Services need arrival, actual supported use, completion/need relief, exit, capacity and cleanup. A timer/API return/render/package roundtrip alone is insufficient. Retain failed/superseded evidence.

Contributors retain rights in eligible original contributions and must have permission to submit them under GPL-3.0-only. No automatic copyright assignment or CLA. Preserve applicable notices and disclose AI use; use the same provenance and review standards for human and AI-developed submissions. Eligible original contributions intentionally submitted for inclusion are licensed under GPL-3.0-only; disclose different third-party terms before submission. Arsenal-pt controls official merges/releases. Contributions and license decisions do not authorize deployment, game launch or publication.

GPL requires corresponding source for covered distributed derivatives, not publication of all private edits or mandatory PRs to this repo. Commercial use is allowed under GPL. Prominent creator credit remains appreciated, while applicable license/notices must be preserved.
