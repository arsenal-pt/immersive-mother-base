# Special/zombie punch - enemy ending

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Special/zombie punch - enemy ending — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-3f61b4434967` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh_ed` |
| Clip hash ID | `3f61b4434967` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
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
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `63afcbd0f9485e3097bd3a67a30abb26c9d48387a2205168df5b66ceff5d490f` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-1313-enetzmb_s_atk_pnh_ed",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 1313,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh_ed",
    "hashId": "3f61b4434967",
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
    "sourceMtarSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "payloads": [
      {
        "extension": ".gani",
        "bytes": 3888,
        "sha256": "63afcbd0f9485e3097bd3a67a30abb26c9d48387a2205168df5b66ceff5d490f"
      },
      {
        "extension": ".enchnk",
        "bytes": 384,
        "sha256": "8f9a9d2ebb5b89b0bb98c9fbcec6553fc35c17d3dc5e4a51eda0fadfd7f0a0dd"
      }
    ],
    "displayTitle": "Special/zombie punch - enemy ending",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-1313-enetzmb_s_atk_pnh_ed.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 0.5,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-1313-enetzmb_s_atk_pnh_ed",
    "title": "Special/zombie punch - enemy ending",
    "shortIdentifier": "enetzmb_s_atk_pnh_ed",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh_ed",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "3f61b4434967",
    "sourceGaniSha256": "63afcbd0f9485e3097bd3a67a30abb26c9d48387a2205168df5b66ceff5d490f",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "ending",
    "rawFrameCount": 15,
    "decodedTrackCount": 18,
    "headerIndex": 92,
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
        -4.855048656463623,
        7.939146518707275,
        3.70546555519104
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 1.9474152326583862,
      "projectedMin": [
        -0.28748610615730286,
        0.015062302350997925,
        -0.7593134045600891
      ],
      "projectedMax": [
        0.6742512583732605,
        1.6938685178756714,
        0.7157175540924072
      ]
    },
    "worldBounds": {
      "min": [
        -0.48272350430488586,
        -0.8005032539367676,
        -0.008784174919128418
      ],
      "max": [
        0.5065838694572449,
        0.3301178216934204,
        1.697941780090332
      ]
    },
    "titledGif": {
      "path": "Soldier_common-1313-enetzmb_s_atk_pnh_ed.gif",
      "bytes": 760089,
      "sha256": "92660f98619ed178975bd22d34db8ab92b6b91f986818e26a8b7d93400121773"
    },
    "thumbnail": {
      "path": "Soldier_common-1313-enetzmb_s_atk_pnh_ed.png",
      "bytes": 145407,
      "sha256": "885fbfc70ea780ac4e878af7af99c93e7dd2b65441e08bcf034b5d30e6521727"
    },
    "privateCleanGifSha256": "0d253a053cac91768c2f0789d6c63b96c44b3d2b3105a8a185b485036a949fc8",
    "privateRenderReceiptSha256": "f64178397890f86f0e2df94359f25202af7a6de47e3f5a1346514f8af09273a9",
    "cleanPngFrameCount": 9,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
