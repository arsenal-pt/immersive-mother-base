# Experimental authored SDK - not installed

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

Credit to **arsenal-pt**, a mention of **Immersive Mother Base**, and a link back to the official repository would be appreciated. This is a community request for prominent project credit, not an additional license restriction. Applicable license, copyright and third-party notices must still be preserved as required by their terms.

Preserved non-IH prototype/controller/tool source from the workbench so the initial core does not silently discard it. These files are outside GameDir and are NOT installed, registered or loaded by the core candidate. GPL-3.0-only selected for eligible original source; full provenance/distribution review pending (see ../LICENSE-SCOPE.md).

NpcStaffControl needs independent reviewed test-slot allocation/resources; OutdoorRestPilot needs fixture/route validation; the performance probe and player-reference wrappers need hook/context review; SoldierClipAdapter is a local-owned-motion adaptation tool, not a shipped animation. No graphs, model/motion assets, private catalogs, traces or runtime data are supplied. Source presence does not grant native capability or prove gameplay behavior.

Before enabling one of these, review its provenance, replace private resource dependencies with a permitted independent/local builder, add safe integration/config and validate the exact candidate. Default installation should remain noninvasive. No old lab controller, IH extra-NPC adapter or private baseline data is included.

## License

Eligible original project code is licensed under **GNU GPL v3.0 only (GPL-3.0-only)**. See [LICENSE](../LICENSE), [LICENSE-SCOPE.md](../LICENSE-SCOPE.md) and [License-Manifest.json](../source-manifest.json) for the text and identified scope.

If you distribute a covered modified version, its recipients must receive GPL rights and the corresponding editable source, including required build/install material. Private changes can remain private. Commercial use is allowed. The official project is intended to be available free of charge; GPL itself does not prohibit charging for copies.

Credit to arsenal-pt and links back are appreciated. Contributions through issues and pull requests are welcome while the project is under active development; GPL does not require a push to this particular repository. Preserve applicable license/copyright notices and identify modifications. Game assets, framework/dependency material and other upstream work keep their own terms. Full provenance/combined-distribution review remains a release gate.
