# Install and restore — 0.1.0-alpha.1

This download installs the regular-soldier daily-life **alpha foundation**, with one Immersive Mother Base menu in Infinite Heaven. It excludes our experimental IH-extra NPC adoption. Group/service/CQC resource-dependent actions are unavailable; this is not the completed living-base roadmap or a new native gameplay/FPS acceptance claim.

## Requirements

- Windows and a legally obtained MGSV TPP installation.
- Separately installed [Infinite Heaven](https://www.nexusmods.com/metalgearsolidvtpp/mods/45) and [IHHook](https://www.nexusmods.com/metalgearsolidvtpp/mods/1226), using their matched upstream instructions and prerequisites (including the required Visual C++ x64 runtime).
- [Python3.10 or later](https://www.python.org/downloads/windows/). The installer and companion use the standard library; no Python package installation is needed for the core.

The reviewed external Lua interface is IH r267. Local native history used game1.0.15.4 and a repaired IHHook r25 build. Other combinations are not certified by structural checks. See [DEPENDENCIES-AND-COMPATIBILITY.md](DEPENDENCIES-AND-COMPATIBILITY.md), including the known stock-r25 pipe/performance issue. No executable/hook/framework is bundled or automatically downloaded.

## Install the core

1. Download **core.zip** from [the versioned release](https://github.com/arsenal-pt/immersive-mother-base/releases/tag/v0.1.0-alpha.1). Extract the whole ZIP to a regular local folder such as Downloads; do not run inside the ZIP or through a symlink/junction/cloud placeholder.
2. Close MGSV. Back up the existing `mod` folder and saves. Use a clean test setup for the alpha; if `mod/modules/NpcIHStaff.lua` from our old private experiment is present, the installer refuses before writing. It never deletes or disables that adapter automatically.
3. Double-click **Install.cmd**, then select your existing `MGS_TPP` folder containing `mgsvtpp.exe`. Alternatively, run the commands below. The installer verifies all20owned Lua payloads and prerequisites, records backups and installs only those filenames. It never starts the game.
4. On a normal Mother Base visit, open **Immersive Mother Base** in IH. Check availability first. Ordinary soldier needs, identities, hierarchy, native patrol and diagnostics are the supported source scope. Do not flip disabled proof flags to enable missing services/training.

```powershell
python -B installer/install.py check --game-dir "D:/Games/MGS_TPP"
python -B installer/install.py install --game-dir "D:/Games/MGS_TPP"
```

IH auto-discovers the six owned modules in `mod/modules`; no IH source/menu-list edits are required. Fourteen helpers go in `mod/nlab`. The browser server, extra actors, experimental SDK and platform geometry are not installed by this step. The PE/framework/hook presence check detects structural prerequisites; it does not certify purchase, DRM, the VC++ runtime or native compatibility.

## Uninstall or recover

Close MGSV and run **Uninstall.cmd**, or:

```powershell
python -B installer/install.py uninstall --game-dir "D:/Games/MGS_TPP"
```

Only the recorded installation is removed. Original overwritten files are restored; previously absent owned files are removed. Repeat installs/upgrades preserve the earliest originals. Edits made after installation cause a refusal rather than being erased. Unrelated files, saves, runtime needs/ranks/recordings and backup history remain.

Receipts/backups are under `mod/imb-install-backups/<version>/<id>/`. Keep them until uninstall is complete. For an interrupted transaction, follow [installer/README.md](installer/README.md) and its explicit `restore --receipt` command. This journaled recovery is hash-guarded; there is no blind destructive force mode.

## Optional companion

Extract **companion.zip**, open its `companion` folder and run:

```powershell
python -B server.py --mod-root "D:/Games/MGS_TPP/mod" --game-exe "D:/Games/MGS_TPP/mgsvtpp.exe"
```

Open http://127.0.0.1:8785. It is loopback-only, never launches the game and displays the core's snapshots/mailboxes. It does not calculate a second simulation. Follow [companion/README.md](companion/README.md) for configuration. Stop with Ctrl+C; removing this extracted companion copy uninstalls it without changing saves/core. Missing/stale native data makes actions unavailable. Without separately supplied local deck data, the map shows observed coordinates on a grid, not a complete minimap.

## Optional Command Platform1 geometry

Extract **command-platform-1-history.zip** and follow [Command Platform1](platforms/command/platform-1/README.md). Select a revision deliberately; **v9.1/v9-E** is the current historical experiment. Some earlier variants crashed on load and are archived diagnostics. All retain their own known defects/evidence.

Rebuild from the exact stock packages extracted from your legally obtained game. Per-input, patch and output hashes are checked; unsupported or previously modded sources are rejected. The helper writes new staging output only. To test the resulting resource replacement, build a local `.MGSV` with external MakeBite and install/uninstall through SnakeBite, preserving current mods and backups. Do not copy FPK files straight into the game root. The core installer never changes game archives or installs these platform overrides.

Native target **Command Platform1 / cl00/pl0 / mtbs_unique_0000** is precise; the other three Command platforms remain unedited. Shared common-prop changes can affect other departments. Known doorway/floor/wall contact and material/culling failures are not fixed by packaging. Full Blender/extracted game assets stay private; download patches require local originals.

## Diagnostics and testing

Core status names include `nlab_life_status.json`, `nlab_base_map.json`, command mailboxes, `nlab/imb-life-save.lua` and `imb-native-ranks.lua`. Use IH/IHHook logs and the owned availability/recorder menu; omit personal saves/captures from public reports.

Offline test evidence and limitations are in [tests/README.md](tests/README.md). Installer tests use temporary fake-game directories, never a real game root. Relevant code/transaction/reconstruction checks pass, but fresh native gameplay, foreground performance and endurance acceptance of this exact public alpha are pending.
