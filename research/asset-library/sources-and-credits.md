# Sources, credits and reference limits

## Ownership and attribution

Konami owns the original MGSV game models and textures shown in these references. They are not original Immersive Mother Base artwork and are not relicensed under the repository's original-code license. This visual-reference library does not distribute models, textures, game archives, decoded geometry, blends or converter binaries. It is not a finding that all reuse or redistribution of game assets is permitted.

Project owner: **arsenal-pt**. Authored plan, metadata, render/encoding/view generators and summaries: **OpenAI Codex (AI/LLM development)**. Community tools and research made the retained source work possible; that work is credited separately from the authored reference code. No endorsement or permission from upstream authors is implied.

- **Atvaark / GzsTool** and its community maintainers: the established container extraction used to prepare retained private sources. [Project](https://github.com/Atvaark/GzsTool), [community-maintained TPP fork](https://github.com/BobDoleOwndU/GzsTool). Retained special-room jobs record GzsTool 0.5.3. No fresh extraction was performed for this starter.
- **Atvaark / FtexTool**: retained FTEX-to-DDS texture conversion. [Project](https://github.com/Atvaark/FtexTool). Prior special-room conversion scripts use 0.3.3; this task reused already verified DDS variants.
- **BobDoleOwndU and FMDL Studio v2 contributors**: model-format/reader reference used by the existing source-preserving static decoder and the community interchange workflow. [Project](https://github.com/BobDoleOwndU/FMDL-Studio-v2/tree/d580b94215cc007df6c38bdb0bfce6a0f30e4701). See the repository-wide [tool credits](../../CREDITS.md) for the contributor list. This starter read retained decoded caches; it did not rerun Unity/FMDL export.
- **MGSV Modding Wiki contributors**: [FMDL/Blender workflow](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/Using_FMDL_Studio_with_Blender.md), revision2326cdf753a6fcfefb1867dd66ed97a078d4d114. Normals, transforms and interchange warnings are version-specific; this reference task does not export anything back into the game.
- **FMDL Studio author documentation**: [setup/texture-folder guide](https://github.com/BobDoleOwndU/FMDL-Studio-v2/wiki/Setting-up-Fmdl-Studio-v2/2cdaa4eefe9b8f57357e865870d902e961fb82d9), revision2cdaa4eefe9b8f57357e865870d902e961fb82d9. Preserve native texture path structure and complete FTEX sidecars during future selected conversion; the guide also distinguishes Blender version support. Cached through MGSV MCP, read 16 October 2026.
- **Blender developers / Blender Foundation**: [Blender](https://www.blender.org/), version5.2.2 for these clean offline renders.
- **Python and Pillow contributors**: [Python](https://www.python.org/) and [Pillow](https://python-pillow.org/), Python 3.14/Pillow 12.2.0 for metadata, thumbnails, GIF encoding and verification.

## What was actually checked

These three identities come from our retained source-linked Mother Base/special-room libraries, not a community filename list. Each original FMDL SHA256 matches its saved member receipt and uniquely appears byte-for-byte in the named retained FPK; that indexed model path string is also present in the FPK. The retained FPK content is hashed. The historic outer chunk3.dat origin comes from previous extraction receipts; current installed DAT membership/content/version was not checked. A loose source file alone would not establish this chain.

Source cache, selected LOD0 and sampler/texture identities were rechecked. Public records retain actual virtual paths/hashes, model/container SHA256 and the selected DDS content hashes; unidentified texture names stay null. Friendly labels/descriptions/tags are authored from native folder/scene evidence and reviewed preview appearance. The source namespace is not proof of exclusive original use.

The rendered base-color maps use actual retained DDS content and native UV0 with the established preview V mapping. Native geometry/UV inputs stay unchanged. Principled shading, studio lighting and display transforms are approximations; packed material channels, native shaders, collisions, interactions, asset animations and runtime/progression behavior are not validated. Turntables move the reference camera, not the asset.

Each entry has a clean 768px still,480px/48-frame full-orbit GIF and160px static thumbnail. No title was burned into the reference images. Clean frames and complete private verification receipts remain private. Public [catalogue](catalogue.json) and [media manifest](../../media/asset-previews/2026-10-16-seating/manifest.json) retain portable identities/output hashes without exposing private installation paths.

## Native quality continuation

The same three native FMDL inputs were read directly for LOD tables and index-buffer ranges; every one of their12face sets exactly matched the retained perLODcache. The read-only format layout was checked previously against [FMDL Studio v2's Fmdl reader](https://github.com/BobDoleOwndU/FMDL-Studio-v2/blob/d580b94215cc007df6c38bdb0bfce6a0f30e4701/FMDL-Studio-v2/Assets/Fmdl%20Studio/Scripts/Classes/Fmdl.cs), credited to BobDoleOwndU and contributors at pinned revisiond580b94215cc007df6c38bdb0bfce6a0f30e4701. All four native LODs per model differ; duplicate retained model copies map to one model identity. Existing source namespaces/where-found records are not exclusive original-use assertions.

Native FTEX and DDS headers agree on dimensions and declared mip counts for all12recorded texture channels. Three retained material manifests and native header records contain one base texture content version per selected asset; no larger retained version was found in that inspected scope. The native texture chain remains private; only metadata and rendered references are published. [FtexTool documentation](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/FtexTool.md) credits Atvaark and explains the FTEX/FTEXS-to-DDS/mip relationship. No new conversion or extraction was performed.

The [community unsolved-problems snapshot](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/Unsolved_problems.md) at revision2326cdf753a6fcfefb1867dd66ed97a078d4d114 records unresolved runtimeLODselection questions. Our own work does not measure runtime thresholds; the catalogue proves source face sets and offline references only. Exact quality/duplicate/mip metadata is in [quality-provenance.json](quality-provenance.json). The9newlower-LOD GIFs/stills and3static comparison sheets have a separate [media manifest](../../media/asset-previews/2026-10-16-seating-quality/manifest.json); original3LOD0media stay unchanged.


## Later local-tool batch (16 October 2026)

Five new references were produced by the owner's five-item run of the deterministic local pipeline; two accepted shelf-component proofs are also included. The pipeline/importer code and authored summaries were developed entirely with OpenAI Codex/AI LLMs. Existing community-format readers and GzsTool/FtexTool source preparation retain the credits above. For these seven jobs, native FMDL and DDS were already prepared privately: no GzsTool or FtexTool conversion was invoked by the retained-static adapter/importer. Native hashes, selected actual texture bindings/headers and existing media hashes were checked; [batch provenance](batch-provenance.json) preserves the resulting evidence. This does not establish native FOX material, collision, assembly or runtime-interaction equivalence.

The gntn_swtc001 namespace identifies its native source path; its observed retained container is on Mother Base. Neither fact alone proves exclusive original usage. Shelf/door/gate/duct references can be components rather than complete assemblies. Unknown outer archives and texture filenames are left unresolved.


## Whole-game metadata catalogue

[Whole-game source/coverage notes](whole-game-catalogue.md) credit Atvaark's pinned GzsTool.Core0.5.3 metadata/selective-export API. The thin wrapper reuses it directly; PFTXS metadata framing retains the original MIT notice in [THIRD-PARTY-NOTICES](../../tools/whole-game-catalogue/THIRD-PARTY-NOTICES.txt). CityHash/Zlib/Gzs binaries remain external. Authored wrapper/docs were developed entirely with OpenAI Codex/AI LLMs, under arsenal-pt's project. The scanner itself has0resolved dependencies/0previews at this checkpoint; it does not replace the existing renderer or establish vanilla/gameplay behavior.
