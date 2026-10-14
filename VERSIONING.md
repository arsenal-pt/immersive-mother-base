# Versions, downloads and reproducibility

The overall mod version is stored in `VERSION` and copied into the installed menu, package manifest and archive filenames during a release. It uses semantic versions, starting with `0.1.0-alpha.1`. Alpha means a testing release with a stated feature set, not completion of the roadmap.

A release uses a fixed Git tag such as `v0.1.0-alpha.1`, a changelog entry and separate core, optional companion and optional platform download archives. Checksums and per-file manifests identify exactly what was distributed. Build recipes and editable corresponding source are in this repository. Old releases stay available; fixes get a new version rather than silently replacing an old archive or moving its tag.

## Platform revisions are separate

`Command Platform1 (cl00/pl0; mtbs_unique_0000) — v9.1` identifies the original/first Command platform and our local geometry iteration. It does not mean the game's version9.1, overall mod version9.1, or all four Command platforms. Other departments/platforms get their own directory and version history when modified.

Historical platform revisions preserve their own input/output hashes and outcomes. Failed variants are labelled archived diagnostics; offline-only variants are not relabelled as native successes. Shared common-prop effects are disclosed separately. Original assets are immutable and stay local; downloads supply transformations that require exact stock resources from a legally obtained local game.

## Release checks

- Verify package allowlists and file hashes, installation prerequisites, backup/uninstall and collision with existing owned files.
- Run relevant Lua/companion/platform and installer tests. Keep offline evidence separate from native gameplay acceptance.
- Keep `VERSION`, the menu version, source manifest, changelog, platform index and download labels consistent.
- Publish only curated original source, notices and reviewed transformation artifacts; no extracted game files, stock/modified archives, Blender files with embedded game assets, saves or credentials.
- Record a release receipt with the final remote commit/tag and download hashes in the development log. Verify the remote result rather than assuming an upload succeeded.

Human-authored commits use the human contributor's identity. AI-generated implementation is credited explicitly; see [CONTRIBUTORS.md](CONTRIBUTORS.md). The official repository remains owned and maintained by arsenal-pt.
