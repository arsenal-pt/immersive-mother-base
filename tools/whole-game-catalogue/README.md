# Whole installed game asset catalogue

This local Windows tool inventories your installed MGSV files and archive members beyond the separate149-model retained preview intake. Normal runs use Python, SQLite and your installed Atvaark GzsTool.Core0.5.3; they require no AI, MCP, server or network. The authored tool was developed with OpenAI Codex assistance.

A filesystem census and outer archive index do not mean every nested model has been found, its dependencies resolved or its preview rendered. Status/export keeps those counts separate. All occurrences, unknown names/types and same-path alternatives remain present; runtime load priority is unresolved.

## Setup and run

Use Python3.11+ on Windows and installed GzsTool0.5.3 with its original DLLs/dictionaries. Keep all original tool files together. Windows .NET Framework4 csc compiles the thin helper once into your private runtime. Nothing is downloaded. Copy config.example.json to a private config.local.json and replace the paths. The runtime and export roots must be separate and outside the game, installed tool directory and public checkout.

Set MGSV_CATALOGUE_CONFIG to your private config path and MGSV_CATALOGUE_PYTHON if python is not on PATH. Double-click Index-Game-Assets.cmd. It performs filesystem census and metadata-only archive indexing, prints coverage, then asks for a nested-container allowance. Default0 stops at the outer index; enter a positive count or explicit all to opt into bounded nested expansion. Each run writes a fresh metadata export and pauses.

Command examples:

    python catalogue.py --config PRIVATE/config.local.json census
    python catalogue.py --config PRIVATE/config.local.json index
    python catalogue.py --config PRIVATE/config.local.json status
    python catalogue.py --config PRIVATE/config.local.json expand --count 25
    python catalogue.py --config PRIVATE/config.local.json expand --count all
    python catalogue.py --config PRIVATE/config.local.json expand --count 1 --container FULL_CONTAINER_ID
    python catalogue.py --config PRIVATE/config.local.json cancel
    python catalogue.py --config PRIVATE/config.local.json export

Count means unfinished container attempts, including resumed attempts; it does not promise that many successful assets. Indexed valid work costs0. Failures/unsupported cases retain reasons and are skipped until explicit --retry-review or changed source evidence. A completed selected container returns a verified index cache hit. Newly found nested containers enter the persistent queue in the same explicitly chosen budget. Default maxDepth8 limits recursion.

## Metadata and bounded extraction

Census walks the whole configured install root without following directory links/junctions. It records protected/private/backup/runtime/config exclusions without reading those contents. Active archive detection uses bounded signatures, including ASF media that happen to use .dat. master DLC paths are recursive; MGO and master source paths remain distinct.

Index calls existing QAR/FPK/FPKD/SBP metadata readers. PFTXS uses a small attributed framing adapter plus the library's public entry-record reader; it avoids the upstream eager payload loop. Unknown formats stay typed/searchable when available, rather than falsely completing a converter.

Nested expansion must selectively decode its enclosing compressed/encrypted QAR member to reach inner tables. It uses existing public Export APIs, never a whole-DAT dump. Actual content SHA256 is populated only after those selected bytes are hashed. Full archive SHA256 remains null; source identity/size/mtime/header and metadata-index SHA are different evidence. FPK filename MD5 and QAR path hashes are not content hashes. Filename origin distinguishes embedded, dictionary-resolved, generated and hash fallback.

Defaults:256MiB maximum declared/decoded container,1GiB combined raw cache/partial stages,2GiB logical read budget per command,2GiB free-space reserve,180second helper timeout and1.5GiB owned-child working/private-memory watchdog. Existing codecs allocate whole buffers, so a malformed compressed stream can exceed its declared length before the watchdog stops it; a failed/terminated decode never becomes complete. The final actual decoded size is checked again. Cache paths use collision-checked short keys; decoded content is shared while all occurrence chains remain. Index metadata, DLL fingerprints and cache verification also consume the read budget.

SQLite persists source snapshots, member occurrences, references, container queue, events and cache hashes. Cancellation terminates/waits only for this worker's child and returns130; completed transactions remain. Source change is detected before/after work and requires a new census. A crashed parent may leave worker.lock; inspect its PID/owned child before manual recovery. Hard-crash cleanup is not automated. No game writes, repacking or game launch occurs.

## Downstream intake and export

Each fresh export contains sanitized catalogue.sqlite plus sources/containers/occurrences/refs CSV, status.json and README. No operational DB, physical source/cache/config paths or raw payloads are exported. IDs, parent-occurrence links, original/resolved names, type/hash/range metadata and lazily known content hashes support later intake selection.

Material sampler/path-hash to FTEX sidecar closure, FOVA/character assembly, compatible animation rigs, FOX shading and preview rendering are separate adapters. This tool currently reports dependency_resolved0 and previews0; the existing149-model renderer remains separate. MTAR/GANI occurrences are searchable when encountered, but clip-level enumeration/playback is not implemented.

## Validation and source credit

Run test_catalogue.py with MGSV_CATALOGUE_TEST_TOOL pointing to the installed pinned tool directory and MGSV_CATALOGUE_TEST_ROOT pointing to a private test workspace. Tiny authored QAR/FPK/SBP/PFTXS fixtures use upstream QAR writing only in tests; they cover unknown/null hashes, references, bounded expansion/restart/cache reuse, malformed ranges, source mutation, export privacy and owned-child cancellation/timeout. No real game payload is needed by tests. Real native-branch coverage is stated separately in the review receipt.

See THIRD-PARTY-NOTICES.txt. Primary APIs are pinned to [Atvaark GzsTool0.5.3](https://github.com/Atvaark/GzsTool/tree/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5). Konami owns original game assets; no raw game payloads are bundled.

## Size-field compatibility

GzsTool0.5.3 has reversed Read-property labels: QarEntry.UncompressedSize holds the stored byte count consumed by ReadData, while QarEntry.CompressedSize holds the header-declared decoded count. Its Write method writes compressedSize into the former field and uncompressedSize into the latter. The extent check correctly uses stored bytes. See [upstream Write274-308](https://github.com/Atvaark/GzsTool/blob/fc4a8196555638c6cf8aa1b7c8dc34ccd5c69cb5/GzsTool.Core/Qar/QarEntry.cs#L274-L308).

The operational legacy declared_size/compressed_size fields preserve those raw values. Prefer the member_sizes view and exported stored_size/declared_decoded_size columns; actual_size/content_sha256 remain separately measured evidence from selected decoding. For non-QAR members the header-declared decoded size is null where the format/transform does not provide it. A tiny authored final-member fixture with decoded length larger than the whole archive guards this distinction.

Every cache acceptance validates the current source snapshot first. Stale metadata-index repair preserves unchanged members' already verified decoded SHA/size evidence. Partial JSONL from a failed helper is retained diagnostically and never imported.

The next deterministic preview-intake bridge is described in the separate review lane; it remains pending. Discovered FMDL records do not automatically become compatible with the existing149-model renderer.
