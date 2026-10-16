# Immersive Mother Base research notes

These notes collect reusable methods and findings from development of Immersive Mother Base for *Metal Gear Solid V: The Phantom Pain*. They are written for contributors who need to understand the boundaries between simulation code, Infinite Heaven (IH), IHHook, native game actors, and FOX Engine resources.

The notes separate upstream documentation from observations made in a private development setup. Private observations are useful leads, not guaranteed behavior on another game build, platform, mod list, or save. Each result says what was actually checked and what remains unproven. Reproduce against your own legally owned installation and record exact game, IH, IHHook, SnakeBite, platform, grade, mod versions, and hashes.

The published 0.1.0-alpha.1 source is a limited, resource-disabled alpha. Some research below describes later private development prototypes and does not mean those systems ship in that release. IH-extra adoption, autonomous CQC and physical facility services are excluded from the default core. The optional Command1 v9.1/history patches are included as experimental components with known rendering and physics defects; see the version index. Do not infer performance, native acceptance, or feature availability from a development capture.

## Reading order

1. [Runtime and performance](runtime-and-performance.md) â€” ownership, budgets, telemetry and FPS diagnosis.
2. [IH, native actors and bridge safety](ih-native-bridge.md) â€” shared-pipe hazards, bounded commands, adoption rules and capability gates.
3. [Identity and roster safety](identity-and-rosters.md) â€” stable identity, changing rosters and rank-limited appointments.
4. [Platform identity and map model](platforms-and-map.md) â€” native naming, grade-dependent layouts and coordinate evidence.
5. [Asset extraction and editing](asset-pipeline.md) â€” preservation, FMDL/Blender mapping, UV orientation and export limits.
6. [Rendering and collision experiments](rendering-and-collision.md) â€” wall reuse, alpha render modes, collision formats and native acceptance.
7. [Native observation and activity capture](native-capture-and-activities.md) â€” safe camera evidence, CQC findings and showcase limits.
8. [Services, animation and actor capabilities](services-and-capabilities.md) â€” route pilots, Hostage2/IH actors, recorder limitations.
9. [Special rooms and reusable interiors](special-rooms.md) â€” Paz, Huey and Battle Gear source placement and future integration.
10. [Contributor verification recipes](verification-recipes.md) â€” compact repeatable workflows and pending gates.
11. [Version and evidence index](version-and-evidence-index.md) â€” published alpha, later prototypes and failed attempts.

12. [MtarTool punching-combo extraction](mtar-punch-combos/README.md) â€” actual community-tool commands, 25 catalogued attack/receiver/special-actor candidates, source hashes, companions, phase hypotheses and a tested extraction replay; [25 titled full-character GIFs](mtar-punch-combos/gallery.md) and an executed preview recipe.

13. [Animation preview workflow](animation-preview-workflow.md) â€” full-character GIFs, plain-English titles, thumbnails, exact clip links and evidence limits for future animation research.

14. [MGSV Animation Reference Library](animation-library/README.md) — 27 clips in paged animated/still tables, separate category/tag/source-location/description/credit columns, individual larger GIF pages and complete JSON/CSV provenance; [additional references and credits](animation-library/references.md) and a [bounded research plan](animation-library/RESEARCH-PLAN.md) for later selected batches.

15. [LMG ready/reload batch](animation-batches/lmg-reloads/README.md) — two new offline kneeling/standing candidates; [category progress](animation-library/category-progress.json) records 2/2 completed and zero remaining in the defined workbook plus stock-archive scope. No held weapon or native reload/timing/compatibility proof.

## Evidence labels

- **Upstream reference** means a linked public source or tool document. It may document an API or file format without proving a specific runtime result.
- **Private development observation** means a result checked against the project owner's local game/data. Exact reports and raw assets are excluded; descriptions are scoped so a contributor can decide what needs to be reproduced.
- **Offline verification** covers parsers, source audits, fixtures and isolated Lua tests. It does not prove that the game loads or accepts the result.
- **Native observation** is limited to the named development version and scenario. It does not imply public-alpha acceptance or general compatibility.
- **Proposal** means a design direction awaiting implementation or native proof.

## Sources and attribution

Original explanatory text and recipes here were authored for this repository from project research. Tool and format authors remain credited through their upstream projects. See the repository CREDITS.md and each linked source. This research package contains no game assets, extracted archives, binary modules, save data, copied third-party libraries, private memory dumps, credentials, or machine-specific paths.

## Current scope boundary

The public repository owner and project creator is arsenal-pt. Original project implementation was AI-written with human direction and testing; the public README AI disclosure remains authoritative. This research package is intended to help contributors build on the GPL-3.0-only project while preserving upstream licenses and game ownership.

