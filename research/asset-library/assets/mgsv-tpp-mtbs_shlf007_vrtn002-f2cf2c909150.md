# Shelf component / variant 002

A native metal shelf component or variant. The full assembled storage unit and interaction are not established.

[Furniture table](../tables/furniture-batch-1.md) | [Library](../README.md) | [Credits](../sources-and-credits.md) | [Batch source data](../batch-provenance.json)

## Still reference

![Shelf component / variant 002](../../../media/asset-previews/2026-10-16-retained-batch/mgsv-tpp-mtbs_shlf007_vrtn002-f2cf2c909150.png)

## 360-degree reference

![Shelf component / variant 002 camera orbit](../../../media/asset-previews/2026-10-16-retained-batch/mgsv-tpp-mtbs_shlf007_vrtn002-f2cf2c909150-360.gif)

Static model; 48 camera views, 100ms/frame,4.8-second loop. This is a reference-camera orbit, not native animation. Actual retained base textures/UVs use approximate studio lighting. FOX shader, collision, interactions and complete assembly are untested.

## Identity and source

| Field | Value |
|---|---|
| Category | Furniture > Storage components |
| Tags | shelf, storage, component, mother-base |
| Native model | `/Assets/tpp/environ/object/mother_base/shelf/mtbs_shlf007/scenes/mtbs_shlf007_vrtn002.fmdl` |
| Native SHA256 | `f2cf2c9091500cbf17911fc372b75d1c8a1b7bd8cc6dd3b851a94b91ce705ce9` |
| Retained container | `/Assets/tpp/pack/mission2/free/f30050/f30050_hanger_btg00.fpk` |
| Retained container SHA256 | `4ad3d31598aff8eff00f8d507f80e5b6e491c71c0bda03fb991391a2560453c9` |
| Location evidence | Retained member record joined by native SHA/path; selected raw hash rechecked. Archive not freshly unpacked. |
| Current installed DAT / priority | Not verified; outer DAT unknown for this record |
| Upstream preparation | Retained pre-extracted native FMDL/converted DDS; no converter invoked by this job |

Source namespace is a path identity, not exclusive original use. Lowercased lookup keys are separate from the exact retained member spelling.

## Quality and native LOD inventory

Texture pixels/mips, geometric detail and approximate studio shader fidelity are separate. Only LOD0 was rendered for this imported batch. Other levels are inventoried, not newly previewed; identical decoded index sets map to their recorded counterpart. The decoded-indices hash uses UTF-8 canonical JSON of triangle-index lists grouped by mesh, not the original packed index-buffer bytes. No upscaling or invented geometry.

| Native LOD | Triangles | Decoded indices SHA256 | Duplicate mapping | Preview status |
|---|---:|---|---|---|
| 0 | 240 | `17bf18617d592cd38f1fb0903db32c8a0cc0addb9b1ba3d693213d52bd9e1c3d` | Distinct within retained model | Rendered above |
| 1 | 174 | `efe0c224afe720114f0d21a8dc002579232fd93bc223b5e15078ffcc7b1f563d` | Distinct within retained model | Not rendered |
| 2 | 140 | `89a85acc35a472fe6f7c7cfe3d5297c03dc2c7f49e1eb3a82c7dbf9315e01ca6` | Distinct within retained model | Not rendered |
| 3 | 120 | `d06bc356a0084ab15b7b62954c374839c468c56ccb0872c459f435e9a74fbcb9` | Distinct within retained model | Not rendered |

## Base textures

| Material | Native sampler / path hash | Pixels | Mip levels | Retained DDS SHA256 |
|---|---|---|---|---|
| 0 | Unknown sampler name (base binding) / `1543210546336962691` | 512 x 512 | 8 native/header verified | `229a21460d3f6da1aca9664382a13afc3355d97b540d785e313334b6e69fd4f4` |
| 1 | Unknown sampler name (base binding) / `1543210546336962691` | 512 x 512 | 8 native/header verified | `229a21460d3f6da1aca9664382a13afc3355d97b540d785e313334b6e69fd4f4` |

Texture virtual filenames are unknown where only native hashes are available. Larger native textures elsewhere in the game were not searched. Only actual base-color maps are applied; normal/specular/packed shader channels are not recreated.

## Attribution and limits

Game models/textures: Konami. Project owner: arsenal-pt. Authored importer/metadata/reference work: OpenAI Codex (AI/LLM). [Community tools and detailed credits](../sources-and-credits.md). No endorsement is implied. Game artwork is outside the original-code license.

Only rendered references and descriptive metadata are distributed. Raw assets, native files, textures, decoded geometry, Blender scenes, private source paths and clean frame caches remain private. [Catalogue](../catalogue.json) and [batch provenance](../batch-provenance.json) preserve identity and media hashes.
