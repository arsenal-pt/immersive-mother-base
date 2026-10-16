# Verified animation source handoff

## Browsing correction - 16 October 2026

The browsing column is **Description**. Every current clip has a short useful action summary, authored from its retained source family/phase and already reviewed offline preview unless an exact verified external description exists. Community-source match status stays in detail/JSON data; a missing community match does not replace the browsing summary with unavailable filler. Browse tables omit the Credits column; central credits, per-entry detail credits and source attribution remain intact.

Tags are semantic search terms, for example CQC, Snake, enemy soldier, light machine gun, reload and kneeling. Keep provenance, uncertainty and review status in separate fields. A source actor/family label is distinct from the stock Ocelot preview mesh. Do not invent a Quiet origin, named character or specific weapon from the reference model; unsupported actor/weapon identities remain unset.

## Extraction-backed locations

The [retained asset map](container-provenance.json) now checks each of the three original FPK indexes directly: the declared MTAR path points to bytes identical to the retained MTAR and its SHA256. All 27 selected GANI payload hashes match bytes within their exact MTAR; saved extraction XML paths (only the tool-added four-digit prefix removed) and retained dictionary identity support the virtual names. No ordinal-only identity is used.

Our saved Gzs/MtarTool outputs and source bytes are first-party extraction evidence. Community descriptions are separate interpretation sources and are not location evidence. The outer FPK virtual path and DAT name remain historical saved-extraction origins: the enclosing DAT index, current contents and current version were not checked. Keep those fields explicitly qualified, and leave unsupported locations null.

For every future extraction, capture this provenance during extraction: source archive/version and content hash, exact outer DAT/FPK and inner MTAR/GANI paths where actually evidenced, tool/dictionary revision and hash, selected member/payload hashes, index/log receipt hashes and an explicit verification status for each link. Reuse exact retained bytes where possible. Check a selective retained index/member; do not launch a whole DAT extraction merely to fill a label.

Reviewed 15 October 2026 for the existing 27 library clips and MGSV MCP documentation. The author documentation below has not been tested in this review.

## Sources and credits

Both supplied sources resolve to **chocmake/chocmake.github.io**, pinned at commit `2301912bd8694e5abd81044b0e9b15c811cb5772` (6 June 2026). Credit **choc / chocmake** for [Adding Player Motions](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1151), last edited 5 June 2026. Credit **BobDoleOwndU** for [BossQuiet2_layers notes](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/files/gani-descriptions/BobDoleOwndU/BossQuiet2_layers.txt), as identified in the [guide's resource table](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1589). Retain **KnochenGott** for the supplied enemy-animation workbook, with attribution explicitly marked user-provided.

The guide blob is `d057a583ed08cddf3bad992318cb6eb3279a054d`; the notes blob is `cc849df018389da78f0d5f76f224eedec174d63e` (12,852 bytes). No applicable guide/description redistribution license was verified. Link and summarize briefly; do not copy the guide or entire notes list.

## Matching result and metadata columns

The supplied notes have 122 raw path/index mappings, numbered 0–121, dated 5 June 2026. Comparing them with the [27-record library snapshot](https://github.com/arsenal-pt/immersive-mother-base/blob/fdff82ed1a28dfd698a351c2008c7252840582b3/research/animation-library/catalogue.json) gives **zero exact virtual-path matches and zero basename matches**. Do not populate any current clip with a BossQuiet description. The notes contain no archive hash or clip payload hashes, so they also cannot establish cross-archive binary equivalence.

Use separate fields for:

- **Category:** the current reviewed group.
- **Tags:** retrieval labels whose basis remains naming or offline observation.
- **Virtual GANI directory:** the parent of the exact source member path, clearly labelled as a logical asset directory.
- **Container location:** DAT → FPK → MTAR, only where evidence exists for that record; otherwise unknown.
- **Description:** distinguish a short authored observation from an attributed community description. Keep community source, author and match status alongside it.

Match archive/version and exact member path/hash evidence before using an upstream description. The comparison removed only the four-digit MtarTool prefix from the raw note's filename and normalized an optional leading slash; it retained all other path spelling and case. Ordinals or short identifiers alone are insufficient. The guide warns that archive variants can differ and even an otherwise unchanged repack can reorder members. [Mapping instructions](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1686), [original-order warning](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1738).

The notes identify **only their own source** as `chunk2.dat` → `Assets/tpp/pack/mission2/story/s10050/s10050_area.fpk` → `Assets/tpp/motion/mtar/bossquiet2/BossQuiet2_layers.mtar`. That chain is not a deployment location and must not be assigned to the current CQC/LMG records. [Notes location header](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/files/gani-descriptions/BobDoleOwndU/BossQuiet2_layers.txt#L1).

## Lessons for MGSV MCP documentation

The guide separates the FPK load list from the GANI playback list. Runtime GANI references require a leading slash and `.gani`; preserve extensionless catalogue/hash paths separately rather than mutating them. Grouping can organize intro/middle/outro clips, but does not verify transitions or pairing. [Configuration](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L924).

Usage differs between Infinite Heaven and the alternative unknown321 motions mod. IH uses its Motions menu and configurable Quick Menu commands; alternative bindings are not universal IH controls. Hold can loop supported clips or leave others frozen on their final frame. These are documented player-playback features, not ordinary NPC compatibility or native acceptance. [Usage](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1151).

Troubleshooting checks package availability, exact GANI paths, configured group lists, dictionary entries and MTAR XML/member consistency. The guide says missing custom dictionary paths may still produce a packed MTAR with alternate hashed names, so packing success alone is insufficient. No rule about base-versus-layer decoding is established by this guide or by the `_layers` filename. [Troubleshooting](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html#L1458).

No extraction, rendering, game launch, install, bulk workbook import or native test was performed. Source labels and identifiers remain documentation evidence, not gameplay proof.
