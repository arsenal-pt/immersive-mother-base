# Command Platform 1 — mtbs_unique_0000

This is the main, unique Command platform: the first platform in the Command cluster. It is not all four Command platforms or the entire Mother Base.

| Identity | Exact value |
| --- | --- |
| Game department / cluster | Command |
| Native cluster code / zero-based index | cl00 / 0 |
| Native plant index / player-facing platform | pl0 / Platform 1 |
| Native plant type | Special |
| Unique layout code | uq_0000 |
| Model package | Assets/tpp/pack/location/mtbs/pack_unique/mtbs_unique_0000.fpk |
| Scene / physics package | Assets/tpp/pack/location/mtbs/pack_unique/mtbs_unique_0000.fpkd |
| Native scene | Assets/tpp/level/location/mtbs/block_unique/mtbs_uni0000.fox2 |

The three additional Command platforms are native pl1, pl2 and pl3 (player-facing Platforms 2, 3 and 4). They use common-platform/division layouts and have no equivalent room/door revision here yet. Shared resources are separate: v9/v9.1 also alter 26 models in mtbs_common.fpk, and those props can affect all seven departments.

Identifiers are verified against our native extraction index and the [Mother Base clusters reference](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/MotherBase_Clusters.md). Some Lua functions use one-based indices while native functions usually use zero-based indices; do not mix them.

## What v9.1 means

v9.1 is our geometry/render experiment revision, not the game's version or the daily-life mod's release version. Earlier revisions explored doors, gray room shells, floors, original-wall reuse and a connected lower bay. v8 expanded door apertures and reverse wall coverage; v8-A removed six added wall shapes at one doorway for diagnosis. v9 tested disabling backface culling on every modeled target. Its cloned native resource paths crashed during loading.

The A/B/C/D suffixes record intermediate isolation builds. v9.1 is the final v9-E follow-up: it keeps original native resource paths and audits the no-culling mode across 439 modeled resources / 747 mesh records. It retains v8-A physics, the previous floors/openings and one shared lower bay. It does not mean completed rooms, finished physics or an engine-wide culling switch.

V9.1 loaded successfully and a short foreground test averaged 57.749 FPS. Human testing still found narrow upright entrances, lower-bay floor fall-through, missing inside-to-outside wall collision, red decals and angle-dependent rendering. Its 32 editor light planes were not registered as native lights. Treat every download here as an experimental developer reference, not a stable platform replacement.

## Version history and downloads

Each version has an immutable transformation patch, exact original-input and rebuilt-output checksums, reconstruction helper and status. These folders are included in GitHub's source download; project Releases may also package them into versioned archives. No full game archives, models, textures or Blender files are hosted here.

| Our revision | What changed | Native status / use |
| --- | --- | --- |
| [v6](versions/v6/) | all-floor gray room shells | offline-only-superseded-layout |
| [v7.8](versions/v7.8/) | original walls and shared lower bay | historical-known-native-defects |
| [v8](versions/v8/) | wider entrances and structural reverse faces | historical-known-native-defects |
| [v8-A](versions/v8-A/) | one-door added-wall collision isolation | historical-diagnostic-not-a-fixed-platform |
| [v9](versions/v9/) | all modeled assets no-culling with cloned resource paths | archived-native-load-crash-do-not-install |
| [v9-A](versions/v9-A/) | cloned resource diagnostic without common override | archived-native-load-crash-do-not-install |
| [v9-B](versions/v9-B/) | core-only cloned resource diagnostic with specialized alpha restored | archived-native-load-crash-do-not-install |
| [v9-C](versions/v9-C/) | original-path owned opaque models diagnostic | historical-subset-diagnostic |
| [v9-D](versions/v9-D/) | original-path all static opaque models diagnostic | historical-opaque-only-diagnostic |
| [v9.1](versions/v9.1/) | original-path all modeled assets no-culling (v9-E) | experimental-known-native-defects |

## Rebuild from your own game files

You need a legitimate installed PC copy of MGSV: The Phantom Pain, Python 3.10+ and bsdiff4 1.2.6. Obtain the exact 28 original packages listed in the selected manifest from your own installation with [GzsTool 0.5.3](https://github.com/Atvaark/GzsTool/releases/tag/v0.5.3). Preserve their Assets/tpp/... directory structure in a separate originals folder. Do not use an already modified 00.dat as the stock baseline.

Run these commands from the chosen version directory:

    py -3 -m pip install -r requirements.txt
    py -3 rebuild.py --originals-root "C:/YourOriginalPacks" --output-dir "C:/NewCommandPlatformStaging" --check-only
    py -3 rebuild.py --originals-root "C:/YourOriginalPacks" --output-dir "C:/NewCommandPlatformStaging"

The helper verifies every original, patch and resulting package checksum. It writes to a new staging folder only. It does not install into the game, modify saves, pack 00.dat or launch MGSV. Wrong or missing originals fail before output is written. Rebuilt files retain their existing native package paths, so no runtime platform rename is required.

These are individual package replacements, not a whole 00.dat drop-in. Installation must use a mod-manager/local build that preserves unrelated installed mods and provides backup/restore. Never copy an entire development archive over the current installation.

Switching away from v9 or v9.1 must also remove/restore their mtbs_common.fpk override. v9-A, v9-B, v9-C and v9-D intentionally rely on the original common package; retaining the old common override silently changes the diagnostic. Archived v9/v9-A/v9-B are known to crash and are preserved for reproducibility, not normal play.

## Editor-only history

All-floor v1–v5 and v7.1–v7.7 remain private Blender authoring iterations. They have no independently frozen native-package targets to reconstruct reliably. They are indexed as history rather than mislabeled as downloadable playable versions. Game-derived editor projects stay private.

## Credits and rights

Mother Base and its models, textures and scene assets are the work of Kojima Productions / Konami. This project reuses the purchaser's existing game data. It does not claim those assets as AI-generated or relicense them under GPL.

Extraction and model/scene tooling relied on [GzsTool](https://github.com/Atvaark/GzsTool) and [FoxTool](https://github.com/Atvaark/FoxTool) by Atvaark, [LbaTool](https://github.com/youarebritish/LbaTool) by youarebritish, [FtexTool](https://github.com/Atvaark/FtexTool) by Atvaark, [FMDL Studio V2](https://github.com/BobDoleOwndU/FMDL-Studio-v2) by BobDoleOwndU and its credited contributors, Blender and Unity. See [project credits](../../../CREDITS.md) for tool authors, pinned references and roles. Eligible original project tooling uses GPL-3.0-only; upstream tools and game content retain their own terms.
