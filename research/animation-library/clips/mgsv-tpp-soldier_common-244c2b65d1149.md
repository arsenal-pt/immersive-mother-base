# Special/zombie punch - enemy phase 2

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Special/zombie punch - enemy phase 2 — full-character offline preview](../../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.gif)](../../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.gif) · [Still image](../../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-soldier_common-244c2b65d1149` |
| Source archive | `Soldier_common` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh2` |
| Clip hash ID | `244c2b65d1149` |
| Original source role | Soldier2Common archive (membership does not prove actor use) |
| Role interpretation | special_actor_punch_candidate |
| Family / phase | zombie_melee / None |
| Raw source frames | 43 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 1430 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e` |
| GANI SHA-256 | `05339d4f98c01ef68cdace9eda7db2dc1a9ca1f94a0bd9bd892159117b9d17d7` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "Soldier_common-1312-enetzmb_s_atk_pnh2",
    "sourceArchive": "Soldier_common",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "archiveOrdinalZeroBased": 1312,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh2",
    "hashId": "244c2b65d1149",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack2",
    "frameCount": 43,
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
        "bytes": 6512,
        "sha256": "05339d4f98c01ef68cdace9eda7db2dc1a9ca1f94a0bd9bd892159117b9d17d7"
      },
      {
        "extension": ".enchnk",
        "bytes": 400,
        "sha256": "f25a0926d659d1b2e6e4907179077d5c162c5280d4caa69c2d1edb9a4e577cbf"
      }
    ],
    "displayTitle": "Special/zombie punch - enemy phase 2",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/Soldier_common-1312-enetzmb_s_atk_pnh2.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 1.43,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "Soldier_common-1312-enetzmb_s_atk_pnh2",
    "title": "Special/zombie punch - enemy phase 2",
    "shortIdentifier": "enetzmb_s_atk_pnh2",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetzmb/enetzmb_s_atk_pnh2",
    "sourceArchive": "Soldier_common",
    "sourceArchiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "hashId": "244c2b65d1149",
    "sourceGaniSha256": "05339d4f98c01ef68cdace9eda7db2dc1a9ca1f94a0bd9bd892159117b9d17d7",
    "sourceRole": "Soldier2Common archive (membership does not prove actor use)",
    "role": "special_actor_punch_candidate",
    "sequenceFamily": "zombie_melee",
    "phase": null,
    "phaseKind": "attack2",
    "rawFrameCount": 43,
    "decodedTrackCount": 18,
    "headerIndex": 783,
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
      42
    ],
    "endpointFrameSavedPrivately": 43,
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
      30
    ],
    "gifDurationMilliseconds": 1430,
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
        -4.790818214416504,
        7.962061882019043,
        3.7474772930145264
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 1.9968467950820923,
      "projectedMin": [
        -0.4326779842376709,
        0.03760732710361481,
        -0.7663645148277283
      ],
      "projectedMax": [
        0.68538898229599,
        1.7590270042419434,
        0.7230194807052612
      ]
    },
    "worldBounds": {
      "min": [
        -0.43598324060440063,
        -0.8881940841674805,
        -0.011904478073120117
      ],
      "max": [
        0.4798106551170349,
        0.3522975444793701,
        1.7017450332641602
      ]
    },
    "titledGif": {
      "path": "Soldier_common-1312-enetzmb_s_atk_pnh2.gif",
      "bytes": 2124993,
      "sha256": "51ff9e49d7ae92a16b8d3faa2c82caa4be972799a952ae751353c87b019376ea"
    },
    "thumbnail": {
      "path": "Soldier_common-1312-enetzmb_s_atk_pnh2.png",
      "bytes": 149187,
      "sha256": "731dca5d2e9de5f394c895e342497e18e81bb93531b4eafa553c57c2175558b8"
    },
    "privateCleanGifSha256": "b06f02deccea26a1002befe4f2cb364d63df72ce9e83344a4109411770708d40",
    "privateRenderReceiptSha256": "16a665f8b687f49caf300901ae8dc016eba4cbf6a8409b945d0255c1b7e9791c",
    "cleanPngFrameCount": 23,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
