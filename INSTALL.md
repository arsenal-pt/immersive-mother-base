# Developer setup and restore

This is a pre-alpha source publication. MGSV TPP on Windows, separately acquired Infinite Heaven and IHHook are required for the in-game core. The exact combined release package and supported revision matrix are still being verified. Do not treat an offline pass as a completed playable release.

## Core

1. Close MGSV for file changes. Back up your `mod` folder and saves. Keep a list of existing files and hashes for restoration.
2. Use a separate test profile and install the external IH/IHHook framework following its own instructions. This repository does not supply it.
3. Review `core/GameDir/mod`, then copy its `nlab` and `modules` contents to the matching directories in your test game's `mod` folder. Record overwritten files; do not install alongside another copy of these same module names. The public source omits our IH-extra adoption modules.
4. On a normal Mother Base visit, the owned menu is **Immersive Mother Base**. Observe availability before issuing a command. Missing resource gates deliberately reject service/group/CQC starts. Do not manually flip proof flags to bypass them.
5. Restore all backed-up overwritten files and remove only newly added owned files to uninstall. Runtime needs/ranks/recordings remain private local files, not shared with the repository. No save-editing step is required.

Current data names include `nlab_life_status.json`, `nlab_base_map.json`, life/staff command mailboxes, and `nlab/imb-life-save.lua` / `imb-native-ranks.lua`. A missing/stale feed is unavailable, not simulated browser data. Use IH/IHHook logs and the owned availability/recorder menu for diagnosis; omit personal saves/captures from public reports.

## Optional companion

Python 3.10+ and Windows; Python standard library only. Run from `companion`:

```powershell
python -B server.py --mod-root "D:/Games/MGS_TPP/mod" --game-exe "D:/Games/MGS_TPP/mgsvtpp.exe"
```

Open http://127.0.0.1:8785. It is loopback-only, never launches the game and uses the core's snapshots/mailboxes. Follow companion/README.md for explicit configuration and optional local name/geometry data. Stop with Ctrl+C; deleting this companion copy removes it without changing game saves. No hosted backend is required.

## Optional v9.1 platform

Follow platforms/command-v9/README.md. Its rebuild helper writes a new staging folder only; it never installs, launches or rewrites an archive. Back up before any separately chosen native install. Reconstructed packs are private local game-derived output. Known collision/rendering failures remain; the daily-life core does not require this geometry component.

## Resource builders and compatibility

Read resource-tools/README.md. The 250 authored route targets round-tripped offline, but native resource admission, service bindings and motion packaging remain pending. Existing physics/render overrides or other mods that replace the same resources conflict until reviewed. Named/story/FOB entry points are protected design requirements, not a blanket tested compatibility claim. Native foreground/endurance checks and a supported game/framework revision matrix remain on the roadmap.
