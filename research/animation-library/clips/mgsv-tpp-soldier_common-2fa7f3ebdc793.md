# NPC combo receiver - front phase 2

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![NPC combo receiver - front phase 2 — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-2fa7f3ebdc793` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f2` |
| Clip hash ID | `2fa7f3ebdc793` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
| Role interpretation | npc_combo_receiver_candidate |
| Family / phase | front / 2 |
| Raw source frames | 90 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 3000 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `eb8590c384bdcdc1c719dbc9fe22f8ee5030714e3859a0fc4c638ed31fb87fbe` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-0118-enemasr_s_new_com_asr_f2",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 118,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f2",
    "hashId": "2fa7f3ebdc793",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "front",
    "phase": 2,
    "phaseKind": "phase",
    "frameCount": 90,
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
        "bytes": 16288,
        "sha256": "eb8590c384bdcdc1c719dbc9fe22f8ee5030714e3859a0fc4c638ed31fb87fbe"
      },
      {
        "extension": ".exchnk",
        "bytes": 1008,
        "sha256": "1c6297fb216ff134a19426f8a8f02ae3b6af6545eb0d6850bebbdf4eb12504db"
      },
      {
        "extension": ".enchnk",
        "bytes": 560,
        "sha256": "4f429c99f7e2230fae40daa13a954ad9aa9b915d971ea318b5044c52c06befc6"
      }
    ],
    "displayTitle": "NPC combo receiver - front phase 2",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-0118-enemasr_s_new_com_asr_f2.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 3.0,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-0118-enemasr_s_new_com_asr_f2",
    "title": "NPC combo receiver - front phase 2",
    "shortIdentifier": "enemasr_s_new_com_asr_f2",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enem/enemasr/enemasr_s_new_com_asr_f2",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "2fa7f3ebdc793",
    "sourceGaniSha256": "eb8590c384bdcdc1c719dbc9fe22f8ee5030714e3859a0fc4c638ed31fb87fbe",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "npc_combo_receiver_candidate",
    "sequenceFamily": "front",
    "phase": 2,
    "phaseKind": "phase",
    "rawFrameCount": 90,
    "decodedTrackCount": 18,
    "headerIndex": 1010,
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
      88
    ],
    "endpointFrameSavedPrivately": 90,
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
      70
    ],
    "gifDurationMilliseconds": 3000,
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
        -4.810617923736572,
        11.314666748046875,
        3.6520626544952393
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.604717254638672,
      "projectedMin": [
        -2.552243947982788,
        -1.1566632986068726,
        1.493536353111267
      ],
      "projectedMax": [
        -0.5394017100334167,
        1.0887826681137085,
        3.9709949493408203
      ]
    },
    "worldBounds": {
      "min": [
        -0.5765055418014526,
        1.6909878253936768,
        -0.04045557975769043
      ],
      "max": [
        0.9334349632263184,
        4.723995208740234,
        1.6977765560150146
      ]
    },
    "titledGif": {
      "path": "Soldier_common-0118-enemasr_s_new_com_asr_f2.gif",
      "bytes": 3536206,
      "sha256": "38155129fb57f3fc01853328651b0a493a3c187f2b584989db9f319057841b7e"
    },
    "thumbnail": {
      "path": "Soldier_common-0118-enemasr_s_new_com_asr_f2.png",
      "bytes": 109571,
      "sha256": "04abeb86a0a6e886cbfe8e60c5825290d467c7d809a9955e536c31888721a924"
    },
    "privateCleanGifSha256": "711e506603712b92b079ce54656b0a8e1e509cd57c9080090290b906381129d8",
    "privateRenderReceiptSha256": "4686052d9cc4be5e15e60f65830bb94d33dab79b5d2610c8b9fb10dfd461437d",
    "cleanPngFrameCount": 46,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
