# Credits and provenance

## People and original work

- **[arsenal-pt](https://github.com/arsenal-pt)** — repository owner, project creator and maintainer; concept, requirements, direction, gameplay testing and official release decisions.
- **OpenAI Codex (AI assistant)** — implementation contributor/tool. All original project implementation and companion tooling to date were developed entirely using AI/LLMs under arsenal-pt's direction. Models and sessions varied; no single model is claimed for the whole history. Future human contributions will be credited individually. See [CONTRIBUTORS.md](CONTRIBUTORS.md).
- **Konami / Kojima Productions and the MGSV development team** — Metal Gear Solid V: The Phantom Pain and its existing models, textures, animations, audio and world assets. This project repurposes locally owned game resources; it does not claim their creation or ownership. Unofficial, not endorsed by the publisher.

## Upstream mods and runtime framework

| Project / authors | Role in this project | Source |
| --- | --- | --- |
| Infinite Heaven — TinManTex and contributors | External Lua framework and menu/module interfaces; still required. Our IH-extra-NPC adoption experiment is excluded from this public core. | [Repository](https://github.com/TinManTex/InfiniteHeaven), [mod page](https://www.nexusmods.com/metalgearsolidvtpp/mods/45) |
| IHHook — TinManTex and contributors | Separately acquired hook/menu/IO support. Local patched-hook performance work is separate from this source package; no DLL is bundled. | [Repository](https://github.com/TinManTex/IHHook), [mod page](https://www.nexusmods.com/metalgearsolidvtpp/mods/1226) |
| SnakeBite / MakeBite — TinManTex and contributors | Game archive mod management and local `.MGSV` packaging; optional platform install uses this external workflow. | [Repository](https://github.com/TinManTex/SnakeBite), [mod page](https://www.nexusmods.com/metalgearsolidvtpp/mods/106) |

These authors created the underlying framework/tool systems. Our AI-development disclosure applies to our original implementation, not to their work. Do not strip their notices, redistribute their implementations as ours, or infer endorsement.

## Asset, format and build tools

| Tool / authors | Actual use / evidence | Source |
| --- | --- | --- |
| GzsTool — Atvaark and contributors | Archive/FPK unpacking and repacking; local platform pipeline used v0.5.3. | [Repository](https://github.com/Atvaark/GzsTool) |
| MtarTool — BobDoleOwndU and contributors | Actual local MTAR unpack/repack and round-trip checks; animation experiments and punching-combo extraction use v0.2.7. Extracted game motions remain private. | [Repository](https://github.com/BobDoleOwndU/MtarTool), [community guide](https://mgsvmoddingwiki.github.io/MtarTool/) |
| Fox Engine MTAR Tools for Blender — mctrollin and contributors | Existing animation inspection and selected player-to-soldier conversion reuse its binary reader/writer utilities. This does not mean every clip was edited in the Blender GUI or is runtime-compatible. | [Repository](https://github.com/mctrollin/fox_engine_mtar_tools_blender) |
| FoxTool — Atvaark and contributors | Native FOX2/XML decode/compile; local pipeline used v0.2.6. | [Repository](https://github.com/Atvaark/FoxTool) |
| FtexTool — Atvaark and contributors | Locally owned texture decoding/preview workflow. | [Repository](https://github.com/Atvaark/FtexTool) |
| FMDL Studio v2 — BobDoleOwndU and contributors | Model/material format references and Unity import/export validation. Culling reference reviewed at d580b94215cc007df6c38bdb0bfce6a0f30e4701; byte-preserving authored writers were also used rather than treating every build as an ordinary Studio export. | [Repository](https://github.com/BobDoleOwndU/FMDL-Studio-v2), [wiki](https://github.com/BobDoleOwndU/FMDL-Studio-v2/wiki) |
| FoxKit / FoxLib — youarebritish and contributors | Fox formats, route serialization and native string-hash recipe. FoxKit's reused hashing notice is retained. | [FoxKit](https://github.com/youarebritish/FoxKit), [FoxLib](https://github.com/youarebritish/FoxLib), [retained notice](resource-tools/FoxKit-Hashing-Upstream-Notice.txt) |
| Blender — Blender Foundation and contributors | Geometry/material editing and previews; local platform authoring used Blender3.6.23. | [Blender](https://www.blender.org/) |
| Unity — Unity Technologies | Host for FoxKit/FMDL Studio conversion/validation; isolated tested editor2021.3.45f2. MGSV itself runs on FOX Engine. | [Unity](https://unity.com/) |
| FSharp.Core / .NET compiler — Microsoft and contributors | External route-builder dependencies. | [F#](https://github.com/dotnet/fsharp), [.NET](https://dotnet.microsoft.com/) |
| CityHash — Google and contributors | External native route-hashing build dependency. The exact compatible DLL is hash-gated by the builder. | [CityHash](https://github.com/google/cityhash) |
| bsdiff / bsdiff4 — Colin Percival, Ilan Schnell and contributors | External BSDIFF40 generator/patch library for hash-checked local platform reconstruction; bsdiff4 pinned1.2.6. | [bsdiff](https://www.daemonology.net/bsdiff/), [bsdiff4](https://github.com/ilanschnell/bsdiff4) |
| Python — Python Software Foundation and contributors | Installer, optional companion, local build and verification scripts. | [Python](https://www.python.org/) |
| Lupa — Stefan Behnel and contributors; Lua authors | Offline Lua5.1 verification; testing dependency, not bundled with runtime. | [Lupa](https://github.com/scoder/lupa), [Lua](https://www.lua.org/authors.html) |
| Git / GitHub | Local source history, reviewed publication and versioned releases. | [Git](https://git-scm.com/), [GitHub](https://github.com/) |

FMDL Studio's upstream README also credits **Joey35233, youarebritish (sai), Tex, Highflex and revel8n**, and earlier format research by **Jayveerk, cra0kalo and HeartlessSeph**. Their contributions are credited through the original project; this does not mean each directly contributed to Immersive Mother Base. Our extraction used original project-specific FMDL readers and Blender scripts alongside those references, rather than claiming a third-party Blender importer was used without evidence.

## Documentation and community

The **[MGSV Modding Wiki and its contributors](https://mgsvmoddingwiki.github.io/)** provided format, installation and conversion guidance, including [Mother Base clusters](https://mgsvmoddingwiki.github.io/MotherBase_Clusters/), [Infinite Heaven](https://mgsvmoddingwiki.github.io/Infinite_Heaven/), [SnakeBite](https://mgsvmoddingwiki.github.io/SnakeBite_Mod_Manager/) and [FMDL Studio with Blender](https://mgsvmoddingwiki.github.io/Using_FMDL_Studio_with_Blender/). The MGSV modding MCP workbench provided source/catalog access and managed conversion tooling; it is a development tool, not a player dependency.

No generated fal artwork/audio is included in this public release. Private gameplay captures, downloaded sound files, other installed mods and experimental IH staff assets are not part of these downloads. Reviewing another mod for compatibility does not make its implementation ours or mean it is bundled.

Eligible original source is GPL-3.0-only. External game/framework/tool/library material retains its own rights and terms; the GPL file does not relicense it. Builders use separately acquired dependencies; new vendored third-party code needs explicit provenance/notices. See [LICENSE-SCOPE.md](LICENSE-SCOPE.md). Prominent credit and links back to the official project are appreciated.
