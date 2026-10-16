# Local asset reference pipeline (first slice)

After setup, double-click **AssetPipeline.cmd** to process your selected manifest and write a fresh local portable catalogue. The window stays open with the result/error and output path. It uses installed tools and local Python code: ordinary runs require no LLM, MCP, agent, network account or server. This is an early local tool, developed entirely using AI LLM assistance (OpenAI Codex), owned by arsenal-pt.

The tested path is a selected static prop in an already retained FPK plus its explicitly identified FTEX family. It runs **Atvaark's GzsTool and FtexTool**, the reused authored native reader/LOD audit, Blender and Pillow. It produces textured stills, 360-degree camera GIFs, thumbnails and a reference catalogue. It does not invent extra model detail or modify the game.

## Setup once

1. Use Windows with your own legitimate game files. Install/configure community tools yourself; this tool does not download or install them. Tested: GzsTool 0.5.3, FtexTool 0.3.3, Blender 5.2.2, Python 3.14.0 with Pillow 12.2.0. The Python code uses 3.11+ features; other tool versions need local verification. Keep each tool's DLLs beside its executable.
2. Copy config.example.json to a **private** config.local.json, and selected-job.example.json to a private job manifest. Supply actual paths and SHA256 pins. Set sourceRoots to the existing private retained source folders. Keep raw files, recipes and source indexes private.
3. Choose a short, local fixed-disk runtime (default %LOCALAPPDATA%/MGSV-Asset-Reference) and a separate exportRoot (default %LOCALAPPDATA%/MGSV-Asset-Reference-Exports). Each default click makes a new timestamped review folder there. Never put the working SQLite/cache in Google Drive, the public checkout, or a source folder. Old .NET converters have path limits; short content-directory keys retain full fingerprints and detect collisions. Existing NTFS aliases are used if available. A very deep runtime can still fail safely; use a short path.
4. Point defaultManifest at the selected job. A recipe supplies exact FPK member/model hash and reviewed material sampler/path-hash → FTEX family/expected DDS hash bindings. This first slice **does not discover those associations across the entire game**. Start from a trusted retained source index or manually reviewed recipe.
5. Set MGSV_ASSET_PYTHON to your Python executable and optionally MGSV_ASSET_CONFIG to your private config path. The launcher otherwise uses python and config.local.json beside itself. CLI Python needs Pillow as well as the configured encoding interpreter; use the same interpreter.
6. Run AssetPipeline.cmd doctor. It fingerprints actual binaries/helpers and reads Windows file versions plus configured Python/Pillow versions. Unsupported/missing tools or source pins require review. The launcher then runs the default manifest when double-clicked.

Examples (substitute your paths):

    python pipeline.py --config PRIVATE/config.local.json doctor
    python pipeline.py --config PRIVATE/config.local.json run --manifest PRIVATE/selected-job.local.json
    python pipeline.py --config PRIVATE/config.local.json queue --manifest PRIVATE/selected-job.local.json
    python pipeline.py --config PRIVATE/config.local.json work
    python pipeline.py --config PRIVATE/config.local.json status
    python pipeline.py --config PRIVATE/config.local.json cancel --job JOB_ID
    python pipeline.py --config PRIVATE/config.local.json work --job JOB_ID
    python pipeline.py --config PRIVATE/config.local.json export --job JOB_ID --output NEW_EMPTY_EXPORT_FOLDER

Use multiple --job arguments for selected exports. Export must be a new/empty folder outside runtime, source roots and the accepted public checkout. Publication is a separate human-reviewed step.

## What runs and what remains manual

| Input | Supported automatic stages | Preparation / limits |
|---|---|---|
| known-static-native | Stage selected FPK; actual GzsTool unpack; stage one FTEX family per material; actual FtexTool DDS; native reader/LOD inventory; render; encode; database/export | Exact retained FPK/member/material/texture recipe required. Only selected FPK and complete FTEX families, not a whole DAT search. |
| prepared | Pinned native FMDL + reviewed DDS/caches; compare caches to direct native reader/LOD proof; render; encode; database/export | Existing extraction/conversion is an explicit prerequisite. This mode does not claim it ran Gzs/Ftex. |
| Other layouts | manual_review | Characters/skinning/FOVA, hidden-group assembly, Unity GUI import, string-path material bindings, unknown sampler hashes, missing/ambiguous textures and arbitrary new format/tool CLIs are not implemented. |
| Animations | Parked | Later adapter; no extraction or animation playback in this slice. |

The bundled static reader is reused byte-exactly. native.py factors the already verified LOD audit into a single-file adapter. See dependency-provenance.json for hashes and pinned community format reference. No new universal converter, third-party binary or third-party source is bundled.

The selected source read records all native LOD counts/index hashes and actual DDS/FTEX pixel/mip metadata. Identical native index sets map duplicateOf to the first corresponding LOD; selected previews remain explicit. All LODs are inventoried, but only manifest lods are rendered. Cross-source variant discovery remains a source-index/recipe responsibility.

The production renderer/encoder are the existing scripts in research/asset-library. Output is a clean 768px still, 48×480px full360 camera frames, a 4.8s looping GIF (100ms/frame), and 160px static thumbnail. Clean frames remain private before any labels. Actual base-color maps/UVs are used with approximate studio shading. Normal/specular/packed FOX material reconstruction, native lighting, native animation, LOD thresholds, physics and gameplay are not reproduced.

## Jobs, cost and recovery

The private jobs.sqlite holds the queue, source/config/tool paths, process argv/PIDs, status, stage fingerprints and asset records. It stays private. One worker runs sequentially; Blender uses two threads. Status writes occur at stage/process transitions.

Stages are content-addressed separately: archive/tool inputs → unpack; FTEX family/tool → DDS; model/reader/audit → native data; native data/selected LOD/base material/Blender/renderer → render; render/Python/Pillow/encoder → GIF. Friendly title, description, category and tag changes update the database/export without another converter or render run. Every cache hit verifies its recorded file hashes. Corrupt/incomplete cache output is retained as diagnostic evidence and rebuilt; short-key collisions block instead of reusing the wrong data.

Cancellation from another console sets a DB flag. The worker terminates/waits for only its own child, retains partial output, marks cancelled and releases its lock. Requeue or work --job resumes from validated completed stages. Child exit failure/timeout never becomes a complete stage. An unsupported/ambiguous input is manual_review; execution failure is failed. Cancel does not delete prior completed references.

A hard OS/process crash may leave worker.lock and an orphan child. This slice does not claim automatic hard-crash recovery. Inspect the recorded worker PID and private process events/logs; ensure the owned child stopped before manually removing a stale lock. Do not kill unrelated Blender/game processes.

## Portable catalogue and privacy

Export creates a **fresh** catalog.sqlite with only assets, lods and textures tables, plus JSON, CSV, Markdown and rendered PNG/GIF. It does not copy the operational jobs database. Only virtual /Assets game paths, hashes, selected quality/texture facts, tool fingerprints and relative media links cross the seam. A final scan rejects machine paths and unexpected file types.

Index loads zero images. Tables contain at most twelve still thumbnails; click one for a larger still and one GIF. Description/tags aid discovery; quality/LOD and texture pixels/mips stay separate. Credits live centrally and on detail pages.

Do not publish raw FPK/FMDL/FTEX/DDS, decoded geometry/cache, game binaries/saves, .blend, private config, logs or operational DB. Rendered reference images do not transfer ownership of Konami's art. Eligible authored source follows the repository GPL-3.0; original assets and community tools retain their own licenses.

## Focused checks

    python test_pipeline.py

Tests use tiny authored subprocess fixtures for failure, CLI cancellation/restart, completed-stage reuse, corrupt cache repair, metadata identity, sampler rejection, collision-safe export and sanitized public SQLite. No game files or large render is required by the unit suite. A real one-chair full48 E2E was separately run on retained private inputs; identical and metadata-only repeats used all five stage caches with zero new converter/render/encoder launches. Upstream preparation limits above still apply.

Sources: [GzsTool — Atvaark](https://github.com/Atvaark/GzsTool), [FtexTool — Atvaark](https://github.com/Atvaark/FtexTool), [FMDL Studio v2 — BobDoleOwndU](https://github.com/BobDoleOwndU/FMDL-Studio-v2), [Blender](https://www.blender.org/), [Pillow](https://python-pillow.org/), and Konami for original MGSV assets.
