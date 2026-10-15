# Rendering and collision experiments

## Reuse existing walls before adding shells

Stock structural walls were usually one-sided and did not provide dependable interior-facing visibility. In the authorized Command1 v7/v8 authoring branch, contributors duplicated/reversed faces derived from retained stock wall geometry and retired the added offset lining shells, while keeping original walls, passage components and floors. The current direction likewise removes added offset shells while preserving originals and the continuous shared lower-bay floor. This is an authoring method, not native access proof.

The authoring copy retained the source walls/floors and modeled opposing interior faces from that source geometry. Removed geometry was the added offset shell, not the original platform wall. Later interiors remain dark and empty, with render gaps, red decal artifacts and angle-dependent popping.

## Alpha render mode is an enum

The FMDL mesh alpha/draw-mode field uses NoCull value 0x20 in the audited source enum; it is an enum value, not a bit flag to OR into the previous setting. FOX2 placement records reference FMDL resources; the draw-mode value belongs to the referenced FMDL mesh data. FMDL Studio documents per-mesh alpha settings, while the exact 0x20 enum mapping here came from the project source/data audit. Replacing modes broadly can change glass, decals and other nonopaque rendering. A private diagnostic routed 439 Command1 models / 747 mesh records to that mode while preserving source geometry and UVs. Its scope did not disable engine occlusion, streaming, LOD, separate character/particle renderers or texture-only decals.

A routing audit found 182 mesh records whose original nonopaque draw modes were overwritten by the diagnostic enum. Their red/white artifacts and angle defects make the overwrite a plausible contributor, but none of those 182 records was individually proven in native play to be a decal or to be fixed by restoring its original mode. Keep original texture/material maps. Test one material class and one viewpoint at a time, compare native render modes, and record angle-dependent visibility. A no-cull pass is a visibility diagnostic, not a final material solution.

## Collision data is separate from render meshes

FOX2 collision, model GEOM, level GEOMS, navigation routes, FreeShape components, render mesh and dynamic gimmicks are different resources. A door opening in a render mesh does not make actor collision passable. A broad-phase overlap or static decoder view is not engine collision proof.

The private copied-door workflow identified target leaves through native path/hash, mesh or face identity, coordinates and parent placement. It retained frames, rails, supports, floors and non-door walls, and preserved both model and level collision. A selective edit zeroed only door-owned primitive units or split a wall quad in its plane. The independent decoder rechecked links, pointer bounds, indices, node IDs, masks, protected surfaces and positive-area blockers. The original source stayed immutable. Even a clean static result does not prove engine collision filtering, door interactions, traversal, rendering or FPS.

For FreeShape encoding, copy source shape type, vertex order, winding and native point representation exactly. A seemingly harmless reorder can flip a face or make a shape invalid. Compare each candidate point and shape against the original source record and validate serialization with an independent parser before packaging. Do not treat point-cloud proximity as source equivalence.

## Do not repeat failed geometry assumptions

These are known native failures in the tested Command1 branch: the bay floor can fall through; ordinary doorways require diving or only allow prone access; and the inside-to-outside wall collision is missing. User testing had already found the doorway and floor failures on earlier wall reuse versions; the current v9.1 branch still has floor contact, upright doorway access and inward collision defects. Offline aperture, shell, collision-source and no-overlap audits did not fix them. The v9.1 native load/render sample is bounded and does not resolve full cache/angle visibility or these physics failures.

Before editing another platform, inventory every platform-grade variant, source placement and shared-resource consumer. Test floor support, opening clearance, inside/outside visibility, material state and performance separately. Preserve all original archive members and compare exact bytes after rollback.

## References

- [FoxKit StaticModel and GeoxCollisionFreeShape guide](https://mgsvmoddingwiki.github.io/FoxKit-_StaticModel_and_GeoxCollisionFreeShape/)
- [MGSV file formats](https://mgsvmoddingwiki.github.io/File_Formats/)
- [FMDL Studio V2 per-mesh settings](https://github.com/BobDoleOwndU/FMDL-Studio-v2/wiki/Exporting-an-Fmdl)
- [Collision attributes](https://mgsvmoddingwiki.github.io/Collision_Attributes/)
- [GeomTool partial reader, pinned revision](https://github.com/Joey35233/GeomTool/blob/4e4b300444e5e0cca85b5113249b76d88d9a55f1/Program.cs)

The collision observations above combine private source decoders and native gameplay failures. The exact NoCull value came from project source/data inspection; the public FMDL Studio docs below describe per-mesh alpha settings but do not publish this exact enum table. Community collision references are partial and do not document the complete native aggregate collision writer.



