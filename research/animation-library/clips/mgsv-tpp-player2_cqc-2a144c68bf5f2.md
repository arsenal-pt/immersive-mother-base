# Snake CQC combo - back phase 2

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - back phase 2 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-2a144c68bf5f2` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_b2` |
| Clip hash ID | `2a144c68bf5f2` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | back / 2 |
| Raw source frames | 85 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2830 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `a2e41dd0a2b9dc64cddba8ba7594ee1011dba23c9708224f37db97990798db48` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0084-snapcqc_s_new_com_asr_b2",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 84,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_b2",
    "hashId": "2a144c68bf5f2",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "back",
    "phase": 2,
    "phaseKind": "phase",
    "frameCount": 85,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.",
    "sourceMtarSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 14768,
        "sha256": "a2e41dd0a2b9dc64cddba8ba7594ee1011dba23c9708224f37db97990798db48"
      },
      {
        "extension": ".exchnk",
        "bytes": 2336,
        "sha256": "90ed0d3dd98a06558c9224fed169e7de41ca8f606ef4cfe3a74d52308c661dde"
      },
      {
        "extension": ".enchnk",
        "bytes": 640,
        "sha256": "3aad53907cdaf7abdefb8c4f56aeb846e37f8eb2b20321eef043ea4f55647004"
      }
    ],
    "displayTitle": "Snake CQC combo - back phase 2",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0084-snapcqc_s_new_com_asr_b2.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.83,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0084-snapcqc_s_new_com_asr_b2",
    "title": "Snake CQC combo - back phase 2",
    "shortIdentifier": "snapcqc_s_new_com_asr_b2",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_b2",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "2a144c68bf5f2",
    "sourceGaniSha256": "a2e41dd0a2b9dc64cddba8ba7594ee1011dba23c9708224f37db97990798db48",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "back",
    "phase": 2,
    "phaseKind": "phase",
    "rawFrameCount": 85,
    "decodedTrackCount": 18,
    "headerIndex": 62,
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
      42,
      44,
      46,
      48,
      50,
      52,
      54,
      56,
      58,
      60,
      62,
      64,
      66,
      68,
      70,
      72,
      74,
      76,
      78,
      80,
      82,
      84
    ],
    "endpointFrameSavedPrivately": 85,
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
    "gifDurationMilliseconds": 2830,
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
        -4.621862411499023,
        9.259695053100586,
        3.708273410797119
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.0816104412078857,
      "projectedMin": [
        -1.2154159545898438,
        -0.3361833691596985,
        0.35182997584342957
      ],
      "projectedMax": [
        -0.13143394887447357,
        1.4583083391189575,
        1.5649728775024414
      ]
    },
    "worldBounds": {
      "min": [
        -0.3204340934753418,
        0.3774655759334564,
        -0.011969804763793945
      ],
      "max": [
        0.47557881474494934,
        1.7921867370605469,
        1.6970624923706055
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0084-snapcqc_s_new_com_asr_b2.gif",
      "bytes": 3583777,
      "sha256": "a01e632e8bdd16248dfca3d0a581a6a13ec5748ad2c55f5ee917c5c84f130077"
    },
    "thumbnail": {
      "path": "player2_cqc-0084-snapcqc_s_new_com_asr_b2.png",
      "bytes": 132093,
      "sha256": "4c16b4aaddce7c430fa9286ad3eed2a394cdbad918c78a4c3b9727f2e3bb5efa"
    },
    "privateCleanGifSha256": "dd8b41489fa12ca7469f58cb1fe6b8a66296d79dec13c3ef517b97c0720b67ec",
    "privateRenderReceiptSha256": "d5b08dc002f5ae9ca28b5c73d695e992bd3bc83e10352c6aacf477acd62b47ac",
    "cleanPngFrameCount": 44,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
