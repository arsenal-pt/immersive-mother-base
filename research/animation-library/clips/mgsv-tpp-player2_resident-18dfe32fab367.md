# Special/zombie punch - player phase 1

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Special/zombie punch - player phase 1 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif)](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-18dfe32fab367` |
| Source archive | `player2_resident` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh` |
| Clip hash ID | `18dfe32fab367` |
| Original source role | player |
| Role interpretation | special_actor_punch_candidate |
| Family / phase | zombie_melee / None |
| Raw source frames | 60 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2000 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0` |
| GANI SHA-256 | `85ad59d986378d24a531a24f8e86a4183c1a5df5aba469ca36df811c67f73383` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_resident-1280-snapzmb_s_atk_pnh",
    "sourceArchive": "player2_resident",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 1280,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh",
    "hashId": "18dfe32fab367",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack",
    "frameCount": 60,
    "frameCountMethod": "GANI2 mini-header uint32 at offset0, consistent with mctrollin reader/previous adapter",
    "frameRate": null,
    "durationSeconds": null,
    "timingNote": "Raw frame count only. Runtime rate and transitions not measured.",
    "namingConfidence": "dictionary-resolved exact archive member",
    "interpretationConfidence": "candidate inferred from family names; not visual confirmation",
    "visualConfirmed": false,
    "nativePlaybackConfirmed": false,
    "relationshipNote": "Distinct special-actor/transition candidate; not an ordinary soldier combo proof.",
    "sourceMtarSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 8624,
        "sha256": "85ad59d986378d24a531a24f8e86a4183c1a5df5aba469ca36df811c67f73383"
      },
      {
        "extension": ".exchnk",
        "bytes": 192,
        "sha256": "8560faeb7d1ae8f8faba245c83712f068e7149391ef44008ad9a16e6c0ff23b3"
      },
      {
        "extension": ".enchnk",
        "bytes": 416,
        "sha256": "54941049f77bef9ce50704865239cd56752bf7d25bf2d9dfa23fb959ecaf4b65"
      }
    ],
    "displayTitle": "Special/zombie punch - player phase 1",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.0,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_resident-1280-snapzmb_s_atk_pnh",
    "title": "Special/zombie punch - player phase 1",
    "shortIdentifier": "snapzmb_s_atk_pnh",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh",
    "sourceArchive": "player2_resident",
    "sourceArchiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "hashId": "18dfe32fab367",
    "sourceGaniSha256": "85ad59d986378d24a531a24f8e86a4183c1a5df5aba469ca36df811c67f73383",
    "sourceRole": "player",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack",
    "rawFrameCount": 60,
    "decodedTrackCount": 18,
    "headerIndex": 465,
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
        -4.884105205535889,
        8.282171249389648,
        3.702364921569824
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.103710174560547,
      "projectedMin": [
        -0.3890284597873688,
        -0.14525564014911652,
        -0.37959519028663635
      ],
      "projectedMax": [
        0.4803098440170288,
        1.6682875156402588,
        0.9294732809066772
      ]
    },
    "worldBounds": {
      "min": [
        -0.5535133481025696,
        -0.5656096935272217,
        -0.006611347198486328
      ],
      "max": [
        0.46116113662719727,
        0.6044343113899231,
        1.6531368494033813
      ]
    },
    "titledGif": {
      "path": "player2_resident-1280-snapzmb_s_atk_pnh.gif",
      "bytes": 2720132,
      "sha256": "7794c13d2acff13304efcca2dca93decb411148c70a04f583553faf7732d6545"
    },
    "thumbnail": {
      "path": "player2_resident-1280-snapzmb_s_atk_pnh.png",
      "bytes": 139906,
      "sha256": "17534b7993c1f04a14d5fd85bb4ec326d6265fc4f4a26fd4a8f483669fb7e27c"
    },
    "privateCleanGifSha256": "d0aa7bf9a9fa6ca396c973d089a30c19ab2d2a7e1becbfacb9c4017182c8d036",
    "privateRenderReceiptSha256": "ffff1b60ca3adb179b265eed84d4d4d8d55174ac614d8b50fedca37cd80c0696",
    "cleanPngFrameCount": 31,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
