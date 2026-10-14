# Immersive Mother Base

Immersive Mother Base aims to make **Mother Base in Metal Gear Solid V: The Phantom Pain** feel like a living, working military or mercenary base. Soldiers should have daily routines: patrol, rest, eat, train, use facilities, work on equipment and maintain the base. The long-term goal is to turn its unused spaces into places people can actually enter and use, including barracks, mess halls, workshops, clinics and offices. Reusing and repurposing the game's existing assets is the preferred approach, with routines and facilities adapting as your base grows. These are project goals; the current download's supported features and unfinished parts are listed below.

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Creator's note:**

> Made entirely with OpenAI Codex (I have no coding/programming/modeling experience of any kind and I really wanted to improve a game which I love).

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

**Owner, creator and maintainer:** [arsenal-pt](https://github.com/arsenal-pt). **Implementation contributor:** OpenAI Codex (AI assistant), under arsenal-pt's direction. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the distinction between these roles and GitHub's commit-based contributor display.

A mod project for **Metal Gear Solid V: The Phantom Pain (MGSV TPP)** to make Mother Base a working, inhabited military base: identities, needs, duties, services, training, specialist personnel and usable spaces that follow the base you have actually built.

## Repository contents

- [core](core/README.md): in-game daily-life modules and a single IH menu.
- [companion](companion/README.md): optional loopback dashboard using the same simulation.
- [Command Platform 1 — cl00/pl0, mtbs_unique_0000](platforms/command/platform-1/README.md): optional v9.1 and historical hash-checked rebuild patches; the other Command platforms have not been modified.
- [experimental-sdk](experimental-sdk/README.md): preserved prototypes, outside installation.
- [resource-tools](resource-tools/README.md) and [tests](tests/README.md): authored route builder and offline verification.

## First-version design

One mod installation and one Immersive Mother Base menu in IH, with submenus for daily life, staff, training and diagnostics. Internal code remains modular. The visual localhost dashboard is a separate optional package using the same simulation.

Infinite Heaven/IHHook are external framework dependencies. Our experimental IH-extra-NPC adoption, controllers, graph variants and inspection/lineup are excluded. Independent future specialist definitions are a separate contribution track.

## Download and current feature set

**[Download v0.1.0-alpha.1](https://github.com/arsenal-pt/immersive-mother-base/releases/tag/v0.1.0-alpha.1)** — separate core installer, optional local dashboard, Command Platform1 history/rebuild tools and corresponding source. See [DOWNLOADS.md](DOWNLOADS.md) for individual files and hashes. This is a ready-to-install **testing alpha foundation**, not the completed living-base roadmap.

| Included in this alpha | Not yet enabled in this public build |
| --- | --- |
| Existing regular-soldier observation; persistent identity and daily-life needs | Our experimental control/adoption of IH extra NPCs and specialist characters |
| Rank-limited hierarchy, reservations, bounded updates and native patrol dispatch | Clean-resource-dependent muster, group conversations and measured service actions |
| One Immersive Mother Base IH menu, diagnostics and action recorder | Finished shower, sleeping, eating and five-minute CQC gameplay routines |
| Optional loopback dashboard using the same in-game simulation | Finished interiors, repaired CMD1 collision/rendering or a complete native minimap |
| Reversible file installer and version/checksum manifests | Broad game/framework compatibility or fresh native performance acceptance |

The core excludes our IH-extra actor integration; **Infinite Heaven and IHHook remain external requirements** for the framework and menu. The browser dashboard is optional. Unsupported actions reject starts, and unavailable services defer needs rather than claiming a soldier ate, showered or recovered. Simulation health is separate from combat hitpoints. Historical private gameplay proof belongs to those tested builds, not automatically to this alpha.

## Requirements and installation

Windows, a legally obtained local MGSV TPP installation, separately installed [Infinite Heaven](https://www.nexusmods.com/metalgearsolidvtpp/mods/45) and [IHHook](https://www.nexusmods.com/metalgearsolidvtpp/mods/1226), and [Python3.10+](https://www.python.org/). The installer uses the standard library, verifies its payload hashes, checks prerequisites and refuses file changes while MGSV is running. It backs up overwritten owned files and provides a checked uninstall; it does not modify the executable, game archives, framework settings or saves.

Follow [INSTALL.md](INSTALL.md). Current offline framework review used IH r267; local native history used game1.0.15.4 and a separately repaired IHHook r25 build. Stock IHHook r25 has a known shared named-pipe lifecycle/performance issue; this core and companion do not use that named-pipe path. Structural prerequisite detection is not proof of full compatibility or FPS on another installation. No repaired DLL is included, and fresh native acceptance of the exact public alpha is still pending.

## Contributions wanted

Highest priority: real usable rooms/spaces for each Mother Base platform and construction stage, plus door access, floors, walls, collision/navigation, lighting and stable rendering. Other priorities are independently defined doctors/nurses, ground crew, researchers, logistics/intel/command staff, native animations/services, performance review and testing.

Submit authored layouts/code/tests/local builders; keep game resources local. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

## Credits

Credit to **arsenal-pt**, a mention of **Immersive Mother Base**, and a link back to the official repository would be appreciated. This is a community request for prominent project credit, not an additional license restriction. Applicable license, copyright and third-party notices must still be preserved as required by their terms.

Upstream authors made this project possible. See [CREDITS.md](CREDITS.md) for linked frameworks, modding tools, libraries and references, including Infinite Heaven, IHHook, SnakeBite/MakeBite, FoxKit/FoxLib, FMDL Studio and Blender. They retain their own authorship and terms. Unofficial project, not publisher/IH-developer endorsed.

## License

Eligible original project code is licensed under **GNU GPL v3.0 only (GPL-3.0-only)**. See [LICENSE](LICENSE), [LICENSE-SCOPE.md](LICENSE-SCOPE.md) and [source-manifest.json](source-manifest.json) for the text and identified scope.

If you distribute a covered modified version, its recipients must receive GPL rights and the corresponding editable source, including required build/install material. Private changes can remain private. Commercial use is allowed. The official project is intended to be available free of charge; GPL itself does not prohibit charging for copies.

Credit to arsenal-pt and links back are appreciated. Contributions through issues and pull requests are welcome while the project is under active development; GPL does not require a push to this particular repository. Preserve applicable license/copyright notices and identify modifications. Game assets, framework/dependency material and other upstream work keep their own terms. Full provenance/combined-distribution review remains a release gate.

## Optional Command Platform 1 — v9.1

The included **v9.1 / v9-E** patch rebuilds the frozen **Command Platform1 (cl00/pl0; mtbs_unique_0000)** revision from exact stock packages extracted from your legally obtained local game. It is a local geometry experiment, not MGSV version9.1 or a change to all Command platforms. Earlier shell/floor/access iterations led to v8/v8-A; v9 attempted broad no-cull rendering, and v9.1 corrected the native resource identity/package layout after v9-family loading failures. See the [platform index and version history](platforms/command/platform-1/README.md). The original v9 diagnostic crashed while loading and is superseded. V9.1 loaded in prior native tests, but upright doorway clearance, lower-bay floor support, inward wall collision, red decals and angle-dependent rendering remain known failures. Shared prop overrides affect matching props across other departments. It is an experimental geometry component, separate from daily-life simulation, and is not installed by default.

No extracted Blender scenes, original models/textures, game archives, third-party framework implementations, saves or private development history are published. Local reconstruction instructions and exact input/output hashes are included. Rebuilt packs can be packaged locally with MakeBite and installed as an optional resource replacement through SnakeBite. They are not a direct loose-file copy into the game folder, and our core installer never installs them automatically. Previous platform transformations are preserved with their own status and hashes; original/private Blender files remain unchanged. [VERSIONING.md](VERSIONING.md) explains the shared naming policy.
