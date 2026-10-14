# Immersive Mother Base

**AI/LLM development disclosure:** To date, this project's original mod implementation and companion tooling have been developed entirely using AI large language models (LLMs), through Codex. Arsenal-pt conceived the project, defines its requirements, directs development and tests gameplay. This is an AI-developed project, not a claim that a human programming team hand-wrote the implementation. Existing game assets, Infinite Heaven/IHHook and other upstream tools were created by their respective authors and are not claimed as this project's AI-generated work.

**Creator's note:**

> Made entirely with OpenAI Codex (I have no coding/programming/modeling experience of any kind and I really wanted to improve a game which I love).

**Active development:** This repository is under active development and is currently pre-alpha. Contributions are appreciated, especially from people who can review and improve the AI-developed code, performance, native game integration and usable Mother Base spaces. Contributions through issues and pull requests to the official repository are encouraged; future human-authored contributions will be credited separately.

Pre-alpha source repository. Creator/maintainer: arsenal-pt. No downloadable release yet.

A mod project for **Metal Gear Solid V: The Phantom Pain (MGSV TPP)** to make Mother Base a working, inhabited military base: identities, needs, duties, services, training, specialist personnel and usable spaces that follow the base you have actually built.

## Repository contents

- [core](core/README.md): in-game daily-life modules and a single IH menu.
- [companion](companion/README.md): optional loopback dashboard using the same simulation.
- [Command Platform v9.1](platforms/command-v9/README.md): optional, hash-checked local rebuild patches from the v9 branch.
- [experimental-sdk](experimental-sdk/README.md): preserved prototypes, outside installation.
- [resource-tools](resource-tools/README.md) and [tests](tests/README.md): authored route builder and offline verification.

## First-version design

One mod installation and one Immersive Mother Base menu in IH, with submenus for daily life, staff, training and diagnostics. Internal code remains modular. The visual localhost dashboard is a separate optional package using the same simulation.

Infinite Heaven/IHHook are external framework dependencies. Our experimental IH-extra-NPC adoption, controllers, graph variants and inspection/lineup are excluded. Independent future specialist definitions are a separate contribution track.

| Evidence | Current examples |
| --- | --- |
| Scoped private native evidence | Ordinary-soldier identity/availability, rank ceilings, local water service, manual routine dispatch, fixed-six manual CQC |
| Partial/prototype | Shower body sequence with fixture work pending, rest/sleep prototype, recorder012 short sample/marker take |
| Candidate work | Portable source/config/build, unified menu, optional dashboard without IH-adoption seams, exact-package testing |
| Future/known gaps | Complete service/schedule coverage, independent specialists, usable interiors across upgrades; Command1 access/support/rendering failures remain unresolved |

Evidence belongs to tested versions. Packaging does not make incomplete mechanics complete. Simulation health is distinct from combat hitpoints. Unsupported services defer needs instead of claiming relief.

## Requirements and current limits

Use a legally obtained local MGSV installation. Exact supported game/IH/IHHook revisions and repaired-hook requirements will be pinned after audit and candidate tests. No game assets are supplied.

See [INSTALL.md](INSTALL.md) for the current developer setup, backup/restore and companion instructions. This is a source publication, not a finished one-click playable release. Service routes/motion bindings still need clean resource packaging and fresh native acceptance; unavailable actions deliberately reject starts. Historical gameplay proof is not proof for this new source build.

## Contributions wanted

Highest priority: real usable rooms/spaces for each Mother Base platform and construction stage, plus door access, floors, walls, collision/navigation, lighting and stable rendering. Other priorities are independently defined doctors/nurses, ground crew, researchers, logistics/intel/command staff, native animations/services, performance review and testing.

Submit authored layouts/code/tests/local builders; keep game resources local. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

## Credits

Credit to **arsenal-pt**, a mention of **Immersive Mother Base**, and a link back to the official repository would be appreciated. This is a community request for prominent project credit, not an additional license restriction. Applicable license, copyright and third-party notices must still be preserved as required by their terms.

Credit individual contributors, TinManTex/IH/IHHook and audited tools/libraries. Unofficial project, not publisher/IH-developer endorsed.

## License

Eligible original project code is licensed under **GNU GPL v3.0 only (GPL-3.0-only)**. See [LICENSE](LICENSE), [LICENSE-SCOPE.md](LICENSE-SCOPE.md) and [source-manifest.json](source-manifest.json) for the text and identified scope.

If you distribute a covered modified version, its recipients must receive GPL rights and the corresponding editable source, including required build/install material. Private changes can remain private. Commercial use is allowed. The official project is intended to be available free of charge; GPL itself does not prohibit charging for copies.

Credit to arsenal-pt and links back are appreciated. Contributions through issues and pull requests are welcome while the project is under active development; GPL does not require a push to this particular repository. Preserve applicable license/copyright notices and identify modifications. Game assets, framework/dependency material and other upstream work keep their own terms. Full provenance/combined-distribution review remains a release gate.

## Optional Command Platform v9 component

The included **v9.1 / v9-E** patches rebuild the frozen Command Platform 1 revision from local stock game packages. The original v9 diagnostic crashed while loading and is superseded. V9.1 loaded in prior native tests, but upright doorway clearance, lower-bay floor support, inward wall collision, red decals and angle-dependent rendering remain known failures. Shared prop overrides affect matching props across other departments. It is an experimental geometry component, separate from daily-life simulation, and is not installed by default.

No extracted Blender scenes, original models/textures, game archives, third-party framework implementations, saves or private development history are published. Local reconstruction instructions and exact input/output hashes are included.
