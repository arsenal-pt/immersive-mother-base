# NPC combo receiver - back phase 3

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![NPC combo receiver - back phase 3 — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-369dec61164bd` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b3` |
| Clip hash ID | `369dec61164bd` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
| Role interpretation | npc_combo_receiver_candidate |
| Family / phase | back / 3 |
| Raw source frames | 120 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 4000 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `f2ad1b1313a4a5bf306d94e3f389d9b11cbe5cf6795211be14e3c6d2f1ebc45a` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-0116-enemasr_s_new_com_asr_b3",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 116,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b3",
    "hashId": "369dec61164bd",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "back",
    "phase": 3,
    "phaseKind": "phase",
    "frameCount": 120,
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
        "bytes": 19664,
        "sha256": "f2ad1b1313a4a5bf306d94e3f389d9b11cbe5cf6795211be14e3c6d2f1ebc45a"
      },
      {
        "extension": ".exchnk",
        "bytes": 1648,
        "sha256": "adbe1c2fa94db3a15c37f6dc6a1f23540aa1e8c368550d91ad5dc1ad263b91f3"
      },
      {
        "extension": ".enchnk",
        "bytes": 736,
        "sha256": "ada51c2dd5bb8419da38d5767f513a6684183ff881d7ac6e570dfdb14b02f596"
      }
    ],
    "displayTitle": "NPC combo receiver - back phase 3",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-0116-enemasr_s_new_com_asr_b3.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 4.0,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-0116-enemasr_s_new_com_asr_b3",
    "title": "NPC combo receiver - back phase 3",
    "shortIdentifier": "enemasr_s_new_com_asr_b3",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_b3",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "369dec61164bd",
    "sourceGaniSha256": "f2ad1b1313a4a5bf306d94e3f389d9b11cbe5cf6795211be14e3c6d2f1ebc45a",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "back",
    "phase": 3,
    "phaseKind": "phase",
    "rawFrameCount": 120,
    "decodedTrackCount": 18,
    "headerIndex": 1137,
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
      104,
      106,
      108,
      110,
      112,
      114,
      116,
      118
    ],
    "endpointFrameSavedPrivately": 120,
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
      60,
      70,
      70,
      60,
      70,
      70,
      60,
      70
    ],
    "gifDurationMilliseconds": 4000,
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
        -5.130742073059082,
        10.599736213684082,
        3.604611873626709
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.4836902618408203,
      "projectedMin": [
        -1.7523661851882935,
        -1.017886757850647,
        1.133589267730713
      ],
      "projectedMax": [
        -0.06578081846237183,
        1.1232255697250366,
        3.430039882659912
      ]
    },
    "worldBounds": {
      "min": [
        -1.2979280948638916,
        1.4684364795684814,
        -0.0993397980928421
      ],
      "max": [
        0.5174920558929443,
        3.5605456829071045,
        1.6326065063476562
      ]
    },
    "titledGif": {
      "path": "Soldier_common-0116-enemasr_s_new_com_asr_b3.gif",
      "bytes": 4647726,
      "sha256": "d7984186d5f102d232fd106db24280060a27cae881e46bff360501e70377f252"
    },
    "thumbnail": {
      "path": "Soldier_common-0116-enemasr_s_new_com_asr_b3.png",
      "bytes": 123427,
      "sha256": "9d5d72855cd03b36299331ab580c6b9229e0ec1de305a4c5f511207579f0bc2e"
    },
    "privateCleanGifSha256": "2c82e35a47ea4030246bc763dc1ccb8523c1106778258c9a72887e28644c696a",
    "privateRenderReceiptSha256": "0df28b33aabbba1d68c8a3c67d430834be464226f592dc9957062acc8b01162e",
    "cleanPngFrameCount": 61,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
