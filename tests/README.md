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
