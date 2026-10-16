# Duct section

A metal duct section with bent connector geometry. This is a static native variant, not an assembled or functional ventilation system.

[Architecture table](../tables/architecture-batch-1.md) | [Library](../README.md) | [Credits](../sources-and-credits.md) | [Batch source data](../batch-provenance.json)

## Still reference

![Duct section](../../../media/asset-previews/2026-10-16-retained-batch/mgsv-tpp-mtbs_duct002_vrtn001-729a38018dc0.png)

## 360-degree reference

![Duct section camera orbit](../../../media/asset-previews/2026-10-16-retained-batch/mgsv-tpp-mtbs_duct002_vrtn001-729a38018dc0-360.gif)

Static model; 48 camera views, 100ms/frame,4.8-second loop. This is a reference-camera orbit, not native animation. Actual retained base textures/UVs use approximate studio lighting. FOX shader, collision, interactions and complete assembly are untested.

## Identity and source

| Field | Value |
|---|---|
| Category | Architecture > Utility components |
| Tags | duct, ventilation, metal, mother-base |
| Native model | `/Assets/tpp/environ/object/mother_base/duct/mtbs_duct002/scenes/mtbs_duct002_vrtn001.fmdl` |
| Native SHA256 | `729a38018dc08fb68bb29813fa50b2d38c0d4fac432780e22b712f3748ed9b0d` |
| Retained container | `/Assets/tpp/pack/location/mtbs/pack_common/mtbs_common.fpk` |
| Retained container SHA256 | `8d0dbf7b3710768ba90f8b0efa820ee00f33181b7cfc465b67cf29eda9a1700d` |
| Location evidence | Retained member record joined by native SHA/path; selected raw hash rechecked. Archive not freshly unpacked. |
| Current installed DAT / priority | Not verified; outer DAT unknown for this record |
| Upstream preparation | Retained pre-extracted native FMDL/converted DDS; no converter invoked by this job |

Source namespace is a path identity, not exclusive original use. Lowercased lookup keys are separate from the exact retained member spelling.

## Quality and native LOD inventory

Texture pixels/mips, geometric detail and approximate studio shader fidelity are separate. Only LOD0 was rendered for this imported batch. Other levels are inventoried, not newly previewed; identical decoded index sets map to their recorded counterpart. The decoded-indices hash uses UTF-8 canonical JSON of triangle-index lists grouped by mesh, not the original packed index-buffer bytes. No upscaling or invented geometry.

| Native LOD | Triangles | Decoded indices SHA256 | Duplicate mapping | Preview status |
|---|---:|---|---|---|
| 0 | 38 | `13cfc0721f290ee2c0bbf0c695d357b9010169e13c4863d0d314288258faf394` | Distinct within retained model | Rendered above |
| 1 | 37 | `d3bbcd4968e07cbfac4e9ee210eef74ad509c8d35d01d956f9875db052e09f98` | Distinct within retained model | Not rendered |
| 2 | 37 | `d3bbcd4968e07cbfac4e9ee210eef74ad509c8d35d01d956f9875db052e09f98` | LOD1 | Same index set as LOD1; no separate preview |
| 3 | 37 | `d3bbcd4968e07cbfac4e9ee210eef74ad509c8d35d01d956f9875db052e09f98` | LOD1 | Same index set as LOD1; no separate preview |

## Base textures

| Material | Native sampler / path hash | Pixels | Mip levels | Retained DDS SHA256 |
|---|---|---|---|---|
| 0 | Unknown sampler name (base binding) / `1543493658329268165` | 512 x 1024 | 9 native/header verified | `0c147e66620df71e7b5c8dcad4a6f47cf2ce20c838e06f37045c4b16b2cff97b` |

Texture virtual filenames are unknown where only native hashes are available. Larger native textures elsewhere in the game were not searched. Only actual base-color maps are applied; normal/specular/packed shader channels are not recreated.

## Attribution and limits

Game models/textures: Konami. Project owner: arsenal-pt. Authored importer/metadata/reference work: OpenAI Codex (AI/LLM). [Community tools and detailed credits](../sources-and-credits.md). No endorsement is implied. Game artwork is outside the original-code license.

Only rendered references and descriptive metadata are distributed. Raw assets, native files, textures, decoded geometry, Blender scenes, private source paths and clean frame caches remain private. [Catalogue](../catalogue.json) and [batch provenance](../batch-provenance.json) preserve identity and media hashes.
