# Contributor verification recipes

These recipes turn the research into repeatable checks. They do not authorize or require a game launch. Use the project instructions and an explicit current task scope before any live install or native test.

## Before changing a resource

- Record game build, save context, IH/IHHook/SnakeBite versions, platform and completed grades.
- Hash original resource and record native path, archive/member identity, material/model/mesh and parent placement.
- Copy to a named candidate; never edit the source original.
- List expected changes and protected resources, including shared-pack consumers.

## Offline model or archive candidate

1. Parse source with a pinned tool/source revision and keep unknown fields opaque.
2. Require no-edit roundtrip or an explicit field-level diff.
3. Validate pointer ranges, counts, indices, bounds, resource references and all protected bytes with an independent reader.
4. Reopen the editor scene and compare source identity, transforms, geometry, UVs and materials.
5. Package from the reviewed candidate manifest and compare output hashes.
6. State clearly which engine properties are still untested.

## Native feature candidate

1. Define one actor family, one action, one endpoint and one stop condition.
2. Capture baseline process/session, live actor identity/status and control owner.
3. Use a bounded read-only observation before and after each action; correlate by actor generation and sequence.
4. Stop on an urgent need, muster, danger, stale observation, actor replacement or player-control conflict.
5. In finally, stop the feature, release leases, restore original routes/settings/camera/pad/clock and verify return.
6. Retain failures and label every claim with the exact version and scenario.

## Performance candidate

Use the same loaded scene, view, actor count, focus and time context. Capture red-capable interval data before and after one isolated change. Report average, p95/max interval, low-cadence windows and process context. A healthy capture that does not reproduce the trigger is inconclusive for causality. Do not infer native performance from offline Lua timings.

## New platform or grade

Start from source inventory and native center/connector transforms. Resolve the correct completed grade and location slot. Rebuild and test the target platform's own layout, shared-resource exposure, floor support, aperture, culling/material and route availability. Do not copy Command1 counts or coordinates as defaults.

## Release hygiene

Publish original explanations, authored glue and eligible project code with clear upstream links and license notices. Exclude owned game resources, extracted binaries, full Blender libraries, saves, memory dumps, credentials, absolute user paths and third-party source copies. Attribute community tools; follow their licenses. Separate alpha-release features from later private findings, and state native acceptance limits plainly.
