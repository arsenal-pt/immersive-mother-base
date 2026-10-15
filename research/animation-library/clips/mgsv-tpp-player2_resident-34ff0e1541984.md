# Special/zombie punch - player ending

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Special/zombie punch - player ending — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.gif)](../../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-34ff0e1541984` |
| Source archive | `player2_resident` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh_ed` |
| Clip hash ID | `34ff0e1541984` |
| Original source role | player |
| Role interpretation | special_actor_punch_candidate |
| Family / phase | zombie_melee / None |
| Raw source frames | 15 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 500 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0` |
| GANI SHA-256 | `abd860c6bcb69a6b46f73604870ab6492463c1350ca494ad2bdc82a67fae8ccf` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_resident-1282-snapzmb_s_atk_pnh_ed",
    "sourceArchive": "player2_resident",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 1282,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh_ed",
    "hashId": "34ff0e1541984",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "ending",
    "frameCount": 15,
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
        "bytes": 3808,
        "sha256": "abd860c6bcb69a6b46f73604870ab6492463c1350ca494ad2bdc82a67fae8ccf"
      },
      {
        "extension": ".exchnk",
        "bytes": 192,
        "sha256": "d13ec3abaf242936a528ff5f3be50dd2952ac4e35d2c553f7843c8ca57fcdcf3"
      },
      {
        "extension": ".enchnk",
        "bytes": 320,
        "sha256": "7e3b9130fa2f804827a455e5657389327753ba57e9c1f0effa1b3bd3d6ed67bf"
      }
    ],
    "displayTitle": "Special/zombie punch - player ending",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_resident-1282-snapzmb_s_atk_pnh_ed.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 0.5,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_resident-1282-snapzmb_s_atk_pnh_ed",
    "title": "Special/zombie punch - player ending",
    "shortIdentifier": "snapzmb_s_atk_pnh_ed",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh_ed",
    "sourceArchive": "player2_resident",
    "sourceArchiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
    "hashId": "34ff0e1541984",
    "sourceGaniSha256": "abd860c6bcb69a6b46f73604870ab6492463c1350ca494ad2bdc82a67fae8ccf",
    "sourceRole": "player",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "ending",
    "rawFrameCount": 15,
    "decodedTrackCount": 18,
    "headerIndex": 1043,
    "sourceFramesSampled": [
      0,
      2,
      4,
      6,
      8,
      10,
      12,
      14
    ],
    "endpointFrameSavedPrivately": 15,
    "chosenSourceFramesPerSecond": 30,
    "gifFrameDurationsMilliseconds": [
      70,
      60,
      70,
      70,
      60,
      70,
      70,
      30
    ],
    "gifDurationMilliseconds": 500,
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
        -4.848073959350586,
        8.317708969116211,
        3.6679508686065674
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 1.9926544427871704,
      "projectedMin": [
        -0.37576454877853394,
        -0.1339578628540039,
        -0.3590342104434967
      ],
      "projectedMax": [
        0.3689873516559601,
        1.5838476419448853,
        0.9130038619041443
      ]
    },
    "worldBounds": {
      "min": [
        -0.5050198435783386,
        -0.4170706868171692,
        -0.004004240036010742
      ],
      "max": [
        0.391670286655426,
        0.5966891050338745,
        1.6531368494033813
      ]
    },
    "titledGif": {
      "path": "player2_resident-1282-snapzmb_s_atk_pnh_ed.gif",
      "bytes": 735524,
      "sha256": "f83e3e0dc31a99a01c09d80f0841b14366dfc4931145e4689a192eac09defc79"
    },
    "thumbnail": {
      "path": "player2_resident-1282-snapzmb_s_atk_pnh_ed.png",
      "bytes": 143905,
      "sha256": "c312ecde8ba7e912f6963d70288ba8b4a4f83ce94e32dc462393b51eba416ba2"
    },
    "privateCleanGifSha256": "7a63f490a2bb845894f54d5c090e34f734e132a14ff3c619c2fd7f7fb164dad5",
    "privateRenderReceiptSha256": "8377ddce02e461fe4d845413bce5aac4b6dee03706b112ec3e5f042ff496b94a",
    "cleanPngFrameCount": 9,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
