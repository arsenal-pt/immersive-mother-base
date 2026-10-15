# Snake CQC combo - front phase 1

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 1 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-6b4ebb77250b` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1` |
| Clip hash ID | `6b4ebb77250b` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | front / 1 |
| Raw source frames | 60 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2000 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `559f6489aa6b151cf396df38b41cde798b2b8e5aad52fabeb091a991bde8438a` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0086-snapcqc_s_new_com_asr_f1",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 86,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1",
    "hashId": "6b4ebb77250b",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "phase",
    "frameCount": 60,
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
        "bytes": 9168,
        "sha256": "559f6489aa6b151cf396df38b41cde798b2b8e5aad52fabeb091a991bde8438a"
      },
      {
        "extension": ".exchnk",
        "bytes": 1920,
        "sha256": "d35a37612d7144be385002560a8f846912feec428174b59b41768b665837fa99"
      },
      {
        "extension": ".enchnk",
        "bytes": 496,
        "sha256": "3c968d291072202c0fe2a82d565151f7e8aa9c64b93a104058d5de12572cb694"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 1",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0086-snapcqc_s_new_com_asr_f1.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.0,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0086-snapcqc_s_new_com_asr_f1",
    "title": "Snake CQC combo - front phase 1",
    "shortIdentifier": "snapcqc_s_new_com_asr_f1",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "6b4ebb77250b",
    "sourceGaniSha256": "559f6489aa6b151cf396df38b41cde798b2b8e5aad52fabeb091a991bde8438a",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "phase",
    "rawFrameCount": 60,
    "decodedTrackCount": 18,
    "headerIndex": 6,
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
      58
    ],
    "endpointFrameSavedPrivately": 60,
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
      70
    ],
    "gifDurationMilliseconds": 2000,
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
        -4.775389671325684,
        9.152024269104004,
        3.6762051582336426
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 1.9988194704055786,
      "projectedMin": [
        -0.881744921207428,
        -0.3266662061214447,
        0.3318457007408142
      ],
      "projectedMax": [
        -0.09137308597564697,
        1.3964539766311646,
        1.5364446640014648
      ]
    },
    "worldBounds": {
      "min": [
        -0.29031094908714294,
        0.46035221219062805,
        -0.009550690650939941
      ],
      "max": [
        0.4320530295372009,
        1.4182286262512207,
        1.6926910877227783
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0086-snapcqc_s_new_com_asr_f1.gif",
      "bytes": 2539240,
      "sha256": "bb80655297a7d6a63765683fc1cfd18c7e620bdf167c3495efae45857b330fad"
    },
    "thumbnail": {
      "path": "player2_cqc-0086-snapcqc_s_new_com_asr_f1.png",
      "bytes": 130636,
      "sha256": "a580794e2fce4213dde23f037f5bf4fe6b61ffc5f6ff9c088dfdea0bbbae7de6"
    },
    "privateCleanGifSha256": "e4021a61dc272d52aa5f518312ffeacaca625ec8ee32fa9906038e468d59f53d",
    "privateRenderReceiptSha256": "daed1b4deb46956b89e87ff1561f66df4c1258469d1fa3176f7adca9a4c744ae",
    "cleanPngFrameCount": 31,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
