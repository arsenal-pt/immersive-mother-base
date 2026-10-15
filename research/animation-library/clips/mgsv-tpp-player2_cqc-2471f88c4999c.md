# Snake CQC combo - front phase 4

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 4 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-2471f88c4999c` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f4` |
| Clip hash ID | `2471f88c4999c` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | front / 4 |
| Raw source frames | 85 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2830 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `a6d95a5d1bd3c3890aa35e7d244bee291b2644c57a9d988ff99750ce9eb05bd6` |

## Interpretation and limits

Equal front/back phase suffix is a proposed attacker/receiver correspondence; native contact/timing not proved.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0089-snapcqc_s_new_com_asr_f4",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 89,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f4",
    "hashId": "2471f88c4999c",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 4,
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
        "bytes": 13936,
        "sha256": "a6d95a5d1bd3c3890aa35e7d244bee291b2644c57a9d988ff99750ce9eb05bd6"
      },
      {
        "extension": ".exchnk",
        "bytes": 2496,
        "sha256": "6d4dc2ae04f0c5b03c7297e0f72344b073b9e15fa3212bc0b2a4d775c8eec8ce"
      },
      {
        "extension": ".enchnk",
        "bytes": 656,
        "sha256": "9fd1d4e5e000e3de187ecc756ccd56d41e8b6643aa44bb9e66459f95f21d2a2e"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 4",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0089-snapcqc_s_new_com_asr_f4.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.83,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0089-snapcqc_s_new_com_asr_f4",
    "title": "Snake CQC combo - front phase 4",
    "shortIdentifier": "snapcqc_s_new_com_asr_f4",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_new_com_asr_f4",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "2471f88c4999c",
    "sourceGaniSha256": "a6d95a5d1bd3c3890aa35e7d244bee291b2644c57a9d988ff99750ce9eb05bd6",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "front",
    "phase": 4,
    "phaseKind": "phase",
    "rawFrameCount": 85,
    "decodedTrackCount": 18,
    "headerIndex": 55,
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
        -4.818479537963867,
        12.533623695373535,
        3.624034881591797
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.3288822174072266,
      "projectedMin": [
        -2.8815650939941406,
        -1.3704415559768677,
        2.6032230854034424
      ],
      "projectedMax": [
        -1.4248924255371094,
        0.6372154951095581,
        4.86838436126709
      ]
    },
    "worldBounds": {
      "min": [
        -0.4882067143917084,
        3.1675291061401367,
        -0.01854419708251953
      ],
      "max": [
        0.38715893030166626,
        5.453547477722168,
        1.693939208984375
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0089-snapcqc_s_new_com_asr_f4.gif",
      "bytes": 3460281,
      "sha256": "e2dfa3f7170bcfc655ecdcfa5d2ceb70b41dab636ea0bb3bb35cbf1334b39868"
    },
    "thumbnail": {
      "path": "player2_cqc-0089-snapcqc_s_new_com_asr_f4.png",
      "bytes": 119235,
      "sha256": "d580626b4054f67433fac5df1b51bddd9cb94ef39085c549d6f0d13aba533aed"
    },
    "privateCleanGifSha256": "8a149c740ca4f9eeeb96d8302230dd6ab2e0e39a145cd318de2ae399f5f569a2",
    "privateRenderReceiptSha256": "b047afa42faf64fe6a9e5c110fad488d740a9e669aed27efd5bc2948da58acc7",
    "cleanPngFrameCount": 44,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
