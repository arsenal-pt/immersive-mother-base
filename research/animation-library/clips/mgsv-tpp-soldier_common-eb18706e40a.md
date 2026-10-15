# NPC combo receiver - back phase 1

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![NPC combo receiver - back phase 1 — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-eb18706e40a` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b1` |
| Clip hash ID | `eb18706e40a` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
| Role interpretation | npc_combo_receiver_candidate |
| Family / phase | back / 1 |
| Raw source frames | 87 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2900 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `1cdf99914b769209550fa4a3d9919d7d829f53ead46a16b86db6765f5d457552` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-0114-enemasr_s_new_com_asr_b1",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 114,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b1",
    "hashId": "eb18706e40a",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "back",
    "phase": 1,
    "phaseKind": "phase",
    "frameCount": 87,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.",
    "sourceMtarSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 14784,
        "sha256": "1cdf99914b769209550fa4a3d9919d7d829f53ead46a16b86db6765f5d457552"
      },
      {
        "extension": ".exchnk",
        "bytes": 608,
        "sha256": "dcf3be1e78fff5eefc64b8c027c113f55237780fedf273b8d4a02e5d0b62c4de"
      },
      {
        "extension": ".enchnk",
        "bytes": 528,
        "sha256": "203fb6ea28286de099cc094710523f7d2833a715bf0ea465440b31e37983a069"
      }
    ],
    "displayTitle": "NPC combo receiver - back phase 1",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-0114-enemasr_s_new_com_asr_b1.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.9,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-0114-enemasr_s_new_com_asr_b1",
    "title": "NPC combo receiver - back phase 1",
    "shortIdentifier": "enemasr_s_new_com_asr_b1",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b1",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "eb18706e40a",
    "sourceGaniSha256": "1cdf99914b769209550fa4a3d9919d7d829f53ead46a16b86db6765f5d457552",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "back",
    "phase": 1,
    "phaseKind": "phase",
    "rawFrameCount": 87,
    "decodedTrackCount": 18,
    "headerIndex": 16,
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
      86
    ],
    "endpointFrameSavedPrivately": 87,
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
      30
    ],
    "gifDurationMilliseconds": 2900,
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
        -4.6379714012146,
        10.562454223632812,
        3.705127000808716
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.5714006423950195,
      "projectedMin": [
        -2.0398459434509277,
        -0.8783066272735596,
        1.0345478057861328
      ],
      "projectedMax": [
        -0.5920198559761047,
        1.3384180068969727,
        3.0502679347991943
      ]
    },
    "worldBounds": {
      "min": [
        -0.4414924383163452,
        1.3351529836654663,
        -0.04087173938751221
      ],
      "max": [
        0.7003380656242371,
        3.634955883026123,
        1.7877349853515625
      ]
    },
    "titledGif": {
      "path": "Soldier_common-0114-enemasr_s_new_com_asr_b1.gif",
      "bytes": 3612515,
      "sha256": "59963a0361d9c35734386b0d0eb723654484078150affa75708281441c932f3f"
    },
    "thumbnail": {
      "path": "Soldier_common-0114-enemasr_s_new_com_asr_b1.png",
      "bytes": 116407,
      "sha256": "0b5a98b48309840691af6a175ba44e2e51d8cabd8e34c71199ab55d77dac3ac3"
    },
    "privateCleanGifSha256": "1b08b1b1e924e96f3715da226400c0de76d946148108ef484b7a98c40dd29a03",
    "privateRenderReceiptSha256": "51c580d0a17e450debda5aba8420a2b1bf400f241837f84b87c4af820f175ddb",
    "cleanPngFrameCount": 45,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
