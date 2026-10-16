# Whole-game catalogue: implemented metadata census, previews next

The [local whole-game catalogue tool](../../tools/whole-game-catalogue/README.md) now walks a configured MGSV installation and indexes its archive members without AI, MCP, a server or network during ordinary runs. This expands discovery beyond the separate prepared149-model preview index. It uses installed community readers rather than a new archive converter.

**Catalogue records are not rendered assets.** Outer archive membership is implemented; nested-container discovery, dependency resolution and previews have separate progress states. This does not establish every nested model, a vanilla installation or effective game/mod load priority.

## Verified offline snapshot - 16 October 2026

| Work | Recorded result | What it establishes |
|---|---:|---|
| Whole-root filesystem census |614files|Includes protected/runtime/backup exclusions; not every file is an asset |
| TPP master outer archive indexes |19QAR /178,512member occurrences|Metadata only, including nested update directories |
| MGO outer archive indexes |2QAR /23,791member occurrences|Separate source scope retained |
| Total indexed outer membership |21QAR /202,303occurrences|Occurrences include duplicates and alternatives, not202,303unique models |
| Unresolved outer names / extensions |59,605 /18|Unknown hashes/types are retained rather than guessed |
| Selected nested proof |1FPK /5embedded records|4HTRE and1FMDL member; child payloads were not extracted |
| Remaining nested queue |43,596containers|Still pending; not ready-to-render assets |
| Scanner dependency-resolved / previews |0 /0|The renderer bridge is not implemented |

The single native proof selectively decoded one stored80,776-byte FPK to150,208bytes using the existing library, then read its inner metadata. Repeating that completed selection launched zero helpers/decodes. The five child payload content hashes remain unknown. Full-archive content hashes were not computed. Other FPKD/SBP/PFTXS branches have authored-fixture coverage only; native proof here covers QAR tables, selected QAR-to-FPK decoding and FPK tables.

The **separate retained preview queue** still covers149model versions, with8completed at this snapshot. The public visual library has10parent references/19rendered views (including earlier seating research outside that queue). None of those counts means the whole-game scanner has produced previews.

## Use and resource limits

Follow the [setup/requirements](../../tools/whole-game-catalogue/README.md#setup-and-run): Windows, Python3.11+, installed GzsTool0.5.3/DLLs/dictionaries, private paths in config, and the Windows .NET Framework compiler for the thin helper. Raw game/tool binaries are not bundled.

Index-Game-Assets.cmd performs the filesystem census and outer metadata indexing, prints coverage and asks for nested-container count. Default0 performs no nested decode. A positive count or explicit all processes unfinished **container attempts**, subject to per-command I/O, timeout, memory, cache and free-space budgets. It does not request that many rendered models. Remaining containers resume on later runs; successful cached work does not use the allowance. Unsupported/failing entries keep reasons and finite retry rules.

Default limits are256MiB per declared/decoded container,1GiB combined raw cache/partials,2GiB logical read budget,2GiB free-space reserve,180seconds per helper and1.5GiB child-memory watchdog. Existing codecs can allocate whole buffers; failed or killed work stays incomplete. Cancellation is supported; hard-crash lock/child recovery remains manual. Operational SQLite, staged bytes and large sanitized CSV/SQLite exports stay local, outside the public repository.

## Next deterministic bridge (pending)

1. Select next unfinished unique discovered FMDL/content candidate in an explicit asset-count budget; preserve all source occurrence chains and alternatives.
2. Selectively stage only that exact model, verify its current source/ordinal/range and actual content SHA, then reuse the existing native reader for layout, hidden/skinned groups and native LOD eligibility.
3. Resolve real material sampler/path hashes to the exact FTEX header and required numbered sidecars. Missing or ambiguous matches remain unresolved; filename similarity is insufficient.
4. Invoke installed FtexTool on the complete supported texture family, verify actual DDS/native dimensions/mips and hashes, then automatically feed the existing static renderer queue without per-asset agent recipes.
5. Reuse the existing Blender/Pillow, provenance/cache/cancel and sanitized reference export stages. Prove one compatible discovered static model with its textures, repeat-cache reuse and bounded next-N continuation before expanding.

FOVA/character assembly, compatible animation rigs/MTAR playback, FOX shader fidelity and native gameplay remain separate capabilities. Indexed MTAR/GANI/type names do not establish clip enumeration or animation previews. No new production extraction or render is implied by this plan.

## Primary sources and credits

**Atvaark and GzsTool contributors** provide the existing archive readers/selective decode API, pinned to [GzsTool0.5.3, fc4a8196](https://github.com/Atvaark/GzsTool/tree/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5). The stock [CLI exports every member](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool/Program.cs#L110-L133); the thin local wrapper instead calls metadata readers and selected exports. [QAR read](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Qar/QarFile.cs#L32-L104), [FPK read](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Fpk/FpkFile.cs#L29-L58), [selective QAR export](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Qar/QarEntry.cs#L133-L167).

The upstream [PFTXS reader eagerly materializes payloads](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Pftxs/PftxsFtexFile.cs#L38-L67). The small attributed metadata framing adapter uses its public entry reader and seeks past payloads. The [original MIT notice](../../tools/whole-game-catalogue/THIRD-PARTY-NOTICES.txt) is preserved; external CityHash/Zlib/Gzs binaries retain their own licenses and are not redistributed. The wrapper also distinguishes upstream's reversed [QAR size-property labels](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Qar/QarEntry.cs#L274-L308): exported stored_size, declared_decoded_size and actual_size are different evidence. Filename hashes/MD5 are not payload content hashes.

The later texture bridge will reuse [Atvaark/FtexTool](https://github.com/Atvaark/FtexTool), the existing source-preserving static reader/community format research, Blender and Pillow; see [central library credits](sources-and-credits.md). Konami owns original game assets. arsenal-pt owns this project; the authored tools/docs were developed entirely using OpenAI Codex/AI LLMs. No original game payloads, installed binaries, large catalogue databases or preview caches are uploaded here.

The implemented tool's14focused authored-fixture tests passed independently under root review. The real offline findings above are explicitly separate from fixture coverage and gameplay proof. Source preparation and the next bridge remain active development; contributions are welcome.
