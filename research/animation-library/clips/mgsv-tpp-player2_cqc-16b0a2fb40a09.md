# Snake CQC combo - front phase 1 end

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC combo - front phase 1 end — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-16b0a2fb40a09` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_f1_ed` |
| Clip hash ID | `16b0a2fb40a09` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | related_combo_transition / None |
| Raw source frames | 30 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 1000 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `4ee7d2b62c9dc5a63e91960dc781ffb1e6ca66279b0f68d0d06ede626eee1796` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0079-snapcqc_s_com_f1_ed",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 79,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_f1_ed",
    "hashId": "16b0a2fb40a09",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "related_combo_transition",
    "phase": null,
    "phaseKind": "ending",
    "frameCount": 30,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Distinct special-actor/transition candidate; not an ordinary soldier combo proof.",
    "sourceMtarSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 6704,
        "sha256": "4ee7d2b62c9dc5a63e91960dc781ffb1e6ca66279b0f68d0d06ede626eee1796"
      },
      {
        "extension": ".exchnk",
        "bytes": 1248,
        "sha256": "2b8ec53c57fb241c4f63ea1b0a470baae0dcc37474e614b94a0a0faa524983aa"
      },
      {
        "extension": ".enchnk",
        "bytes": 336,
        "sha256": "1637f6b7b95bfa88e37c1767a0adfff274772ce741bc5b2aeca30c3daa8ec7fe"
      }
    ],
    "displayTitle": "Snake CQC combo - front phase 1 end",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0079-snapcqc_s_com_f1_ed.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 1.0,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0079-snapcqc_s_com_f1_ed",
    "title": "Snake CQC combo - front phase 1 end",
    "shortIdentifier": "snapcqc_s_com_f1_ed",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_f1_ed",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "16b0a2fb40a09",
    "sourceGaniSha256": "4ee7d2b62c9dc5a63e91960dc781ffb1e6ca66279b0f68d0d06ede626eee1796",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "related_combo_transition",
    "phase": null,
    "phaseKind": "ending",
    "rawFrameCount": 30,
    "decodedTrackCount": 18,
    "headerIndex": 33,
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
      28
    ],
    "endpointFrameSavedPrivately": 30,
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
      70
    ],
    "gifDurationMilliseconds": 1000,
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
        -4.774507999420166,
        9.153257369995117,
        3.6746106147766113
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 1.994861125946045,
      "projectedMin": [
        -0.8821545839309692,
        -0.3266662061214447,
        0.3318457007408142
      ],
      "projectedMax": [
        -0.09372983872890472,
        1.3930416107177734,
        1.5367112159729004
      ]
    },
    "worldBounds": {
      "min": [
        -0.29015710949897766,
        0.4609157145023346,
        -0.009096026420593262
      ],
      "max": [
        0.41937848925590515,
        1.4186408519744873,
        1.6838397979736328
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0079-snapcqc_s_com_f1_ed.gif",
      "bytes": 1275602,
      "sha256": "77bcb607a6537ff0d9a2d57e9113cf57695b5bc649cf99df13a4057ecc12b505"
    },
    "thumbnail": {
      "path": "player2_cqc-0079-snapcqc_s_com_f1_ed.png",
      "bytes": 130306,
      "sha256": "3fd8071451792dfae06d93ba131692bfd7e36dbb1ed76d25fc49cf2be24705d4"
    },
    "privateCleanGifSha256": "e40f2f08a8cbd08042c912c314ad5d6ce1c38a5bb18583de15045943aef58eda",
    "privateRenderReceiptSha256": "72d8482137917183aa8accd66b1af9214bd9c45e5edc7a00f5d938a7d25f4f3b",
    "cleanPngFrameCount": 16,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
