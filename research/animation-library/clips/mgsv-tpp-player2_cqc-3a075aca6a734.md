# Snake CQC combo - front phase 2

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 2 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-3a075aca6a734` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f2` |
| Clip hash ID | `3a075aca6a734` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | front / 2 |
| Raw source frames | 78 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2600 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `c0c88943e60826f9a3578f99da0f0c5af8a7490d306b08686ee54848a275b640` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0087-snapcqc_s_new_com_asr_f2",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 87,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f2",
    "hashId": "3a075aca6a734",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 2,
    "phaseKind": "phase",
    "frameCount": 78,
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
        "bytes": 13248,
        "sha256": "c0c88943e60826f9a3578f99da0f0c5af8a7490d306b08686ee54848a275b640"
      },
      {
        "extension": ".exchnk",
        "bytes": 2336,
        "sha256": "331b3e88d1726f66896b6aa666a5ed6b1f54ed5915af0fc4a77fda714cdf1003"
      },
      {
        "extension": ".enchnk",
        "bytes": 640,
        "sha256": "de3fa85655119f0fe808d278a2f9005c866494727e77f032b592aff02575cb8f"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 2",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0087-snapcqc_s_new_com_asr_f2.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.6,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0087-snapcqc_s_new_com_asr_f2",
    "title": "Snake CQC combo - front phase 2",
    "shortIdentifier": "snapcqc_s_new_com_asr_f2",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f2",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "3a075aca6a734",
    "sourceGaniSha256": "c0c88943e60826f9a3578f99da0f0c5af8a7490d306b08686ee54848a275b640",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 2,
    "phaseKind": "phase",
    "rawFrameCount": 78,
    "decodedTrackCount": 18,
    "headerIndex": 87,
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
      76
    ],
    "endpointFrameSavedPrivately": 78,
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
      70
    ],
    "gifDurationMilliseconds": 2600,
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
        -4.748138904571533,
        9.770801544189453,
        3.6218132972717285
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.1450705528259277,
      "projectedMin": [
        -1.403273344039917,
        -0.592470109462738,
        0.4232158660888672
      ],
      "projectedMax": [
        -0.24048951268196106,
        1.2567286491394043,
        2.41054105758667
      ]
    },
    "worldBounds": {
      "min": [
        -0.6193822622299194,
        0.5985494256019592,
        -0.011986255645751953
      ],
      "max": [
        0.42011427879333496,
        2.5801005363464355,
        1.6857664585113525
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0087-snapcqc_s_new_com_asr_f2.gif",
      "bytes": 3184768,
      "sha256": "a6e9d2eeccf9aef2fddbaa6443a55c92a756829b915d3d657b5714c789357eaf"
    },
    "thumbnail": {
      "path": "player2_cqc-0087-snapcqc_s_new_com_asr_f2.png",
      "bytes": 125368,
      "sha256": "d0cb0b26885f3ded53c83ce828c8db636392002739096af79efdf6a3518a94d3"
    },
    "privateCleanGifSha256": "06ae6ce9983088404a048c039ff19956e8477ce0315de774ffed3274fb84f721",
    "privateRenderReceiptSha256": "742bbd71a34cee49fb86d40b6fff2474f889b6ffd864024130650d7ccf0b3cab",
    "cleanPngFrameCount": 40,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
