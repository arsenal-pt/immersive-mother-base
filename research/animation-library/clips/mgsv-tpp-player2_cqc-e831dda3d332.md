# Snake CQC - left start/miss transition

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; the source archive below identifies the original animation.

[![Snake CQC - left start/miss transition — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.gif)](../../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.png)

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_cqc-e831dda3d332` |
| Source archive | `player2_cqc` |
| Exact clip name | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_st_mis_l` |
| Clip hash ID | `e831dda3d332` |
| Original source role | player |
| Role interpretation | snake_combo_initiator_candidate |
| Family / phase | related_combo_transition / None |
| Raw source frames | 75 |
| Native frame rate / duration | Unmeasured / unknown |
| Chosen preview speed | 30 source frames/s; every second source frame sampled |
| Full GIF duration | 2500 ms |
| Reference character | Stock Ocelot oce0_main0_def (untextured) |
| Offline preview | Actual decoded motion on a mapped reference rig |
| Native gameplay / paired alignment | Unverified / unverified |
| Ordinary soldier attacker proof | Unverified |
| Archive SHA-256 | `e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85` |
| GANI SHA-256 | `3c39793629d178a55b8b543d3b68faa9453488a325c3bf93f4cfc38fea1f3bc5` |

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

The preview speed is a presentation choice. Individual clips have no matched partner or held weapon; names alone do not prove unarmed punching. Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.

The historical extraction record below keeps its original confidence fields. Its original visualConfirmed=false predates the later offline preview; it is not a claim that the library has no GIF. Offline visualization and native gameplay proof are separate fields.

<details>
<summary>Complete extraction and preview records</summary>

```json
{
  "extraction": {
    "id": "player2_cqc-0080-snapcqc_s_com_st_mis_l",
    "sourceArchive": "player2_cqc",
    "sourceRole": "player",
    "archiveOrdinalZeroBased": 80,
    "ordinalNote": "Ordinal in first MtarTool extraction XML; tool may renumber on repack",
    "name": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_st_mis_l",
    "hashId": "e831dda3d332",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "related_combo_transition",
    "phase": null,
    "phaseKind": "attack",
    "frameCount": 75,
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
        "bytes": 9872,
        "sha256": "3c39793629d178a55b8b543d3b68faa9453488a325c3bf93f4cfc38fea1f3bc5"
      },
      {
        "extension": ".enchnk",
        "bytes": 272,
        "sha256": "c09afd99f130141ddb34c700bfddce1526ac8044b0da2403710717e405a7ce5f"
      }
    ],
    "displayTitle": "Snake CQC - left start/miss transition",
    "offlinePreviewConfirmed": true,
    "preview": {
      "status": "offline-reference-character",
      "referenceCharacter": "Stock Ocelot oce0_main0_def",
      "gif": "../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.gif",
      "thumbnail": "../../media/animation-previews/2026-10-15/player2_cqc-0080-snapcqc_s_com_st_mis_l.png",
      "manifest": "../../media/animation-previews/2026-10-15/preview-manifest.json",
      "chosenSourceFramesPerSecond": 30,
      "nominalGifFramesPerSecond": 15,
      "durationSeconds": 2.5,
      "nativeTimingVerified": false,
      "nativeGameplayProof": false
    }
  },
  "preview": {
    "id": "player2_cqc-0080-snapcqc_s_com_st_mis_l",
    "title": "Snake CQC - left start/miss transition",
    "shortIdentifier": "snapcqc_s_com_st_mis_l",
    "sourceName": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapcqc/snapcqc_s_com_st_mis_l",
    "sourceArchive": "player2_cqc",
    "sourceArchiveSha256": "e75addc327f7602041f3e309317f5cc580be65189f31350bd9e3c45d1146aa85",
    "hashId": "e831dda3d332",
    "sourceGaniSha256": "3c39793629d178a55b8b543d3b68faa9453488a325c3bf93f4cfc38fea1f3bc5",
    "sourceRole": "player",
    "role": "snake_combo_initiator_candidate",
    "sequenceFamily": "related_combo_transition",
    "phase": null,
    "phaseKind": "attack",
    "rawFrameCount": 75,
    "decodedTrackCount": 18,
    "headerIndex": 18,
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
      74
    ],
    "endpointFrameSavedPrivately": 75,
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
      30
    ],
    "gifDurationMilliseconds": 2500,
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
        -4.507643699645996,
        9.366875648498535,
        3.7138848304748535
      ],
      "rotation": [
        1.2772102355957031,
        9.18613878297947e-08,
        -2.613518238067627
      ],
      "orthographicScale": 2.150179862976074,
      "projectedMin": [
        -1.4125243425369263,
        -0.37050479650497437,
        0.16242316365242004
      ],
      "projectedMax": [
        -0.2396554946899414,
        1.4830985069274902,
        1.8246873617172241
      ]
    },
    "worldBounds": {
      "min": [
        -0.19709846377372742,
        0.34992456436157227,
        -0.024501442909240723
      ],
      "max": [
        0.7781689763069153,
        1.8146998882293701,
        1.7752180099487305
      ]
    },
    "titledGif": {
      "path": "player2_cqc-0080-snapcqc_s_com_st_mis_l.gif",
      "bytes": 3134898,
      "sha256": "5bfb47642cc6077db223e2d5f5daa94820861ef149b8b50232ce36817bc9a0fc"
    },
    "thumbnail": {
      "path": "player2_cqc-0080-snapcqc_s_com_st_mis_l.png",
      "bytes": 124176,
      "sha256": "c003fd05d266c452cf02eae2fbc68c86bf34cdd19b5be5b55e689534563411a3"
    },
    "privateCleanGifSha256": "5cff5233ac451185a324914d7434d38a82080270b07536b5d5856b26d4520d70",
    "privateRenderReceiptSha256": "c2ac27bf1674d27afb40cd64f0a14730e5f43840d1da4cbb5a2ee3270ac5b763",
    "cleanPngFrameCount": 39,
    "maximumPerVertexWeightSumError": 1.4901161193847656e-07
  }
}
```

</details>

[Extraction method](../../mtar-punch-combos/README.md) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
