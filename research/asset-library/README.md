# MGSV asset reference library

A visual reference for stock assets from *Metal Gear Solid V: The Phantom Pain*: see a textured model, find its actual retained game path and source identity, and decide whether it might suit a future mod. This contains rendered previews and descriptive metadata, not downloadable game assets.

**10 unique parent models, 19 rendered reference views.** The original three seating models each have LOD0-3 previews. Seven later references have LOD0 previews; their other native levels are inventoried separately and are not presented as completed previews. Five were produced by the user's local five-item run; two shelf components came from earlier reviewed tool proofs. The chair is included once.

This index loads no images. Tables load at most 12 small static thumbnails per page. Open one asset to see its full still and 360-degree camera-orbit GIF.

| Category | Parent models | Browse |
|---|---:|---|
| Furniture > Seating |3| [Folding chair, rolling stool, wheelchair; LOD0-3](tables/seating-1.md) |
| Furniture > Storage components |2| [Shelf variants and upright/frame](tables/furniture-batch-1.md) |
| Architecture > Access and utility components |4| [Ladder, door panel, gate/shutter panel, duct](tables/architecture-batch-1.md) |
| Equipment > Controls and fixtures |1| [Emergency-stop/control switch panel](tables/equipment-batch-1.md) |

[Plan and categories](RESEARCH-PLAN.md) | [Standing workflow](workflow.md) | [JSON](catalogue.json) | [Parent CSV](catalogue.csv) | [Credits and evidence](sources-and-credits.md)

## Quality and evidence

Mesh detail, texture pixels/mip levels, and shader fidelity are separate. Browsing tables show selected native LOD/triangle count and actual base-texture dimensions/mips. Detail pages show exact retained model/container paths, content hashes, material sampler names when exported (otherwise explicitly unknown), actual native path/binding hashes and native LOD inventory. Identical native index sets are mapped instead of being rendered repeatedly. Unknown texture filenames and outer DAT origins remain unknown.

The references use actual retained models, UVs and base textures from a privately owned installation, with approximate studio materials on a contrasting light background. Normal/specular/packed FOX shader channels are not recreated. The turntable rotates the camera around a static model; it is not a native animation. These are offline references, not proof of working doors, climbing, collisions, complete assemblies or native engine shading.

- Original seating quality evidence: [12 rendered native LOD views](quality-variants.csv), [native/texture/source records](quality-provenance.json).
- Imported batch: [28 native LOD records and their preview status](batch-native-lods.csv), [source/media provenance](batch-provenance.json). Only seven selected LOD0 views are added.

Exact retained member identity and selected source hashes are checked. The current installed DAT content/version and runtime load priority were not verified for these reference records. A copied or retained source is not evidence of current installed membership.

## Local tool and wider catalogue

The [local non-agentic pipeline](../../tools/asset-reference-pipeline/README.md) provides a category/count menu, persistent next-unfinished queue and aggregate portable exports. Once configured, ordinary runs need no AI, MCP, agent or network. Its current automatic source is a prepared **149-version retained index**, not the entire game. An [export import adapter](import_batch.py) merges reviewed portable output without re-rendering or reading raw game assets.

The [whole-game metadata catalogue](whole-game-catalogue.md) is now implemented as a separate local tool:21as-installedQAR archives/202,303outer member occurrences were indexed, plus one bounded nestedFPK proof. **43,596nested containers remain pending; scanner dependencies/previews are0/0.** Count/all is bounded by I/O/time/cache budgets and remaining work resumes later. The bridge from discovered models and exact texture dependencies into the existing renderer is pending. Metadata discovery, assemblies and successful previews remain separate; no all-game visual completion is claimed.

Konami retains rights in game artwork. No FMDL, textures, archives, decoded geometry, Blender files or tool binaries are bundled. Authored reference code/metadata was developed using AI/LLMs; arsenal-pt owns the project and OpenAI Codex prepared the implementation. See [central credits and license scope](sources-and-credits.md).
