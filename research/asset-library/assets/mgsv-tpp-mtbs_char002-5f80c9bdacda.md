# Folding chair

A weathered blue folding chair with a white metal frame, suitable as a visual reference for hangar, office or rest-area seating.

[Seating table](../tables/seating-1.md) | [Library](../README.md) | [Credits and evidence rules](../sources-and-credits.md)

## Still reference

![Folding chair - clean textured still](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-mtbs_char002-5f80c9bdacda.png)

## 360-degree reference

![Folding chair - full camera orbit](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-mtbs_char002-5f80c9bdacda-360.gif)

The camera circles a static model. This is not a native game animation. Actual retained base-color texture/UVs are shown with approximate studio materials and lighting; this is not proof of FOX shader or gameplay equivalence.

## Identity and location

| Field | Value |
|---|---|
| Category | Furniture > Seating |
| Tags | chair, folding-chair, seating, furniture, metal-frame, blue-upholstery, hangar, mother-base |
| Source namespace | mother_base; this does not establish exclusive original use |
| Observed retained use | Retained static Huey/Battle Gear hangar variants btg00 through btg05. |
| Native model | `/Assets/tpp/environ/object/mother_base/chair/mtbs_char002/scenes/mtbs_char002.fmdl` |
| Native SHA256 | `5f80c9bdacdab46673a783adc5bd997618f1a13738e2f4401f99b799974eab43` |
| FPK | `/Assets/tpp/pack/mission2/free/f30050/f30050_hanger_btg00.fpk` |
| Retained FPK SHA256 | `4ad3d31598aff8eff00f8d507f80e5b6e491c71c0bda03fb991391a2560453c9` |
| Historical DAT origin | `master/chunk3.dat`; current installed DAT unverified |
| Location evidence | Retained indexed member identity plus unique byte-exact FMDL payload and indexed path string in retained FPK; no fresh extraction/current DAT check |
| Selected geometry | LOD0; 358 triangles; native geometry/UV inputs unchanged |
| Native bounds | `[[-0.25523099303245544, -0.00389080005697906, -0.3178029954433441], [0.25523099303245544, 0.9150750041007996, 0.24254100024700165]]` (native coordinate units) |
| Preview | Blender5.2.2;768px still;480px GIF;48angles/7.5degrees;100ms each;4.8seconds;160px static thumbnail |

## Texture bindings

Bindings below are source metadata. Only the actual base-color texture drives this approximate preview. Native texture virtual paths are unknown where stored by hash; the DDS hashes identify retained converted content, not fabricated game filenames.

| Sampler | Native path hash | Native virtual path | Retained DDS SHA256 | Dimensions |
|---|---|---|---|---|
| Base_Tex_SRGB | `1542935154948558078` | Unknown; hash identity retained | `105362d96275cb39c12d25ece58841b1a7dfe89c2628d1e85559acd1b9f67c7f` | 512x256 |
| NormalMap_Tex_NRM | `1543544073143106902` | Unknown; hash identity retained | `e05db30fb6e7a68d664599b7734b5848fd3929e6a5136f4d5a3adc96b32187d5` | 512x256 |
| SpecularMap_Tex_LIN | `1542766372082993548` | Unknown; hash identity retained | `7af34bf62110276d1692eb94d0e9901aed9b4d27a1a1d1603fea54e4202c6505` | 512x256 |
| MatParamMap_Tex_LIN | `1542914060993304892` | Unknown; hash identity retained | `cbc88981516d43e65c57e26504284d6694169be0d56d5a3be9a2195b51aff6e8` | 512x256 |

## Native LOD comparison

All four native face sets use the same source bounds, framing and highest verified retained base-color texture. LOD0 has the most triangles for this model in these retained inputs. Mesh detail is separate from texture resolution and approximate studio shading. No larger retained base version was found; this does not establish absence elsewhere in the game.

![Folding chair - four native LODs compared](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-mtbs_char002-5f80c9bdacda-lod-comparison.png)

| Preview | Native LOD | Geometric detail | Triangles | Base texture | Open selected view |
|---|---|---|---:|---|---|
| [![Folding chair LOD0](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-mtbs_char002-5f80c9bdacda-thumb.png)](#still-reference) | LOD0 | Highest retained geometric detail | 358 | 512x256; 8 mips | [Existing original reference](#still-reference) |
| [![Folding chair LOD1](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-mtbs_char002-5f80c9bdacda-lod1-thumb.png)](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod1.md) | LOD1 | Reduced geometric detail 1 | 270 | 512x256; 8 mips | [Still and 360-degree view](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod1.md) |
| [![Folding chair LOD2](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-mtbs_char002-5f80c9bdacda-lod2-thumb.png)](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod2.md) | LOD2 | Reduced geometric detail 2 | 196 | 512x256; 8 mips | [Still and 360-degree view](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod2.md) |
| [![Folding chair LOD3](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-mtbs_char002-5f80c9bdacda-lod3-thumb.png)](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod3.md) | LOD3 | Reduced geometric detail 3 | 150 | 512x256; 8 mips | [Still and 360-degree view](mgsv-tpp-mtbs_char002-5f80c9bdacda-lod3.md) |

### Texture channels and mip counts

These native/DDS header sizes are separate from geometric LOD. Only the base map is used in the studio preview; other channels are catalogued rather than treated as engine-perfect shading.

| Channel | Pixels | Native/DDS mip levels | Used in preview |
|---|---|---:|---|
| Base_Tex_SRGB | 512x256 | 8 | Base color only |
| NormalMap_Tex_NRM | 512x256 | 8 | Recorded, not applied |
| SpecularMap_Tex_LIN | 512x256 | 8 | Recorded, not applied |
| MatParamMap_Tex_LIN | 512x256 | 8 | Recorded, not applied |

[Exact native LOD/deduplicated source mappings, texture hashes and declared mip dimensions](../quality-provenance.json). No original textures or geometry are included.

## Attribution and limits

Game model and textures: Konami. Reference preparation is AI/LLM-authored using the established community tool pipeline; see [central credits](../sources-and-credits.md). The repository owner is arsenal-pt. Game artwork is not covered by the original-code license.

Friendly labels and tags come from native folder identity, recorded scene use and reviewed preview appearance. Runtime interaction, folding/rolling/wheel movement, collisions, progression and native material response were not tested. A use tag is a search aid, not a promised mechanic.

No source FMDL, texture, archive, decoded geometry or blend is provided. The [catalogue](../catalogue.json) includes this entry and media hashes; clean frames and original sources remain private.
