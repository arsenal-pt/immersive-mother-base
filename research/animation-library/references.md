# Animation research references

Reviewed 15 October 2026. These sources support discovery and attribution. Community descriptions and matching names do not establish native playback, timing, rig compatibility or paired contact.

## Community motion notes

[Adding Player Motions](https://chocmake.github.io/guides/mgsv-adding-player-motions/#resources) by **choc / chocmake** collects motion descriptions and explains matching numeric indices to GANI paths. Its resource table credits individual note authors, including **BobDoleOwndU, choc, amars464 and Shigu**. Preserve per-note credits when using a particular list. Reviewed source: [commit `2301912`](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html), guide last-edited date 5 June 2026.

The guide pairs internal GANI order with filenames known when an archive was unpacked. It identifies different `player2_resident` ordering between `chunk0.dat` and `00.dat`/`01.dat` variants, and explains that dictionary updates can change resolved paths. Future cross-references should retain the exact archive/version, original numeric index, resolved path and dictionary revision together. This recommendation follows the [guide's resources and matching instructions](https://github.com/chocmake/chocmake.github.io/blob/2301912bd8694e5abd81044b0e9b15c811cb5772/guides/mgsv-adding-player-motions/index.html).

## Supplied enemy-animation workbook

**KnochenGott** is credited for the supplied `enemyanimation.xlsx`, as explicitly identified by the user. That attribution is user-provided and has not been independently established from a public author page. The workbook remains private and is not bundled or reproduced here.

A bounded read-only review found one worksheet, `Sheet1`, with stored extent `B1:AP725` and category/code headings for weapon, posture, vehicle, dog and zombie motions. Its 724 nonempty worksheet row records are **not a verified animation-entry count**. No whole-list import, description copying, matching against the current 25 clips, extraction or preview generation was performed. Source identity: 28,268 bytes; SHA-256 `849e9052875866d392354ab856df8c77c0f794fa83ed422d190a07b1741ad7cd`, unchanged after review. These are workbook observations, not tested motion behavior.

## Additional supplied reference

[Nexus Mods reference 2531](https://www.nexusmods.com/metalgearsolidvtpp/mods/2531?tab=description) is retained for follow-up. Its description page could not be retrieved during this review, so its title, author, contents, version and reuse terms have not been verified. No capability or authorship claim is inferred from the link.

## Next selected research

After the user chooses and approves a small motion set, identify its exact source archives and compare only selected identifiers with community notes or the workbook. Keep community descriptions attributed and separate from observed motion labels. Apply the existing full-character preview workflow and record native testing separately. Expanding the workbook into a catalogue or extracting a broader animation set remains future work.


## Batch002 selected source matching

The authorized next section matches only the supplied workbook's LMG cells Sheet1 L4:L5 to actual enetmgn_q_rdy_rld/enetmgn_s_rdy_rld archive members. KnochenGott attribution remains human supplied; the workbook stays read-only/private and no unrelated rows/descriptions are imported. See the [defined coverage/receipt metadata](../animation-batches/lmg-reloads/README.md) and [category ledger](category-progress.json). Source names are interpretation leads; native weapon mechanics/contact/timing remain unproved.

## Descriptions and metadata provenance

Read [verified description sources and matching rules](description-sources.md) before enriching an entry. The supplied BobDoleOwndU BossQuiet2_layers notes have zero virtual-path or basename matches among the current 27 clips; community description text/author stays unavailable for those entries. Authored categories, retrieval tags and preview summaries are separately credited, with exact source GANI locations and recorded MTAR/pack labels. The [source-review registry](metadata-source-review.json) retains pinned source identity and the empty exact-match set; unknown full container paths stay unrecorded.

The [container provenance map](container-provenance.json) records historical DAT origins and exact virtual FPK/MTAR paths for the three archive hashes used here, verified from retained source receipts, successful extraction logs and matching immutable ZIP members. These are source locations, not deployment instructions or current-install verification; missing evidence remains unrecorded.
