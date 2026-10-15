# Special/zombie punch - player phase 2

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Special/zombie punch - player phase 2 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.gif)](../../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-29553c4699ca8` |
| Source archive | `player2_resident` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh2` |
| Clip hash ID | `29553c4699ca8` |
| Original source role | player |
| Role interpretation | special_actor_punch_candidate |
| Family / phase | zombie_melee / None |
| Raw source frames | 43 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 1430 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0` |
| GANI SHA-256 | `30f0aaad13eb97e979790384cfb9c27cbb451af07d1b360329ee8370d51ea645` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_resident-1281-snapzmb_s_atk_pnh2",
    "sourceArchive": "player2_resident",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 1281,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh2",
    "hashId": "29553c4699ca8",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack2",
    "frameCount": 43,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Distinct special-actor/transition candidate; not an ordinary soldier combo proof.",
    "sourceMtarSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 5088,
        "sha256": "30f0aaad13eb97e979790384cfb9c27cbb451af07d1b360329ee8370d51ea645"
      },
      {
        "extension": ".exchnk",
        "bytes": 96,
        "sha256": "49e5ce665e305efbe010b6e5b7365dcd6c134b6070b24cb7751294131cd74d16"
      },
      {
        "extension": ".enchnk",
        "bytes": 336,
        "sha256": "0b6d2cd76086bf97722f96c31a4d0e2b8e9a1e6781dbe33494ecbb00097b1634"
      }
    ],
    "displayTitle": "Special/zombie punch - player phase 2",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_resident-1281-snapzmb_s_atk_pnh2.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 1.43,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_resident-1281-snapzmb_s_atk_pnh2",
    "title": "Special/zombie punch - player phase 2",
    "shortIdentifier": "snapzmb_s_atk_pnh2",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh2",
    "sourceArchive": "player2_resident",
    "sourceArchiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "hashId": "29553c4699ca8",
    "sourceGaniSha256": "30f0aaad13eb97e979790384cfb9c27cbb451af07d1b360329ee8370d51ea645",
    "sourceRole": "player",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack2",
    "rawFrameCount": 43,
    "decodedTrackCount": 18,
    "headerIndex": 799,
    "sourceFramesSampled": [
      0,
      2,
      4,
      6,
      8,
      10,
      12,
      14,
      16,
      18,
      20,
      22,
      24,
      26,
      28,
      30,
      32,
      34,
      36,
      38,
      40,
      42
    ],
    "endpointFrameSavedPrivately": 43,
    "chosenSourceFramesPerSecond": 30,
    "gifFrameDurationsMilliseconds": [
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70,
      30
    ],
    "gifDurationMilliseconds": 1430,
    "nativeFrameRate": null,
    "rawLayoutFrameRateField": "5",
    "rawLayoutRateMeaning": "Unverified enum/value; not assumed to be frames per second",
    "referenceCharacter": "Stock Ocelot oce0_main0_def",
    "visualStatus": "actual decoded motion rendered on offline stock reference character",
    "nativeGameplayProof": false,
    "pairedAlignmentProof": false,
    "ordinarySoldierAttackProof": false,
    "cameraFixedForFullClip": true,
    "camera": {
      "fixedForEntireClip": true,
      "location": [
        -4.881778240203857,
        8.296561241149902,
        3.703960657119751
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.0996978282928467,
      "projectedMin": [
        -0.3889905512332916,
        -0.14525635540485382,
        -0.37959563732147217
      ],
      "projectedMax": [
        0.4617514908313751,
        1.6648280620574951,
        0.9519475698471069
      ]
    },
    "worldBounds": {
      "min": [
        -0.5543546676635742,
        -0.5314828157424927,
        -0.006611227989196777
      ],
      "max": [
        0.4660760760307312,
        0.6156499981880188,
        1.6505249738693237
      ]
    },
    "titledGif": {
      "path": "player2_resident-1281-snapzmb_s_atk_pnh2.gif",
      "bytes": 2002604,
      "sha256": "b972b33e22706d1fcb33df7d64dc75d52836b7adb873b5cd5a1eff176c80ea52"
    },
    "thumbnail": {
      "path": "player2_resident-1281-snapzmb_s_atk_pnh2.png",
      "bytes": 138326,
      "sha256": "9dd3b0d95b667c17d2968892bb9934d9b5820beff1d6fe59a787e5b5b7b5f425"
    },
    "privateCleanGifSha256": "f43ac4c70b0fd71a4919e060d6de2cdf6536485b51a072a43d47fa6272d366aa",
    "privateRenderReceiptSha256": "a4bf73135c25562509cdaa4bc8f9a229b1e9d48414963dbf6f121c0b7628c33e",
    "cleanPngFrameCount": 23,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
