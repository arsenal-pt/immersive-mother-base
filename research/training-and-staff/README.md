# Training animations and walking staff

This work is in progress. The goal is fluid unarmed practice, shooting with the correct weapons, a watching circle, and compatible medical and maintenance staff who can walk around Mother Base. No new gameplay fix is accepted by this research update.

[Animation library](../animation-library/README.md) | [Asset library](../asset-library/README.md)

## Training repair

A recorded four-person test completed four rounds and two alternating role cycles. Completed initiator motions remained held for about 8.9-9.2 seconds while the other role recovered and the pair rested. This reproduces the visible frozen or leaning endpoints.

Two attempted idle transitions were rejected. A rifle-ready reference gave the wrong empty-handed posture; replaying its same path did not produce a second completion event. Releasing the held action back to the normal controller also gave a rifle-ready posture and a guard interruption. The first precise offending condition was not established by the retained samples. Both trials were rolled back. The missing-completion, identity, ownership, support and cleanup checks remain in place.

The next source-backed candidate is the player unarmed-family idle `snapnon_s_idl_r`. Its ordered bindings match the retained Soldier layout after the existing root-vector precision conversion. That conversion preserves the other 55 segments, but a codec round trip is not native posture or loop proof. Its full-character preview shows a relaxed unarmed stance and a closely matching loop seam. A reviewed duration/resource plan and native gameplay test are still required. Automatic training stays off.

Shooting, pistols, matched contact, circle spectators and a complete sustained session remain separate native acceptance tasks.

## Unarmed idle reference

**Simple name:** relaxed unarmed standing idle. **Game identifier:** `snapnon_s_idl_r` from `player2_resident`.

[Open the titled animation detail](unarmed-idle.md) | [Still alternative](unarmed-idle-still.md) | [Preview metadata](unarmed-idle-preview.json)

This index loads no images. The separate animated detail loads one GIF; the still page loads one PNG and no GIFs.

This is an **experimental adapted reference** on the stock Ocelot mesh, with **offline visual evidence only**. It is not a working training fix or a native soldier demonstration. The two rejected native idle-transition trials described above were rolled back. The original motion is a Snake/player-family clip. Its 150 raw frames use a chosen preview rate of 30 source frames/s; native timing is unmeasured. The experimental adapted reference changes only the root-vector precision, preserving the other 55 segments. An ordered binding match to a retained Soldier layout does not prove Soldier2 playback compatibility. First/end evaluated mesh positions differ by less than 0.000001 in the offline reference scene. This supports a loop proposal; it does not establish native loop playback or duration coverage.

## Requested cinematic references

| Requested scene | Retained script candidate | Evidence available | Still required |
| --- | --- | --- | --- |
| Ocelot trains recruits / shooting range | `OcelotIsPupilOfSnake`, `p51_010350_000_final`, `f30050_d002.fpk` | Selected scene package, board/weapon-related members, SAND mapping and 105 decoded DEMO packets | Confirm the English scene mapping; decode rotations; identify actor/bone bindings; convert and preview choreography |
| Low morale / Mother Base fight | `MoraleOfMBIsLow`, `p51_010040_000_final`, `f30050_d000.fpk` | Selected scene package and retained script mapping | Extract and decode its separate cinematic stream, identify roles and verify gameplay-compatible motion |

These mappings come from retained local scripts containing Infinite Heaven/tex edits. They are not a claim that an untouched current game script or the English scene title has been verified.

The common Ocelot package yielded 37 body and 11 facial ordinary motions. Those are not the cinematic choreography. For one selected shooting-scene skeletal packet, 15 static vector channels decode; 67 rotation channels stop at the unsupported 18-bit quaternion format. No guessed decoder or actor labels were substituted. The checked [Fox Engine animation template](https://github.com/kapuragu/FoxEngineTemplates/blob/14e1396e109a81d99f96f6e873663c3a8e28a9ed/common/anim_common.bt) and [motion reader](https://github.com/mctrollin/fox_engine_mtar_tools_blender/blob/7fa90e589349ad4ba87102f0061a8d8d343a8bf4/py_utilities/util_binary_read.py) establish other widths, not this format.

The inspected native demo interface plays a whole scene and applies a scene transform. It provides no established per-NPC skeletal-track binding route. Its Mother Base wrapper also changes gameplay state, so playing the whole cinematic is not a substitute for ambient training.

## Walking staff

The first test is one additive doctor on a normal Hostage2 controller, keeping all 30 existing Infinite Heaven actors and protected named/child actors. Its two packages compiled and passed unpack/round-trip checks. A temporary native test preserved all 30 original actor identities, but the additive doctor did not resolve: the game package lookup reported both custom pack names missing from its package registry. No movement command was sent. The exact original physical archive was restored afterward. The lookup function still returns the requested pack list, so those warnings alone do not prove the engine omitted the payloads. Package and actor-definition binding remain under investigation; native walking is not yet proved.

| Appearance | Exact source status | Gameplay status |
| --- | --- | --- |
| Doctor | IH `DOCTOR_0`, TPP `dct0_main0_def_v00_ih_hos.parts` | Native additive actor unresolved; package-lookup and actor-definition binding under investigation |
| Nurse | IH `NURSE_3_FEMALE`, TPP `nrs3_main0_def_v00_ih_hos.parts` | Known TPP mapping; normal-controller test pending |
| Maintenance crew | IH `DDS_GROUNDCREW` mapping | Controller/parts compatibility unresolved; the documented Soldier2 loading failure is not a supported integration |
| Ground Zeroes nurse | Exact model/parts/rig unidentified | Two supported archive indexes checked; unknown entries and one unsupported index remain, so absence is not established |

Appearance alone does not establish animation or controller compatibility. Successful walking requires a real, independently identified actor, gradual horizontal movement on a valid route, preserved original actors, and confirmed scoped cleanup.

## Publication and evidence

The existing animation library contains reviewed decoded previews with readable titles and exact source identifiers. Unsupported cinematic tracks are not counted as usable library entries. Native bug recordings, extracted game payloads, rigs, archives and saves remain private. Only reviewed rendered previews, authored metadata, research and code belong in the public repository.

This page records a research boundary, not a new mod release. Preparing this research packet changes no installed runtime or release tag. No accepted training fix, complete cutscene choreography or Ground Zeroes nurse identification is claimed.