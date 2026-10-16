# MGSV asset reference library

A small visual reference for stock assets from *Metal Gear Solid V: The Phantom Pain*: see what a model looks like, find its exact game path and source identity, and judge whether it could suit a future mod. This contains screenshots/renders and metadata, not downloadable game assets.

The first set has **three textured Furniture > Seating assets, with all four distinct native LODs each: twelve reference views**. The index loads no images; category pages use small static thumbnails. Open an entry for its larger still and 360-degree camera turntable. This does not catalogue all seating assets or the entire game.

| Category | Selected references | Browse |
|---|---:|---|
| Furniture > Seating |3| [Folding chair, rolling stool and wheelchair; LOD0-3](tables/seating-1.md) |

[Plan and categories](RESEARCH-PLAN.md) | [Standing workflow](workflow.md) | [JSON](catalogue.json) | [CSV](catalogue.csv) | [Credits and evidence](sources-and-credits.md)

The examples use actual retained models, UVs and base-color textures from a privately owned installation, with approximate studio materials on a contrasting light background. Turntables rotate the camera around static models; they are not native asset animations. These are offline reference renders, not proof of engine-perfect shading, collisions, interactions or animation compatibility.

Exact retained model/container bytes are checked. The outer DAT location is a historical extraction origin; current installed DAT content/version was not checked. Unknown texture filenames remain unknown rather than guessed from a hash.

Konami retains rights in the game artwork. No FMDL, textures, archives, decoded geometry or Blender files are bundled. This project/reference pipeline is developed using AI/LLMs; arsenal-pt is the project owner and OpenAI Codex prepared the authored reference work. See the central credits and repository license scope.

Only this three-entry starter was selected. Future work proceeds in expressly assigned small batches; the separate all-game asset catalogue remains parked.

## Quality and variants

The existing previews already use LOD0, which has the most triangles for each of these three models in the retained source. Lower native LOD1-3 views are individually linked from each asset overview with a static four-LOD comparison. Identical model copies in other retained containers are mapped once instead of being rendered repeatedly. The original three IDs/previews remain unchanged.

**Mesh detail, texture resolution and shader fidelity are separate.** Quality/LOD labels include native level and triangle count. The Base texture column gives actual pixels and declared native mip count: folding chair512x256/8mips, rolling stool256x128/7mips, wheelchair1024x1024/9mips. No larger retained base version or higher retained model detail was found within the inspected exact families; this does not prove absence elsewhere in the game. Normal/specular/material channels are catalogued but the studio references use only actual base-color textures with approximate shading. No detail was invented, upscaled or subdivided.

[Native LOD/texture/source evidence](quality-provenance.json) | [All12LODrows as CSV](quality-variants.csv). Native texture mip chains remain private; this is not a LOD-by-mip render product. Runtime thresholds and native shader selection remain untested.
