# Platform identity, grades and map evidence

## Use native identifiers in data

The tested platform is the Command cluster's first platform: native cluster index cl00, plant index pl0, normal location slot mtbs_unique_0000. Project-facing text calls it Command Platform 1. The internal authored simulation commonly uses a one-based department number; convert at one explicit boundary and document it. Do not infer that a similarly named platform in another subsystem shares the same index base.

Other Command platforms were not edited in the v9.1 experiment. Shared props can have cross-department effects if redirected through common packs, so record every touched native path and every common-resource consumer. A Command1 result is not a general platform result.

## Resolve the constructed base from live grades

Command layouts 0–3 correspond to completed Command grades 1–4. Those layouts change bridge counts and connections. Other departments have independent completed grades 0–4. A project audit exhaustively checked 62,500 legal grade vectors. Construction-in-progress grades are excluded by the native GetMbStageClusterGrade behavior. Reject contradictory layout/grade observations rather than filling gaps with guessed bridge records.

The native base map is a projection of NAV2 walkable decks, division footprints and authored connector graph. It is not a full 3D collision map or proof that a given actor can traverse every bridge. An edge/connector is available only when both native endpoint platforms exist. Preserve unsupported/missing mesh templates as unknown instead of inventing their geometry.

## Coordinate survey recipe

1. Start from a fresh per-platform inventory of current grade, layout, platform centers, route endpoints and source resource IDs.
2. Keep coordinate frames named: source-local, platform-local, cluster/world and mission-world are not interchangeable.
3. Compare a live read-only transform survey against the source layout transform; record maximum error and exact mission/layout.
4. For route or room proposals, include actor floor/support, platform grade and streaming owner. A route point in one mission-world FRT must not be transformed a second time.
5. Validate visibility, collision, navigation and performance as separate properties.

In one private layout-3 survey, all 28 main platform centers matched within 0.0000305 m. This supports the surveyed transform path only. It does not prove all grades, movement or route acceptance.

## Platform growth and service fallbacks

Facility eligibility must use completed grades, not upgrade targets. The service prototype catalog was limited to Command cluster 1/platform index 1 in a surveyed layout-3 base, with a minimum completed grade. Elsewhere it should report unavailable or use a smaller explicitly defined fallback. Do not silently move an actor across departments to satisfy a routine.

For any future platform, copy the workflow, not Command1's counts or dimensions. Re-inventory the platform, grade variants, construction assets, conditional story and FOB content, bridge endpoints, common props and navigation. A feature is platform-ready only after its own authored assets, source validation and bounded native observation pass.

## References

- [MotherBase Clusters reference](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/MotherBase_Clusters.md)
- [TppLocation source, pinned revision](https://github.com/TinManTex/mgsv-deminified-lua/blob/3b8d6a0487ce45f69502d40e684b3d653d3b8965/data1/Assets/tpp/script/lib/TppLocation.lua)
- [FRT format](https://mgsvmoddingwiki.github.io/FRT/)
- [Routes reference](https://mgsvmoddingwiki.github.io/Routes/)

The exhaustive layout audit and transform survey are private development evidence. The native naming rules and grade model were cross-checked against the linked source revision and local owned-game records.
