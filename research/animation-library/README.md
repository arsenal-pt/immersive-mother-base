# MGSV Animation Reference Library

A visual reference for researching animations in **Metal Gear Solid V: The Phantom Pain**. Browse **28 decoded clips** across explicitly scoped categories, with exact source identities, larger GIF views and complete technical records.

**This index loads no GIFs or thumbnails.** Expand a category and choose a table page. Each animated table loads **at most four small GIFs**; still-image pages run no animations. Click a preview or title to open one larger clip. No mod, dashboard or running game is needed.

[All data (JSON)](catalogue.json) · [Spreadsheet data (CSV)](catalogue.csv) · [Additional animation references](references.md) · [Research plan](RESEARCH-PLAN.md) · [Extraction research](../mtar-punch-combos/README.md)

## Browse by section

The largest current animated page contains 3.00 MiB of thumbnail files. Separate pages bound the number of animations loaded; collapsed HTML sections alone do not guarantee that images are deferred.

<details>
<summary><strong>Snake CQC combo and transition candidates</strong> - 11 clips</summary>

| Page | Clip range | Animated table | Still-image table |
| --- | --- | --- | --- |
| 1 | `snapcqc_s_com_f1_ed` to `snapcqc_s_new_com_asr_b3` | [Open 4 GIFs](tables/snake-cqc-1.md) | [Open stills](tables/snake-cqc-1-stills.md) |
| 2 | `snapcqc_s_new_com_asr_f1` to `snapcqc_s_new_com_asr_f4` | [Open 4 GIFs](tables/snake-cqc-2.md) | [Open stills](tables/snake-cqc-2-stills.md) |
| 3 | `snapcqc_s_new_com_asr_b1` to `snapcqc_s_new_com_asr_f5` | [Open 3 GIFs](tables/snake-cqc-3.md) | [Open stills](tables/snake-cqc-3-stills.md) |

</details>

<details>
<summary><strong>NPC receiving and reaction candidates</strong> - 8 clips</summary>

| Page | Clip range | Animated table | Still-image table |
| --- | --- | --- | --- |
| 1 | `enemasr_s_new_com_asr_b1` to `enemasr_s_new_com_asr_f1` | [Open 4 GIFs](tables/npc-receivers-1.md) | [Open stills](tables/npc-receivers-1-stills.md) |
| 2 | `enemasr_s_new_com_asr_f2` to `enemasr_s_new_com_asr_f5` | [Open 4 GIFs](tables/npc-receivers-2.md) | [Open stills](tables/npc-receivers-2-stills.md) |

</details>

<details>
<summary><strong>Special / zombie actor candidates</strong> - 6 clips</summary>

| Page | Clip range | Animated table | Still-image table |
| --- | --- | --- | --- |
| 1 | `snapzmb_s_atk_pnh` to `enetzmb_s_atk_pnh` | [Open 4 GIFs](tables/special-actors-1.md) | [Open stills](tables/special-actors-1-stills.md) |
| 2 | `enetzmb_s_atk_pnh2` to `enetzmb_s_atk_pnh_ed` | [Open 2 GIFs](tables/special-actors-2.md) | [Open stills](tables/special-actors-2-stills.md) |

</details>

<details>
<summary><strong>LMG ready/reload candidates</strong> - 2 clips</summary>

| Page | Clip range | Animated table | Still-image table |
| --- | --- | --- | --- |
| 1 | `enetmgn_q_rdy_rld` to `enetmgn_s_rdy_rld` | [Open 2 GIFs](tables/lmg-reloads-1.md) | [Open stills](tables/lmg-reloads-1-stills.md) |

</details>

<details>
<summary><strong>Ocelot-package locomotion references</strong> - 1 clips</summary>

| Page | Clip range | Animated table | Still-image table |
| --- | --- | --- | --- |
| 1 | `oce0_s_wlk_a` | [Open 1 GIFs](tables/ocelot-locomotion-1.md) | [Open stills](tables/ocelot-locomotion-1-stills.md) |

</details>

## Metadata columns

Browsing tables separate **category**, **semantic tags**, **virtual GANI directory/file**, **MTAR/container location** and **Description**. Credits remain central and per-entry in the detail/source data. Every entry has a concise action description; authored observations stay separate from attributed community descriptions and their exact-match status. The reviewed BossQuiet2_layers notes match none of the original 27 paths. The walking reference uses a separately credited authored observation. Read [description sources and matching rules](description-sources.md), the [machine-readable source review](metadata-source-review.json) and [retained container provenance](container-provenance.json).

## How to read the previews

The visible figure is untextured stock Ocelot, used as a full-character reference for original Snake/NPC source motions and the separately pinned Ocelot-package walking reference. All are **offline previews**. Durations use a chosen 30 source frames/s; native timing is unmeasured. Labels retain candidate, receiver, transition and special-actor distinctions. Individual clips have no matched partner or held weapon, and hair/clothing motion is approximate.

Each detail page includes source archive and exact clip path, hash ID, frame counts, sidecar/payload hashes, role confidence, chosen preview timing and verification limits. Complete extraction/render records are in JSON; CSV supplies common searchable columns. Stable library IDs use game + archive + clip hash. Older extraction ordinals remain historical fields because repacking can renumber them. JSON media paths are relative to the repository root.

The [original expanded gallery](../mtar-punch-combos/gallery.md) remains available for historical reference; it can load more full-size animations at once.

## Category coverage

The [category ledger](category-progress.json) records the selected source version/list, completed IDs, remaining IDs and next cursor. The current LMG ready/reload section has two identified entries. Completing that defined scope does not establish all-game LMG coverage. Stop at the selected category boundary; do not add another category to fill a batch cap.

## Reuse and future expansion

This is general MGSV animation research hosted in Immersive Mother Base. It does not depend on the mod's simulation or Infinite Heaven. Future sets can cover idle actions, locomotion, duties, services, training and reactions, including movements unrelated to Mother Base.

A separate animation-library project is a **future direction**, not a second repository created by this update. Portable JSON/CSV, stable IDs, individual clip pages and explicit media paths support a later move while preserving provenance, credits and evidence limits. Coverage is scoped to identified source versions/lists, not every animation in the game.

Follow the [bounded research plan](RESEARCH-PLAN.md) and [preview workflow](../animation-preview-workflow.md). Reference names from a guide or spreadsheet are discovery leads, not proof that a clip has been extracted, previewed or tested. See [reference notes](references.md) for the additional sources and their scope.

## Rebuilding

The existing extraction catalogue and preview manifest are the input records. Do not hand-edit generated tables, pages, CSV, JSON or thumbnails. With Python 3.10+ and Pillow 12.2.0 installed, run from the repository root:

```console
python research/animation-library/build-library.py
python research/animation-library/build-library.py --check
# Metadata changes only: preserve existing reviewed media
python research/animation-library/build-library.py --metadata-only
python research/animation-library/build-library.py --metadata-only --check
```

This reads existing reviewed GIFs, deterministically downscales their composited frames, retains loop and total display duration, and writes only library documentation and new thumbnails. The full-size GIFs and original metadata stay unchanged. New batches need explicit input registration/group labels in the builder. The --metadata-only option reuses hash-verified existing thumbnails and writes no media. No raw game files are copied, no game is launched, and research media stays outside software packages.

## Credits and scope

Original game assets/animations: **Konami / Kojima Productions**. Community motion decoding, reference rig and mappings: **mctrollin**. Model conversion: **FMDL Studio v2 / BobDoleOwndU and contributors**. Supporting tools include GzsTool, MtarTool, Blender and Pillow. See [full credits](../../CREDITS.md), [additional source credits](references.md) and the [executed recipe](../mtar-punch-combos/full-character-preview-recipe.md).

Created under **arsenal-pt**'s direction; original library code/documentation were developed using **OpenAI Codex / AI LLMs**. Contributions and corrections are welcome. Eligible original work follows [GPL-3.0-only](../../LICENSE); rendered game-derived media retains its [asset scope](../../LICENSE-SCOPE.md). No raw model, rig scene or animation payload is included.
