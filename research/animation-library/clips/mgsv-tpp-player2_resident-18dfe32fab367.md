# Special/zombie punch - player phase 1

[Back to animation library](../README.md) · [Complete library data](../catalogue.json)

Click the image to open the original full-size GIF. Its visible character is a reference model; source identity is recorded separately below.

[![Special/zombie punch - player phase 1 — full-character offline preview](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif)](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif)

[Open full-size GIF](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.gif) · [Still image](../../../media/animation-previews/2026-10-15/player2_resident-1280-snapzmb_s_atk_pnh.png)

## Classification and descriptions

**Category:** Special / zombie actor candidates. **Tags:** `offline-reference`, `source-player`, `special-actor`, `zombie-namespace`, `punch-candidate`.

**Authored preview description:** Special/zombie punch - player phase 1 on an untextured reference character. Credit: arsenal-pt / OpenAI Codex. Previously reviewed titled offline preview; source meanings/native use remain unverified.

**Community source description:** Unavailable. No verified exact source-description match for this entry. The reviewed BossQuiet2_layers list has zero matching paths among the current 27 clips.

Match status: `unavailable-no-verified-exact-match`. [Description sources and matching rules](../description-sources.md).

The source directory is a virtual game-asset directory. The retained clip stem and the .gani file path are separate fields. [Container provenance](../container-provenance.json) joins retained FPK/MTAR hashes and historical extraction logs; recorded DAT origins do not verify current DAT contents.

## Technical data

| Field | Value |
| --- | --- |
| Game | Metal Gear Solid V: The Phantom Pain |
| Library ID | `mgsv-tpp-player2_resident-18dfe32fab367` |
| Category | Special / zombie actor candidates |
| Tags (authored retrieval labels) | offline-reference, source-player, special-actor, zombie-namespace, punch-candidate |
| Source archive | `player2_resident` |
| Exact clip stem (retained) | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh` |
| Virtual GANI file | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh.gani` |
| Virtual GANI directory | `/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb` |
| MTAR file | `player2_resident.mtar` |
| Recorded container label | player2_resident_motion |
| Virtual MTAR path | /Assets/tpp/motion/mtar/player2/player2_resident.mtar |
| Virtual FPK path | /Assets/tpp/pack/player/motion/player2_resident_motion.fpk |
| Recorded DAT origin | a_chunk7.dat |
| DAT version limit | Historical source-receipt origin; entire DAT content/version not rechecked by this metadata task |
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
| Dictionary snapshot SHA-256 | `30c11a1f6478db700bdb7df5327ddf8a21bab35111c3aec01e84cf8572fad591` |

## Credits and evidence

- **Konami / Kojima Productions** — original game animation.
- **mctrollin and contributors** — community motion decoder, reference rig and mappings.
- **arsenal-pt / OpenAI Codex** — authored catalogue category, tags and preview summary.

Categories/tags and preview summaries are project-authored. Candidate roles/families come from retained naming metadata; posture labels come from the already reviewed offline preview. An unavailable community description has no attributed per-entry source author. [Full tool/model credits](../../../CREDITS.md).

## Interpretation and limits

Distinct special-actor/transition candidate; not an ordinary soldier combo proof.

Preview speed is a presentation choice. Individual clips have no matched partner or held weapon. Labels alone do not prove native weapon handling, interaction contact or actor compatibility. Hair, scarf and holster motion uses mapped-ancestor fallbacks; native Fox cloth/twist and timing remain unverified.

Historical extraction confidence fields below are unchanged. Original visualConfirmed=false predates the later offline preview; offline visualization and native gameplay proof remain separate fields.

<details>
<summary>Classification, location and description provenance</summary>

```json
{
  "category": {
    "id": "special-actors",
    "label": "Special / zombie actor candidates"
  },
  "tags": [
    "offline-reference",
    "source-player",
    "special-actor",
    "zombie-namespace",
    "punch-candidate"
  ],
  "classificationProvenance": {
    "kind": "project-authored",
    "credit": "arsenal-pt / OpenAI Codex",
    "categoryAndCandidateTags": "Retained source namespace, role, family and phase metadata; interpretations remain candidates",
    "postureTags": null,
    "extractionRecordPath": "research/mtar-punch-combos/animations-metadata.json",
    "nativeGameplayProof": false
  },
  "locations": {
    "ganiVirtualPath": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb/snapzmb_s_atk_pnh.gani",
    "ganiDirectory": "/Assets/tpp/motion/SI_game/fani/bodies/snap/snapzmb",
    "archiveFile": "player2_resident.mtar",
    "recordedContainerLabel": "player2_resident_motion",
    "archiveVirtualPath": "/Assets/tpp/motion/mtar/player2/player2_resident.mtar",
    "containerVirtualPath": "/Assets/tpp/pack/player/motion/player2_resident_motion.fpk",
    "containerLocationStatus": "known historical virtual paths; exact retained FPK/MTAR hashes verified",
    "provenance": {
      "kind": "retained-extraction-record",
      "recordPath": "research/mtar-punch-combos/animations-metadata.json",
      "archiveSha256": "18c4a35c524dcc46f19e712f61a261c94283720a0f119340cecc17eef37fc0d0",
      "dictionarySha256": "30c11a1f6478db700bdb7df5327ddf8a21bab35111c3aec01e84cf8572fad591",
      "pathRule": "Exact resolved member stem plus the extracted .gani payload extension; no extraction ordinal used",
      "containerReview": "research/animation-library/container-provenance.json",
      "containerEvidence": [
        {
          "kind": "source-provenance receipt",
          "sha256": "e4ae0bf6f27d42630865662a89e5a387748fdf1cfbf91c718f4254c0855bffc8"
        },
        {
          "kind": "successful Gzs command receipt",
          "sha256": "5cbcac1e19cdb652353306f15b39c1878ead289b907ee462d72be516343ee615",
          "commandTag": "gzs-player2_resident_motion",
          "exitCode": 0
        },
        {
          "kind": "retained Gzs extracted-path log",
          "sha256": "a235e3237db4844b8bf4573dde2130504deaa80e695c932f3f994fd7a6b9ee82"
        },
        {
          "kind": "immutable private library receipt",
          "sha256": "b640d528849cdf79327353cf6c37d2f15244659a6e3039f2cee18e8cb431cbb8",
          "libraryZipSha256": "299795a7378d55f18d059f02a2946763d8c546c2a4db5da6bdb5baed84646c2d"
        }
      ],
      "containerVerification": "Exact retained FPK and original MTAR member bytes match recorded hashes; pack label joins the successful extraction log. No new extraction or current DAT verification."
    },
    "datArchive": "a_chunk7.dat",
    "datArchiveSha256": null,
    "containerSha256": "22a6a75782f1b80978e5990211700a5f75e7496c2550ddf56450aed8236501a3",
    "datOriginStatus": "Historical source-receipt origin; entire DAT content/version not rechecked by this metadata task"
  },
  "authoredDescription": {
    "text": "Special/zombie punch - player phase 1 on an untextured reference character.",
    "kind": "project-authored preview summary",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Previously reviewed titled offline preview; source meanings/native use remain unverified"
  },
  "sourceDescription": {
    "status": "unavailable-no-verified-exact-match",
    "text": null,
    "credit": null,
    "sourceUrl": null,
    "reason": "No verified exact source-description match for this entry. The reviewed BossQuiet2_layers list has zero matching paths among the current 27 clips.",
    "reviewRecord": "research/animation-library/metadata-source-review.json"
  },
  "credits": [
    {
      "name": "Konami / Kojima Productions",
      "role": "original game animation"
    },
    {
      "name": "mctrollin and contributors",
      "role": "community motion decoder, reference rig and mappings"
    },
    {
      "name": "arsenal-pt / OpenAI Codex",
      "role": "authored catalogue category, tags and preview summary"
    }
  ]
}
```

</details>

<details>
<summary>Complete original extraction and preview records</summary>

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

[Exact extraction catalogue](../../mtar-punch-combos/animations-metadata.json) · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)
