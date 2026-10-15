# NPC combo receiver - front phase 1

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![NPC combo receiver - front phase 1 — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-2cf6595afc1aa` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f1` |
| Clip hash ID | `2cf6595afc1aa` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
| Role interpretation | npc_combo_receiver_candidate |
| Family / phase | front / 1 |
| Raw source frames | 65 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2170 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `d9b388178a1ccf8b56a7acadbd5f6da9cad8fd1754bc50da2d092a586ce7ba88` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-0117-enemasr_s_new_com_asr_f1",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 117,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f1",
    "hashId": "2cf6595afc1aa",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "phase",
    "frameCount": 65,
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
        "bytes": 10672,
        "sha256": "d9b388178a1ccf8b56a7acadbd5f6da9cad8fd1754bc50da2d092a586ce7ba88"
      },
      {
        "extension": ".exchnk",
        "bytes": 800,
        "sha256": "110778263ff19f24e6a8aff2336f20a9e0e1ae428472f67e9537fe82cdd7cc41"
      },
      {
        "extension": ".enchnk",
        "bytes": 544,
        "sha256": "09ee787732681e7225488265007f88b3c49a70038b2275d2b9ee2f7f30d108e1"
      }
    ],
    "displayTitle": "NPC combo receiver - front phase 1",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-0117-enemasr_s_new_com_asr_f1.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.17,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-0117-enemasr_s_new_com_asr_f1",
    "title": "NPC combo receiver - front phase 1",
    "shortIdentifier": "enemasr_s_new_com_asr_f1",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f1",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "2cf6595afc1aa",
    "sourceGaniSha256": "d9b388178a1ccf8b56a7acadbd5f6da9cad8fd1754bc50da2d092a586ce7ba88",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "front",
    "phase": 1,
    "phaseKind": "phase",
    "rawFrameCount": 65,
    "decodedTrackCount": 18,
    "headerIndex": 965,
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
      64
    ],
    "endpointFrameSavedPrivately": 65,
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
      40
    ],
    "gifDurationMilliseconds": 2170,
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
        -4.529630184173584,
        10.554056167602539,
        3.6115336418151855
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.4739952087402344,
      "projectedMin": [
        -2.292506217956543,
        -0.9080134630203247,
        0.7637200951576233
      ],
      "projectedMax": [
        -0.518061637878418,
        1.2247411012649536,
        3.148529529571533
      ]
    },
    "worldBounds": {
      "min": [
        -0.31553107500076294,
        1.0969048738479614,
        -0.030245184898376465
      ],
      "max": [
        0.834081768989563,
        3.8509349822998047,
        1.6636334657669067
      ]
    },
    "titledGif": {
      "path": "Soldier_common-0117-enemasr_s_new_com_asr_f1.gif",
      "bytes": 2659436,
      "sha256": "9dcbfedf45ef1d146af916b2ffa333429ba26e9b989397c20690ce2e84d39cc7"
    },
    "thumbnail": {
      "path": "Soldier_common-0117-enemasr_s_new_com_asr_f1.png",
      "bytes": 123089,
      "sha256": "3d3cf398a0f36ca27e85baae252268dd5d1132584bf598dd3a0e8ee9fb149681"
    },
    "privateCleanGifSha256": "f40f198e001855327c886e69443bb994876f2d3956def1e2e53427a6b3932283",
    "privateRenderReceiptSha256": "b2237c515cd62d8c01c7c84b50254e18a17eca669a23d9a140e793dbfba41cdc",
    "cleanPngFrameCount": 34,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
