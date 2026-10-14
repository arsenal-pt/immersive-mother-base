# Offline verification

From repository root, with Python 3.10+, Node.js and externally installed `lupa` providing Lua 5.1:

```powershell
python -B tests/test_core.py
python -B tests/test_companion.py
node tests/test_map.cjs
```

You can pass `--library-dir` to test_core.py for an existing Lupa directory. Core checks validate actual source, menu wiring, fail-closed unavailable services, regular soldier setup, throttled updates, recorder closure and pure life/hierarchy/reservation behavior. fixtures/LifeLayout.lua preserves authored behavior assumptions for the pure 31-case suite; it is not an installed runtime resource.

The HTTP suite uses temporary synthetic files, an ephemeral child server and the test Python process as the exact-executable fixture. It terminates only that child; real port8785, game roots and saves are not used. Map checks use the authored module with a DOM fixture. Test outputs belong in ignored build/.

The platform helper tests validate exact input/output hashes, corrupted/wrong-base rejection and no-overwrite staging. None of these offline suites claims native animations, floor contact, accessibility, frame rate or installation acceptance.

For optional platform checks, install its external requirements and run `python -B tests/test_platform.py`. Add `--originals-root` to validate all three frozen outputs from your exact owned inputs.


## Alpha installer and context regressions

`python -B tests/test_installer.py` verifies reversible file transactions in temporary fake-game folders:31tests,30pass and one Windows-symlink privilege skip; actual Windows junction rejection is separately tested and passed. It checks corrupt payloads/backups, path boundaries, process/OS locking, upgrades/earliest originals, partial failure recovery, preservation of edits and refusal of the legacy private IH-extra adapter.

`python -B tests/test_readiness.py --library-dir <existing-Lupa-library-folder>` runs16portable context checks against the installed-source candidate. Cached actions/direct-provider commands must reject non-normal/loading/other-mission contexts while valid normal-MB patrol still works. Actual IH r267 loader/menu replay was also checked privately without bundling upstream source.

The source manifest tracks current payload hashes. Historical native evidence is not transferred to this alpha. Package ZIP hashes and corresponding-source tag are in the versioned release manifest.
