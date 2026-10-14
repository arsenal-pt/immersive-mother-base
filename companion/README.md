# Immersive Mother Base — optional companion

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

Credit to **arsenal-pt**, a mention of **Immersive Mother Base**, and a link back to the official repository would be appreciated. This is a community request for prominent project credit, not an additional license restriction. Applicable license, copyright and third-party notices must still be preserved as required by their terms.

Creator: **arsenal-pt**. This is a pre-alpha source component. Original source license: **GPL-3.0-only** (see LICENSE and LICENSE-SCOPE.md). Full provenance/distribution review remains pending; a finished playable release is not implied.

This optional browser dashboard displays status produced by the in-game Lua simulation and sends commands through its existing local text mailboxes. It does not simulate staff independently. The game core and its Infinite Heaven / IHHook dependencies must be supplied and installed separately. No framework source, binaries, game assets, extracted catalogues, saves or personal configuration are included. Extra IH staff adoption, walking pilots, inspection and graph experiments are excluded.

Requires Windows and Python 3.10 or newer. It uses the Python standard library; no package installation is required. Game build support and core dependencies must be confirmed by the core candidate review. Optional native name enrichment is limited to the original reviewed **day3900** signatures and disabled by default; support for other builds is not claimed.

## Start

Run from this directory with paths to your owned local installation:

    python -B server.py --mod-root "D:/Games/MGS_TPP/mod" --game-exe "D:/Games/MGS_TPP/mgsvtpp.exe"

Default URL: http://127.0.0.1:8785. Use --port 8790 for another port. The server listens on loopback only, never launches the game, and refuses to start without an explicit existing mod directory and executable path.

Alternatively copy config.example.json to a personal config file, set the two installation paths, and run:

    python -B server.py --config config.local.json

Config paths are relative to the config file; CLI paths are relative to the current directory. CLI values override config. Keep personal config outside a shared package.

Stop with Ctrl+C. Removing the companion directory uninstalls it. This does not change saves, remove/reinstall the core, or launch/close MGSV.

## Optional local data

Private deck geometry, layout fixtures and extracted language tables are excluded. Leave their config values null when unavailable.

- geometry_catalog / --geometry-catalog: an explicit local catalogue compatible with the authored map module. Without it, the map displays observed coordinates on a grid and reports deck geometry unavailable. No complete platform or collision coverage is claimed.
- layout_file / --layout-file: optional local layout. Without it, the dashboard works but supplemental facility markers are unavailable.
- native_names: true / --native-names plus name_resources / --name-resources: opt into read-only name lookup against separately owned language data. Original day3900 signatures are validated before fixed-address reads. Missing data, a closed process or signature mismatch keeps feed labels. No roster/table is bundled, no cache is persisted, and no Lua name table is published.

Executable paths, game build and owned data are never guessed. In-game naming remains core-owned; this helper only enriches browser labels.

## Status and action gates

Retained endpoints: /status, /staff-status, /base-map-state, /base-map-geometry, /layout, /command and /staff-command. Existing files: nlab_life_status.json, nlab_base_map.json, nlab_staff_control_status.json, nlab_life_command.txt and nlab_staff_command.txt.

The last complete snapshot survives partial replacements without refreshing age. Commands require a fresh, advancing normal Mother Base feed and the exact configured executable process. Staff changes require ready normal-MB capacity and their own fresh status. Native CQC readiness and scheduled verification are separate gates. One life command remains outstanding until acknowledged; staff commands retain their bounded pending gate. Writes use a unique temporary file and atomic replacement.

POST requests accept the current loopback Origin or no Origin for local tools. Unknown routes and unsupported bodies are rejected. Extra IH endpoints and catalogue browsing are absent. Legacy extra-adapter actors and metadata are filtered defensively if an earlier feed is connected; this does not install or activate the adapter.

A closed/paused game, wrong mission or stale feed makes controls unavailable. Missing feeds return HTTP 503. There is no fixture or simulated runtime fallback.

## Verification and limits

Offline tests use the actual child server on ephemeral ports with temporary synthetic files. They cover status, atomic life/staff IPC, outstanding commands, Origin, stale/partial feeds, closed exact executable, wrong mission, paused state, capacity/CQC gates and excluded routes. The map test uses the actual authored module and a DOM fixture. Exact test child handles are terminated; real mod roots and port 8785 are never used.

From the repository root:

    python -B tests/test_companion.py
    node tests/test_map.cjs

These are source/offline checks. Installation, browser-to-core real gameplay, game-build compatibility and performance remain pending root review and native acceptance. Geometry, service-animation and recorder limitations are not solved by packaging.

Authored source was developed with Codex assistance; candidate preparation also used Codex. No generated art/audio/assets are included. Infinite Heaven and IHHook remain separately acquired core dependencies, credited to their upstream authors and not relicensed by this candidate.

## License

Eligible original project code is licensed under **GNU GPL v3.0 only (GPL-3.0-only)**. See [LICENSE](LICENSE), [LICENSE-SCOPE.md](../LICENSE-SCOPE.md) and [source-manifest.json](../source-manifest.json) for the text and identified scope.

If you distribute a covered modified version, its recipients must receive GPL rights and the corresponding editable source, including required build/install material. Private changes can remain private. Commercial use is allowed. The official project is intended to be available free of charge; GPL itself does not prohibit charging for copies.

Credit to arsenal-pt and links back are appreciated. Contributions through issues and pull requests are welcome while the project is under active development; GPL does not require a push to this particular repository. Preserve applicable license/copyright notices and identify modifications. Game assets, framework/dependency material and other upstream work keep their own terms. Full provenance/combined-distribution review remains a release gate.
