# Extraction and model editing pipeline

## Preserve source identity before editing

Keep source originals immutable. An editable scene should preserve native resource path, source hash, mesh/submesh identity, source vertex indices, UVs, materials, transforms, LOD membership and references to linked source libraries. Make edits in a clearly named copy and keep a manifest mapping each changed instance back to its original path and hash. Do not commit extracted models, textures, archives or complete game resource collections.

For reusable models, maintain one canonical source library and build derived platform views from it. If a placement needs a unique affine correction, keep it as an explicitly mapped derived mesh and retain an inverse/source mapping. Do not bake placement-space vertices back into the canonical source buffer. Refresh derived instances from the edited library; avoid rerunning an extractor that would overwrite authored changes from stock cache.

## Coordinate and UV conventions

The tested coordinate conversion is native (x, y, z) to Blender (x, -z, y); the inverse is Blender (xb, yb, zb) to native (xb, zb, -yb). This direction is corroborated by the FMDL Blender exporter conversion at its pinned source revision, and the project-specific door roundtrip independently matched 192 positions, 124 triangles and UV0 by native vertex identity. Placement is stored in native scene records and is separate from the source vertex buffer. Keep UV orientation tied to the native mesh, not world axes. Compare positions, triangle order and UV0 by native vertex identity after import/export.

The community FMDL Studio path imported stock assets into Unity, but one ordinary export/reimport changed UV/metadata and collapsed four LOD levels to one. For a fixed-topology, fixed-count model, a constrained native source-template writer achieved no-edit byte identity and a 1 mm interior vertex change affecting three bytes; Blender mapping reproduced the tested door model's 192 positions, 124 triangles and UV0. This is narrow evidence for that parsed layout and topology. It is not a general FMDL writer or whole-platform export path.

## Reproducible round-trip checks

For a candidate model:

1. Record original resource path and SHA-256 and parse all stream offsets, counts, formats, bounds and LODs.
2. Import into a disposable editor copy and preserve native vertex index as an attribute.
3. Export without edits and require byte identity where the writer claims preservation; otherwise compare every preserved field explicitly.
4. For an edit, constrain topology and selected vertices; compare untouched streams byte-for-byte.
5. Reopen the saved scene independently and compare positions, UVs, normals/tangents, bounds and mesh/material assignments.
6. Rebuild only copied native resources and validate archive references and package manifests.
7. Keep native load, visibility, collision, navigation and performance as later gates.

The tested editable library contained 984 source models and 3,432 submeshes. A writer-layout scan accepted 806 model paths but only 1,467 submeshes; many large building sources were rejected. Do not describe this writer as complete coverage.

## Archive and resource preservation

Preserve archive membership, names, flags, order-sensitive metadata and unmodified payload bytes. Hash both source and reconstructed outputs. Keep native paths when possible; aliases can affect dependency resolution and streaming. If an archive reader emits hashed names for unknown entries, validate them against the full native path hash before use. A payload hash is not a resource identity by itself.

Source inventories and linked libraries may include copyrighted game data. Publish authored scripts and original explanations only, with upstream format/tool links. Keep extracted binaries, Blender scenes with embedded originals, converted textures and save data private.

## Upstream tools and references

- [FoxKit](https://mgsvmoddingwiki.github.io/FoxKit/)
- [FMDL Studio V2](https://mgsvmoddingwiki.github.io/FMDL_Studio_V2/)
- [FMDL Studio with Blender](https://mgsvmoddingwiki.github.io/Using_FMDL_Studio_with_Blender/)
- [MGSV file formats](https://mgsvmoddingwiki.github.io/File_Formats/)
- [FMDL Blender exporter coordinate conversion, pinned source revision](https://github.com/the4chancup/pes-fmdl-blender/blob/231093d/pes-fmdl/IO.py#L3345-L3357) — used as a converter reference; project-specific mapping was independently roundtrip-checked.
- [GzsTool hashing source, pinned revision](https://github.com/Atvaark/GzsTool/blob/384cb81155ada82716c21b95035b5306b1c0d9cf/GzsTool.Core/Utility/Hashing.cs)

Private development evidence: editor-file workflow, native round-trip validation and special-room inventory. Private asset files and reports are excluded.


