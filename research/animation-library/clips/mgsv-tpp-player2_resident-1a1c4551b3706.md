# Snake CQC combo - front phase 5

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 5 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.gif)](../../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-1a1c4551b3706` |
| Source archive | `player2_resident` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f5` |
| Clip hash ID | `1a1c4551b3706` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | front / 5 |
| Raw source frames | 105 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 3500 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0` |
| GANI SHA-256 | `959df67edf0edc1ed2e48df021ca164f78ab2d5921acf76a09c739c82993814a` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_resident-0228-snapcqc_s_new_com_asr_f5",
    "sourceArchive": "player2_resident",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 228,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f5",
    "hashId": "1a1c4551b3706",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 5,
    "phaseKind": "phase",
    "frameCount": 105,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.",
    "sourceMtarSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 21360,
        "sha256": "959df67edf0edc1ed2e48df021ca164f78ab2d5921acf76a09c739c82993814a"
      },
      {
        "extension": ".exchnk",
        "bytes": 2880,
        "sha256": "dfe924705bfe995506dde9812667ebfcf16517141586d0a5cec14897a20cb5b9"
      },
      {
        "extension": ".enchnk",
        "bytes": 784,
        "sha256": "7dfceb191880ae31db8d818842198711265cde3ff392fa814557eb63f2e268ca"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 5",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_resident-0228-snapcqc_s_new_com_asr_f5.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 3.5,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_resident-0228-snapcqc_s_new_com_asr_f5",
    "title": "Snake CQC combo - front phase 5",
    "shortIdentifier": "snapcqc_s_new_com_asr_f5",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f5",
    "sourceArchive": "player2_resident",
    "sourceArchiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "hashId": "1a1c4551b3706",
    "sourceGaniSha256": "959df67edf0edc1ed2e48df021ca164f78ab2d5921acf76a09c739c82993814a",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 5,
    "phaseKind": "phase",
    "rawFrameCount": 105,
    "decodedTrackCount": 18,
    "headerIndex": 487,
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
      84,
      86,
      88,
      90,
      92,
      94,
      96,
      98,
      100,
      102,
      104
    ],
    "endpointFrameSavedPrivately": 105,
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
      30
    ],
    "gifDurationMilliseconds": 3500,
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
        -4.905694961547852,
        13.910687446594238,
        3.6888716220855713
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.3981242179870605,
      "projectedMin": [
        -3.4660804271698,
        -1.6951615810394287,
        3.7340219020843506
      ],
      "projectedMax": [
        -2.0774338245391846,
        0.37218689918518066,
        6.136407852172852
      ]
    },
    "worldBounds": {
      "min": [
        -0.5520486831665039,
        4.497485160827637,
        -0.011938929557800293
      ],
      "max": [
        0.40660786628723145,
        6.8922014236450195,
        1.686340093612671
      ]
    },
    "titledGif": {
      "path": "player2_resident-0228-snapcqc_s_new_com_asr_f5.gif",
      "bytes": 4167737,
      "sha256": "54fb0e1ecc8ee6cd00fb0c6de7400be855b014bb5d66bcedfe34614ce7be0c55"
    },
    "thumbnail": {
      "path": "player2_resident-0228-snapcqc_s_new_com_asr_f5.png",
      "bytes": 108774,
      "sha256": "d597c1620e0434a76dd8f47ae5a0781b2c109cc6608fc13160f0451b80b14fd8"
    },
    "privateCleanGifSha256": "bc2bf9d2054b8dced190cf6faa0da6bc44959d77a0f1c6c24566148a802e1e68",
    "privateRenderReceiptSha256": "d91fbdf4ab956f2f1565bdf09b528100980a4b01eb9cfcb9d41260b17e1b98e3",
    "cleanPngFrameCount": 54,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
