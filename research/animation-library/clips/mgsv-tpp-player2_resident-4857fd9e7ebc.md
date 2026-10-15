# Snake CQC combo - front phase 1 start

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 1 start — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.gif)](../../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-4857fd9e7ebc` |
| Source archive | `player2_resident` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1_st` |
| Clip hash ID | `4857fd9e7ebc` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | front / 1 |
| Raw source frames | 25 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 830 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0` |
| GANI SHA-256 | `b21e279f226b0eb59ea8fbc174c4b030e64e0cc16d51957399e5bd17edc48260` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_resident-0227-snapcqc_s_new_com_asr_f1_st",
    "sourceArchive": "player2_resident",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 227,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1_st",
    "hashId": "4857fd9e7ebc",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "start",
    "frameCount": 25,
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
        "bytes": 6176,
        "sha256": "b21e279f226b0eb59ea8fbc174c4b030e64e0cc16d51957399e5bd17edc48260"
      },
      {
        "extension": ".exchnk",
        "bytes": 1056,
        "sha256": "eda32fe2985371fb63e48fc219b7367cbdd3dd95a7df94de25f6dcfcbe3a7d87"
      },
      {
        "extension": ".enchnk",
        "bytes": 416,
        "sha256": "3a8dc0033e8ef92b0529155a6664416b4372331e7290a1e21ca474eefd61501a"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 1 start",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_resident-0227-snapcqc_s_new_com_asr_f1_st.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 0.83,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_resident-0227-snapcqc_s_new_com_asr_f1_st",
    "title": "Snake CQC combo - front phase 1 start",
    "shortIdentifier": "snapcqc_s_new_com_asr_f1_st",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f1_st",
    "sourceArchive": "player2_resident",
    "sourceArchiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "hashId": "4857fd9e7ebc",
    "sourceGaniSha256": "b21e279f226b0eb59ea8fbc174c4b030e64e0cc16d51957399e5bd17edc48260",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "start",
    "rawFrameCount": 25,
    "decodedTrackCount": 18,
    "headerIndex": 83,
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
      24
    ],
    "endpointFrameSavedPrivately": 25,
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
      30
    ],
    "gifDurationMilliseconds": 830,
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
        -4.748749732971191,
        8.806422233581543,
        3.689448356628418
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.1740121841430664,
      "projectedMin": [
        -0.8814355134963989,
        -0.29923057556152344,
        -0.25050488114356995
      ],
      "projectedMax": [
        0.21057310700416565,
        1.5749177932739258,
        1.5292612314224243
      ]
    },
    "worldBounds": {
      "min": [
        -0.3582620322704315,
        -0.2764163017272949,
        -0.010796308517456055
      ],
      "max": [
        0.4804127514362335,
        1.3993628025054932,
        1.681931734085083
      ]
    },
    "titledGif": {
      "path": "player2_resident-0227-snapcqc_s_new_com_asr_f1_st.gif",
      "bytes": 1122108,
      "sha256": "c59a0862298f8e508dea2f3e150a2852f4a67f517d6229090d027e0423613ad0"
    },
    "thumbnail": {
      "path": "player2_resident-0227-snapcqc_s_new_com_asr_f1_st.png",
      "bytes": 123900,
      "sha256": "a385b3e2742c33682f143c2f6a26c2bbfd6498c25a3b10c6a9592803d8b4cd57"
    },
    "privateCleanGifSha256": "e7ed6edf5c82b5508ee6934b528675d22ae1a7851ff31cda8dcde72ed00566bc",
    "privateRenderReceiptSha256": "affa36a743e220acce5d98c3caaae834dbbed27e9b7ea7f5a075fa506d18b9c5",
    "cleanPngFrameCount": 14,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
