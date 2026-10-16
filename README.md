# Immersive Mother Base

Immersive Mother Base aims to make **Mother Base in Metal Gear Solid V: The Phantom Pain** feel like a living, working military or mercenary base. Soldiers should have daily routines: patrol, rest, eat, train, use facilities, work on equipment and maintain the base. The long-term goal is to turn its unused spaces into places people can actually enter and use, including barracks, mess halls, workshops, clinics and offices. Reusing and repurposing the game's existing assets is the preferred approach, with routines and facilities adapting as your base grows. These are project goals; the current download's supported features and unfinished parts are listed below.

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Creator's note:**

> Made entirely with OpenAI Codex (I have no coding/programming/modeling experience of any kind and I really wanted to improve a game which I love).

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

**Owner, creator and maintainer:** [arsenal-pt](https://github.com/arsenal-pt). **Implementation contributor:** OpenAI Codex (AI assistant), under arsenal-pt's direction. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the distinction between these roles and GitHub's commit-based contributor display.

A mod project for **Metal Gear Solid V: The Phantom Pain (MGSV TPP)** to make Mother Base a working, inhabited military base: identities, needs, duties, services, training, specialist personnel and usable spaces that follow the base you have actually built.

## Development showcase

**Recorded development build, 14 October 2026.** These are prototype results, beyond the smaller [public alpha feature set](#download-and-current-feature-set). Groups, services and CQC starts remain disabled in that download.

- The altered platform appearance, red decals and unfinished open interiors come from the **optional Command Platform 1 v9.1 experiment**. The standard core keeps the normal platform and does not add these WIP spaces.
- Children, doctors, some other NPCs and helicopters visible here come from the separately enabled **Infinite Heaven Mother Base NPCs** configuration; they are not included as features of this mod. The test mattress and radio are also excluded from the standard download.
- Reused animations still need pose/alignment/recovery fixes. Shower footage shows a queue only; NPC entry, washing and exit are unfinished. Room work still has doorway/floor/inside-wall collision failures, backface culling and textures popping in and out at certain angles.

### Captioned video - 2 minutes 50 seconds

https://github.com/user-attachments/assets/87f7cc30-23a1-49b6-bf4b-e100d5d832e4

Use the play button above to watch the captioned web version, or download the full-resolution copy below.

[Download the full-resolution captioned video (1080p, 24.3 MB)](https://github.com/arsenal-pt/immersive-mother-base/raw/refs/heads/main/media/showcase/2026-10-14/Immersive-Mother-Base-Showcase-CAPTIONED.mp4) Â· [Video captions](media/showcase/2026-10-14/video-captions.txt) Â· [All 17 screenshots and capture notes](media/showcase/2026-10-14/README.md)

### Muster and CQC training

| **Muster** - soldiers assembling at assigned spots | **CQC Training** - fixed pairs alternating practice throws |
| --- | --- |
| ![Muster - wider formation view](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/01-muster-angle-B.webp) | ![CQC training - fixed pairs, wider view](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/03-cqc-angle-B.webp) |

### Social gathering and shower queue

| **Social Gathering** - soldiers pausing to socialize | **Shower Queue (prototype)** - waiting at the unit; washing is not implemented |
| --- | --- |
| ![Social gathering - first angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/05-gathering-angle-A.webp) | ![Shower queue prototype - first angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/07-shower-queue-angle-A.webp) |

<details>
<summary>More event angles: Muster, CQC Training, Social Gathering and Shower Queue</summary>

| **Muster - opposite angle** | **CQC Training - opposite angle** |
| --- | --- |
| ![Muster - opposite angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/02-muster-angle-A.webp) | ![CQC training - opposite angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/04-cqc-angle-A.webp) |

| **Social Gathering - opposite angle** | **Shower Queue - opposite angle** |
| --- | --- |
| ![Social gathering - opposite angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/06-gathering-angle-B.webp) | ![Shower queue prototype - opposite angle](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/08-shower-queue-angle-B.webp) |

</details>

### Optional Command Platform 1 interiors - work in progress

| **Lower Shared Bay** - one large shared space planned behind the lower doors | **Main-Level Interior** - existing walls with experimental floors/openings |
| --- | --- |
| ![Lower shared bay (WIP) - eastward](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/09-lower-shared-bay-eastward.webp) | ![Main-level interior (WIP) - inward view](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/11-main-room-inward.webp) |

These are unfinished structural experiments, not accepted barracks, offices or other usable facilities. Floor support and upright door clearance remain unreliable.

<details>
<summary>More interior views: reverse angles, west interior and upper levels</summary>

| **Lower Shared Bay - reverse view** | **Main-Level Interior - reverse view** |
| --- | --- |
| ![Lower shared bay (WIP) - westward](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/10-lower-shared-bay-westward.webp) | ![Main-level interior (WIP) - reverse view](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/12-main-room-reverse.webp) |

**West Interior (WIP)**

![West interior (WIP)](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/13-west-room.webp)

| **Upper Interior - level 12 (WIP)** | **Upper Command Interior - level 20 (WIP)** |
| --- | --- |
| ![Upper interior (WIP) - level 12](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/14-upper-room-L12.webp) | ![Upper command interior (WIP) - level 20](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/15-upper-command-room-L20.webp) |

</details>

### Optional companion dashboard

| **Base Map and Testing Controls** | **Staff and Daily-Life Needs** |
| --- | --- |
| ![Companion dashboard - map and testing controls](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/16-dashboard-map.webp) | ![Companion dashboard - staff needs](https://raw.githubusercontent.com/arsenal-pt/immersive-mother-base/main/media/showcase/2026-10-14/17-dashboard-staff-needs.webp) |

The dashboard shown is the development testing setup. Its experimental controls do not mean those activities are enabled in the downloadable public alpha. See [capture notes](media/showcase/2026-10-14/README.md) and [credits](CREDITS.md).

## Repository contents

- [research](research/README.md): accumulated technical findings, known failures, source references and repeatable contributor workflows. Later development observations are labeled separately from the public alpha. Browse the [MGSV Animation Reference Library](research/animation-library/README.md): 27 clips in small animated tables, still-image pages, larger GIF views and complete data, including [two LMG ready/reload candidates](research/animation-batches/lmg-reloads/README.md). Tables show category, useful tags, actual source locations and plain-English descriptions; credits are retained in central/detail records.

- [MGSV Asset Reference Library](research/asset-library/README.md): 10 parent models and 19 preview views: seating, shelf components, ladder/door/gate/duct sections and a control switch, with static thumbnails, full stills/360-degree references, separate LOD/texture metadata and exact retained source identities. These are visual references; no source game assets are included.
- [Whole-game metadata catalogue](research/asset-library/whole-game-catalogue.md): local non-agentic installed-file/archive census,21QAR/202,303outer occurrences in the offline snapshot; nested dependency/preview bridge remains in progress.
- [core](core/README.md): in-game daily-life modules and a single IH menu.
- [companion](companion/README.md): optional loopback dashboard using the same simulation.
- [Command Platform 1 â€” cl00/pl0, mtbs_unique_0000](platforms/command/platform-1/README.md): optional v9.1 and historical hash-checked rebuild patches; the other Command platforms have not been modified.
- [experimental-sdk](experimental-sdk/README.md): preserved prototypes, outside installation.
- [resource-tools](resource-tools/README.md) and [tests](tests/README.md): authored route builder and offline verification.

## First-version design

One mod installation and one Immersive Mother Base menu in IH, with submenus for daily life, staff, training and diagnostics. Internal code remains modular. The visual localhost dashboard is a separate optional package using the same simulation.

Infinite Heaven/IHHook are external framework dependencies. Our experimental IH-extra-NPC adoption, controllers, graph variants and inspection/lineup are excluded. Independent future specialist definitions are a separate contribution track.

## Download and current feature set

**[Download v0.1.0-alpha.1](https://github.com/arsenal-pt/immersive-mother-base/releases/tag/v0.1.0-alpha.1)** â€” separate core installer, optional local dashboard, Command Platform1 history/rebuild tools and corresponding source. See [DOWNLOADS.md](DOWNLOADS.md) for individual files and hashes. This is a ready-to-install **testing alpha foundation**, not the completed living-base roadmap.

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

## Optional Command Platform 1 â€” v9.1

The included **v9.1 / v9-E** patch rebuilds the frozen **Command Platform1 (cl00/pl0; mtbs_unique_0000)** revision from exact stock packages extracted from your legally obtained local game. It is a local geometry experiment, not MGSV version9.1 or a change to all Command platforms. Earlier shell/floor/access iterations led to v8/v8-A; v9 attempted broad no-cull rendering, and v9.1 corrected the native resource identity/package layout after v9-family loading failures. See the [platform index and version history](platforms/command/platform-1/README.md). The original v9 diagnostic crashed while loading and is superseded. V9.1 loaded in prior native tests, but upright doorway clearance, lower-bay floor support, inward wall collision, red decals and angle-dependent rendering remain known failures. Shared prop overrides affect matching props across other departments. It is an experimental geometry component, separate from daily-life simulation, and is not installed by default.

No extracted Blender scenes, original models/textures, game archives, third-party framework implementations, saves or private development history are published. Local reconstruction instructions and exact input/output hashes are included. Rebuilt packs can be packaged locally with MakeBite and installed as an optional resource replacement through SnakeBite. They are not a direct loose-file copy into the game folder, and our core installer never installs them automatically. Previous platform transformations are preserved with their own status and hashes; original/private Blender files remain unchanged. [VERSIONING.md](VERSIONING.md) explains the shared naming policy.
