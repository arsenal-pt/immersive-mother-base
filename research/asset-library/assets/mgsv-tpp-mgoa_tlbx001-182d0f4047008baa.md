# mgoa tlbx001

Textured static native model reference; assembly and interactivity are not inferred.

[Discovered static models table](../tables/discovered-static-models-4b29110f-batch-1.md) | [Library](../README.md) | [Credits](../sources-and-credits.md) | [Batch source data](../batch-provenance.json)

## Still reference

![mgoa tlbx001](../../../media/asset-previews/2026-10-16-installed-completions/mgsv-tpp-mgoa_tlbx001-182d0f4047008baa.png)

## 360-degree reference

![mgoa tlbx001 camera orbit](../../../media/asset-previews/2026-10-16-installed-completions/mgsv-tpp-mgoa_tlbx001-182d0f4047008baa-360.gif)

Static model; 48 camera views, 100ms/frame,4.8-second loop. This is a reference-camera orbit, not native animation. Actual captured base textures/UVs use approximate studio lighting. FOX shader, collision, interactions and complete assembly are untested.

## Identity and source

| Field | Value |
|---|---|
| Category | Discovered static models > Installed-source static components |
| Tags | static model, native model, mgoa_tlbx001 |
| Native model | `/Assets/mgo/environ/object/mgo_afgh/toolbox/mgoa_tlbx001/scenes/mgoa_tlbx001.fmdl` |
| Native SHA256 | `f652aa025af99ed1040204f54e304ab0086d9a475412f4decf32b679e74dc168` |
| Captured source container | `/Assets/mgo/pack/location/afc0/pack_common/afc0_common.fpk` |
| Captured source container SHA256 | `20a950cab0d6912ac3a270b90dc6dc673f2d13859eb636819bfa3955fca6e320` |
| Location evidence | Selected native member/content and captured installed-source chain; full archive SHA/runtime priority unresolved |
| Current installed DAT / priority | Captured as-installed chain; full archive SHA and effective runtime priority unresolved |
| Upstream preparation | Selective installed-archive staging by the credited GzsTool Core bridge; actual complete FTEX-family conversion by FtexTool; automatic native inspection and reference rendering. |

Source namespace is a path identity, not exclusive original use. Lowercased lookup keys are separate from the exact retained member spelling.

## Quality and native LOD inventory

Texture pixels/mips, geometric detail and approximate studio shader fidelity are separate. Only LOD0 was rendered for this imported batch. Other levels are inventoried, not newly previewed; identical decoded index sets map to their recorded counterpart. The decoded-indices hash uses UTF-8 canonical JSON of triangle-index lists grouped by mesh, not the original packed index-buffer bytes. No upscaling or invented geometry.

| Native LOD | Triangles | Decoded indices SHA256 | Duplicate mapping | Preview status |
|---|---:|---|---|---|
| 0 | 210 | `bbc34f68dc1274bc46a9478daf07d3afc8ddd0b4f7a8eac8dd6aa955fe10f33a` | Distinct within retained model | Rendered above |
| 1 | 200 | `86d4c199ed7a8deca9139bbaea7832691a751edcba4c802db8e7aad3b9cf1d2e` | Distinct within retained model | Not rendered |
| 2 | 194 | `eac195ab58c8111a347229e59a8017297f3510ef6b696d0d414180585462cda5` | Distinct within retained model | Not rendered |
| 3 | 190 | `0435f0dba06cfa244873de7ba2822fd79e2bcdd64eee3c0eb66a0d18365dd9b2` | Distinct within retained model | Not rendered |

## Base textures

| Material | Native sampler / path hash | Pixels | Mip levels | Retained DDS SHA256 |
|---|---|---|---|---|
| 0 | Base_Tex_SRGB / `1543527986023263228` | 512 x 256 | 8 native/header verified | `54f0226cd4818ac486de6519681170379d8889130ec6f11a02cb6fbd64720dcd` |

Texture virtual filenames are unknown where only native hashes are available. Larger native textures elsewhere in the game were not searched. Only actual base-color maps are applied; normal/specular/packed shader channels are not recreated.

## Attribution and limits

Game models/textures: Konami. Project owner: arsenal-pt. Authored importer/metadata/reference work: OpenAI Codex (AI/LLM). [Community tools and detailed credits](../sources-and-credits.md). No endorsement is implied. Game artwork is outside the original-code license.

Only rendered references and descriptive metadata are distributed. Raw assets, native files, textures, decoded geometry, Blender scenes, private source paths and clean frame caches remain private. [Catalogue](../catalogue.json) and [batch provenance](../batch-provenance.json) preserve identity and media hashes.

## Captured base-texture locations

| Material | Actual native texture path | Complete family identity |
|---|---|---|
| 0 | `Unknown; native binding retained` | `76e3e26c5efe3086aba03bf22eeb7496a5e95eebeb5b41743a874776cf252997` |
