# MGSV asset reference library

A visual reference for stock assets from *Metal Gear Solid V: The Phantom Pain*: see a textured model, find its actual retained game path and source identity, and decide whether it might suit a future mod. This contains rendered previews and descriptive metadata, not downloadable game assets.

**40 parent reference identities, 49 rendered views.** The original 10 parent records and 19 views are preserved. Thirty additional installed-source completed references each add one LOD0 still, camera-orbit GIF and thumbnail. Their other native levels are inventoried, not claimed rendered. These source filenames include MGO namespaces found in the as-installed archives; they are not asserted to be complete assemblies, stock Mother Base placements or vanilla-install content.

This index loads no images. Tables load at most 12 small static thumbnails per page. Open one asset to see its full still and 360-degree camera-orbit GIF.

| Category | Parent models | Browse |
|---|---:|---|
| Furniture > Seating |3| [Folding chair, rolling stool, wheelchair; LOD0-3](tables/seating-1.md) |
| Furniture > Storage components |2| [Shelf variants and upright/frame](tables/furniture-batch-1.md) |
| Architecture > Access and utility components |4| [Ladder, door panel, gate/shutter panel, duct](tables/architecture-batch-1.md) |
| Equipment > Controls and fixtures |1| [Emergency-stop/control switch panel](tables/equipment-batch-1.md) |
| Discovered static models > Installed-source components |30| [Native filenames and captured source variants](tables/discovered-static-models-4b29110f-batch-1.md) |

[Plan and categories](RESEARCH-PLAN.md) | [Standing workflow](workflow.md) | [JSON](catalogue.json) | [Parent CSV](catalogue.csv) | [Credits and evidence](sources-and-credits.md)

## Quality and evidence

Mesh detail, texture pixels/mip levels, and shader fidelity are separate. Browsing tables show selected native LOD/triangle count and actual base-texture dimensions/mips. Detail pages show exact retained model/container paths, content hashes, material sampler names when exported (otherwise explicitly unknown), actual native path/binding hashes and native LOD inventory. Identical native index sets are mapped instead of being rendered repeatedly. Unknown texture filenames and outer DAT origins remain unknown.

The references use actual retained models, UVs and base textures from a privately owned installation, with approximate studio materials on a contrasting light background. Normal/specular/packed FOX shader channels are not recreated. The turntable rotates the camera around a static model; it is not a native animation. These are offline references, not proof of working doors, climbing, collisions, complete assemblies or native engine shading.

- Original seating quality evidence: [12 rendered native LOD views](quality-variants.csv), [native/texture/source records](quality-provenance.json).
- Imported references: [native LOD inventory and preview status](batch-native-lods.csv) covers the original seven retained-source models plus thirty installed-source records. Each imported reference has only its selected LOD0 view rendered; [source/media provenance](batch-provenance.json) distinguishes both groups.

For the original ten retained-source records, exact retained member identity and selected hashes were checked; current installed DAT membership/version was not verified. The thirty installed-source records retain their actual captured as-installed member/container/texture chains and selected hashes. Full archive content SHA, vanilla-install status, exhaustive alternatives and effective runtime priority remain unresolved. See the per-record evidence.

## Local tool and wider catalogue

The [local non-agentic pipeline](../../tools/asset-reference-pipeline/README.md) provides a category/count menu, persistent next-unfinished queue and aggregate portable exports. Once configured, ordinary runs need no AI, MCP, agent or network. Its current automatic source is a prepared **149-version retained index**, not the entire game. An [export import adapter](import_batch.py) merges reviewed portable output without re-rendering or reading raw game assets.

The [whole-game discovery and static-preview tool](whole-game-catalogue.md) now automatically joins installed archive/eligible loose models to real material/texture dependencies and the same renderer. Its default menu targets new completed model previews, skips valid caches and finite unsupported entries, resumes unfinished work and exports an aggregate local catalogue. It is separate from the old149-model profile and is not an all-game visual-completion claim. The dated metadata snapshot and current proof/format limits are documented on that page. The 30 installed-source references below are a reviewed output batch from local development. Publishing these references does not publish the separate newer local tool-code history.

Konami retains rights in game artwork. No FMDL, textures, archives, decoded geometry, Blender files or tool binaries are bundled. Authored reference code/metadata was developed using AI/LLMs; arsenal-pt owns the project and OpenAI Codex prepared the implementation. See [central credits and license scope](sources-and-credits.md).

## Installed-source completed reference batch - 16 October 2026

Thirty existing completed references were selected from a read-only queue snapshot. Their media are copied byte-for-byte, not re-rendered. [Completion identities](completion-proofs.json) and [full portable source/material/texture/tool evidence](batch-provenance.json) retain actual captured provenance. Names remain sanitized native filenames; interactions and complete assemblies are untested. The original 10 records and all accepted seating LOD media remain unchanged. No raw model, texture, geometry, operational database or private machine path is distributed.
