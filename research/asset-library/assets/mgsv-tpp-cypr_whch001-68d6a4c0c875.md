# Wheelchair

A blue wheelchair with large rear wheels, push handles and front footrests, shown as a static medical-furniture reference.

[Seating table](../tables/seating-1.md) | [Library](../README.md) | [Credits and evidence rules](../sources-and-credits.md)

## Still reference

![Wheelchair - clean textured still](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-cypr_whch001-68d6a4c0c875.png)

## 360-degree reference

![Wheelchair - full camera orbit](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-cypr_whch001-68d6a4c0c875-360.gif)

The camera circles a static model. This is not a native game animation. Actual retained base-color texture/UVs are shown with approximate studio materials and lighting; this is not proof of FOX shader or gameplay equivalence.

## Identity and location

| Field | Value |
|---|---|
| Category | Furniture > Seating |
| Tags | wheelchair, medical, seating, mobility, blue-upholstery, paz-room, cyprus |
| Source namespace | cyprus; this does not establish exclusive original use |
| Observed retained use | Retained resident Medical/Paz room static furnishings. |
| Native model | `/Assets/tpp/environ/object/cyprus/wheelchair/cypr_whch001/scenes/cypr_whch001.fmdl` |
| Native SHA256 | `68d6a4c0c87566273d3281c7059fbeddf9b6d55252b37eea77495cc338648441` |
| FPK | `/Assets/tpp/pack/location/mtbs/pack_unique/mtbs_unique_0040.fpk` |
| Retained FPK SHA256 | `6ca583eb49087f8444eb123edee8756504dd48d26a9ab4a27e5c3e775e1f0682` |
| Historical DAT origin | `master/chunk3.dat`; current installed DAT unverified |
| Location evidence | Retained indexed member identity plus unique byte-exact FMDL payload and indexed path string in retained FPK; no fresh extraction/current DAT check |
| Selected geometry | LOD0; 1588 triangles; native geometry/UV inputs unchanged |
| Native bounds | `[[-0.38685500621795654, -0.0008611000375822186, -0.5100850462913513], [0.38685500621795654, 0.9604989886283875, 0.6363450288772583]]` (native coordinate units) |
| Preview | Blender5.2.2;768px still;480px GIF;48angles/7.5degrees;100ms each;4.8seconds;160px static thumbnail |

## Texture bindings

Bindings below are source metadata. Only the actual base-color texture drives this approximate preview. Native texture virtual paths are unknown where stored by hash; the DDS hashes identify retained converted content, not fabricated game filenames.

| Sampler | Native path hash | Native virtual path | Retained DDS SHA256 | Dimensions |
|---|---|---|---|---|
| Base_Tex_SRGB | `1542794976997329743` | Unknown; hash identity retained | `60edb4993e25dd7a2d22ccc7c9845601be9236ca6f60d33f52a84a8aad457f40` | 1024x1024 |
| NormalMap_Tex_NRM | `1542752255105725688` | Unknown; hash identity retained | `b51262b24200a77a9cdb0fd16733bf43fd3f8c84c5f2850f94b44001660009c5` | 1024x1024 |
| SpecularMap_Tex_LIN | `1542548934547970504` | Unknown; hash identity retained | `1a058399ed921f5c57770ed9b4a7c844d3f08233666449bdb861748a5253bba5` | 1024x1024 |
| MatParamMap_Tex_LIN | `1542754739783832592` | Unknown; hash identity retained | `a68d3563596aab885f962266eebdbe1d4477ab09da98e26bd0eea7d452828b3d` | 1024x1024 |

## Native LOD comparison

All four native face sets use the same source bounds, framing and highest verified retained base-color texture. LOD0 has the most triangles for this model in these retained inputs. Mesh detail is separate from texture resolution and approximate studio shading. No larger retained base version was found; this does not establish absence elsewhere in the game.

![Wheelchair - four native LODs compared](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-cypr_whch001-68d6a4c0c875-lod-comparison.png)

| Preview | Native LOD | Geometric detail | Triangles | Base texture | Open selected view |
|---|---|---|---:|---|---|
| [![Wheelchair LOD0](../../../media/asset-previews/2026-10-16-seating/mgsv-tpp-cypr_whch001-68d6a4c0c875-thumb.png)](#still-reference) | LOD0 | Highest retained geometric detail | 1588 | 1024x1024; 9 mips | [Existing original reference](#still-reference) |
| [![Wheelchair LOD1](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-cypr_whch001-68d6a4c0c875-lod1-thumb.png)](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod1.md) | LOD1 | Reduced geometric detail 1 | 1452 | 1024x1024; 9 mips | [Still and 360-degree view](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod1.md) |
| [![Wheelchair LOD2](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-cypr_whch001-68d6a4c0c875-lod2-thumb.png)](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod2.md) | LOD2 | Reduced geometric detail 2 | 1384 | 1024x1024; 9 mips | [Still and 360-degree view](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod2.md) |
| [![Wheelchair LOD3](../../../media/asset-previews/2026-10-16-seating-quality/mgsv-tpp-cypr_whch001-68d6a4c0c875-lod3-thumb.png)](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod3.md) | LOD3 | Reduced geometric detail 3 | 1344 | 1024x1024; 9 mips | [Still and 360-degree view](mgsv-tpp-cypr_whch001-68d6a4c0c875-lod3.md) |

### Texture channels and mip counts

These native/DDS header sizes are separate from geometric LOD. Only the base map is used in the studio preview; other channels are catalogued rather than treated as engine-perfect shading.

| Channel | Pixels | Native/DDS mip levels | Used in preview |
|---|---|---:|---|
| Base_Tex_SRGB | 1024x1024 | 9 | Base color only |
| NormalMap_Tex_NRM | 1024x1024 | 9 | Recorded, not applied |
| SpecularMap_Tex_LIN | 1024x1024 | 9 | Recorded, not applied |
| MatParamMap_Tex_LIN | 1024x1024 | 9 | Recorded, not applied |

[Exact native LOD/deduplicated source mappings, texture hashes and declared mip dimensions](../quality-provenance.json). No original textures or geometry are included.

## Attribution and limits

Game model and textures: Konami. Reference preparation is AI/LLM-authored using the established community tool pipeline; see [central credits](../sources-and-credits.md). The repository owner is arsenal-pt. Game artwork is not covered by the original-code license.

Friendly labels and tags come from native folder identity, recorded scene use and reviewed preview appearance. Runtime interaction, folding/rolling/wheel movement, collisions, progression and native material response were not tested. A use tag is a search aid, not a promised mechanic.

No source FMDL, texture, archive, decoded geometry or blend is provided. The [catalogue](../catalogue.json) includes this entry and media hashes; clean frames and original sources remain private.
