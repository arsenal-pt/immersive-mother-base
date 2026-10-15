# LMG ready/reload candidates — batch002

This section adds **two new source clips**, both actual identified `enetmgn` members in the preserved stock `Soldier_common` archive. It is the tied smallest supported humanoid section in the supplied workbook: LMG and Sniper each list2 entries; source-column order selected LMG. The batch stops at these2 rather than adding another category to reach25.

| Exact clip identifier | Plain-English offline view | Hash ID | Raw frames | Detail |
| --- | --- | --- | ---: | --- |
| enetmgn_q_rdy_rld | Kneeling LMG reload candidate |313cdbcc7c1d9|337|[Open clip](../../animation-library/clips/mgsv-tpp-soldier_common-313cdbcc7c1d9.md)|
| enetmgn_s_rdy_rld | Standing LMG reload candidate |380f6573688d2|337|[Open clip](../../animation-library/clips/mgsv-tpp-soldier_common-380f6573688d2.md)|

[Browse this category](../../animation-library/tables/lmg-reloads-1.md) · [Still images](../../animation-library/tables/lmg-reloads-1-stills.md) · [Exact extraction records](animations-metadata.json) · [Preview manifest](../../../media/animation-previews/2026-10-15-lmg-reloads/preview-manifest.json) · [Category progress](../../animation-library/category-progress.json)

## Defined coverage and stop condition

Coverage is **Sheet1 L4:L5 in the supplied enemy animation workbook** (SHA256 `849e9052875866d392354ab856df8c77c0f794fa83ed422d190a07b1741ad7cd`) plus the two identified `enetmgn` matches in the1345-member stock `Soldier_common.mtar` (SHA256 `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e`). Both are now extracted/catalogued and previewed offline: previously catalogued0, new2, remaining0, next cursor none. This does not establish all LMG animations in every archive/version, identify unresolved names, or authorize another category. The ledger preserves exact completed IDs, exclusions and source scope for later expressly assigned batches.

## Executed method

The starting input is the immutable MTAR preserved by the earlier stock extraction. Actual community MtarTool0.2.7 unpacked a copied archive; both selected GANIs and all available EXCHNK/ENCHNK companions match the immutable full-library ZIP. Shared TRK/CHNK layouts and original MTAR/XML remain private. This batch did not freshly extract DAT/FPK packages or reconvert the model. Future batches should reuse exact hash-verified retained members, including the private ZIP, instead of repeating whole-container extraction unnecessarily.

The proven [full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) and original renderer were reused with the unchanged stock Ocelot weighted character, community mctrollin rig/mappings and standard Blender skinning. The kneeling sample was reviewed before integration. Each337-frame clip has170 clean PNGs including a separate endpoint; GIFs sample169 frames in0..336 and last11.23s at the **chosen30 source frames/s**, nominal15 GIF FPS. Native FPS remains unknown. The fixed camera fits every evaluated integer-frame mesh position; root travel is retained. Clean originals stay private.

[Encode-LMG-Previews.py](Encode-LMG-Previews.py) adapts the existing authored encoder for an explicit1–25 source count and this category's labels. Final GIFs use256-color MEDIANCUT palettes without dithering and delta encoding; every decoded composited frame was checked pixel-for-pixel against its quantized clean/captioned source, plus loop/frame-count/delay checks. This changes storage, not movement or timing. Large GIFs are shown only on individual detail pages; the category table loads two small previews. Thumbnails preserve each source's actual aspect ratio; the earlier25 previews/records remain unchanged.

## Interpretation and credits

The visible figure is an **untextured stock Ocelot reference model, with no held LMG**. Names and the supplied category support ready/reload interpretations; offline images support kneeling/standing posture labels. They do not prove native reload mechanics, weapon handling/contact, actor compatibility or game playback. Native Fox cloth/twist/physics is not reproduced; the established18 secondary-bone ancestor fallbacks remain disclosed. No game launch, live installation, native test, source motion edit or procedural limb animation was performed.

Original assets/animations: **Konami / Kojima Productions**. Workbook discovery credit: **KnochenGott**, explicitly supplied by the human; the workbook and unrelated rows/descriptions are not redistributed. [choc/chocmake's guide and credited note authors](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html) remain a pinned reference, not new gameplay evidence. Community tools: **BobDoleOwndU / MtarTool**, **mctrollin / MTAR reader, rig and mappings**, **FMDL Studio v2 / BobDoleOwndU and contributors**, **Atvaark / GzsTool**, Blender and Pillow. Authored pipeline/library glue developed using **OpenAI Codex** under **arsenal-pt**'s direction. See [credits](../../../CREDITS.md), [references](../../animation-library/references.md) and [license scope](../../../LICENSE-SCOPE.md). Raw game animations, models, scenes, installed tools and workbook remain private.
