# Starts walking forward

[Library index](../README.md) · [Complete catalogue](../catalogue.json)

Starts walking forward.

[![Starts walking forward - offline full-character reference](../../../media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.gif)](../../../media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.gif)

[Full GIF](../../../media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.gif) · [Still image](../../../media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.png)

**Exact identifier:** `oce0_s_wlk_st_f_r`. **Tags:** walking, start, forward, locomotion, Ocelot package.

Observed action is authored from root-reviewed samples; no community description, native actor/weapon compatibility or continuous human review is asserted.

## Technical data

| Field | Value |
| --- | --- |
| Virtual GANI | /Assets/tpp/motion/SI_game/fani/bodies/oce0/oce0/oce0_s_wlk_st_f_r.gani |
| MTAR | /Assets/tpp/motion/mtar/ocelot2/Ocelot2_layers.mtar |
| Historical FPK | /Assets/tpp/pack/mission2/free/f30050/f30050_ocelot.fpk |
| Historical DAT | master/chunk3.dat |
| Source archive SHA256 | b8d40a45d7a89fd600a58c3f487cb6cb8e06cd3a9a9001a8f425854fafba59b7 |
| GANI SHA256 | e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52 |
| Source identity limit | Payload SHA256 identity; name PathCode64 not independently recomputed; exporter prefix is not an ordinal |
| Source header / decoded body tracks / raw frames | 27 / 18 / 103 |
| Chosen source rate / native rate | 30 source frames/s / unknown |
| GIF frames / duration | 52 / 3430 ms; separate endpoint103 excluded |
| Reference character | Stock Ocelot full-character community reference, untextured |
| Actual reference scene SHA256 | 68e793fb833999c2489d9de1811d6f9b27df471c2e418b4b872a1200ea0b105c |
| Weight audit | 21 meshes; max per-vertex sum error 1.4901161193847656e-07 |
| Secondary ancestor fallbacks | 18; hair/cloth/holster are approximate |
| Root motion | retained; GIF restart resets travel, not native continuity proof |
| Root visual QA | Root reviewed sampled clean and encoded contact poses; not continuous human visual inspection |
| DAT limit | historical October 26/27 identity/stat plus exact 32-byte catalogue header; no whole-DAT hash or fresh installed-currentness proof |

Native timing, floor/contact, paired motion, cloth/twist and arbitrary actor compatibility remain unverified. This is not a training-posture fix.

## Credits

- Konami / Kojima Productions: original game content.
- mctrollin and contributors: community decoder/reference rig/maps.
- BobDoleOwndU and contributors: MtarTool/FMDL tooling.
- Blender / Pillow contributors: rendering and encoding tools.
- arsenal-pt / OpenAI Codex: authored observation, metadata and integration.

[Full credits](../../../CREDITS.md) · [License scope](../../../LICENSE-SCOPE.md) · [Exact reviewed source/provenance](../reviewed/ocelot-transitions-20261029.json)

<details>
<summary>Complete source and preview provenance</summary>

```json
{
  "id": "mgsv-tpp-ocelot2_layers-payloadsha256-e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52",
  "title": "Starts walking forward",
  "shortIdentifier": "oce0_s_wlk_st_f_r",
  "group": "ocelot-locomotion",
  "source": {
    "game": "MGSV TPP",
    "archive": "Ocelot2_layers",
    "archiveSha256": "b8d40a45d7a89fd600a58c3f487cb6cb8e06cd3a9a9001a8f425854fafba59b7",
    "path": "/Assets/tpp/motion/SI_game/fani/bodies/oce0/oce0/oce0_s_wlk_st_f_r",
    "hashId": null,
    "payloadSha256": "e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52",
    "originalCatalogueId": "mgsv-tpp-ocelot2_layers-payloadsha256-e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52"
  },
  "identityBasis": "archive plus full payload SHA256; exporter number is not an archive ordinal or PathCode64",
  "rawFrameCount": 103,
  "nativeFrameRate": null,
  "previewDurationMilliseconds": 3430,
  "detailPage": "research/animation-library/clips/mgsv-tpp-ocelot2_layers-payloadsha256-e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52.md",
  "media": {
    "fullGif": {
      "path": "media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.gif",
      "sha256": "5a0b5ae2beb239ee0f3378094c12d39ccbf79f8c265d17c3425dca16f2a1417b",
      "bytes": 3356914
    },
    "animatedThumbnail": {
      "path": "media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.gif",
      "sha256": "5a0b5ae2beb239ee0f3378094c12d39ccbf79f8c265d17c3425dca16f2a1417b",
      "bytes": 3356914,
      "width": 480,
      "height": 614,
      "displayWidth": 160,
      "displayHeight": 205,
      "kind": "accepted full GIF reused for display; display scaling does not reduce download bytes",
      "encodedFrames": 52,
      "durationMilliseconds": 3430,
      "loop": 0
    },
    "stillThumbnail": {
      "path": "media/animation-previews/2026-10-29-ocelot-transitions/oce0_s_wlk_st_f_r.png",
      "sha256": "67c7f2ce0cb7afdf6fbd1edc9ac70fe63b0ace8c9b521c57d851141eb4bdac46",
      "bytes": 94098,
      "width": 480,
      "height": 614
    }
  },
  "evidence": {
    "offlineDecodedPreview": true,
    "nativeGameplay": false,
    "nativeTiming": false,
    "pairedAlignment": false,
    "ordinarySoldierAttacker": false,
    "sampledRootVisualAcceptance": true,
    "continuousHumanVisualReview": false
  },
  "originalRecords": {
    "extraction": {
      "id": "mgsv-tpp-ocelot2_layers-payloadsha256-e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52",
      "exactClipName": "oce0_s_wlk_st_f_r",
      "virtualGaniPath": "/Assets/tpp/motion/SI_game/fani/bodies/oce0/oce0/oce0_s_wlk_st_f_r.gani",
      "category": "Ocelot-package locomotion source references",
      "description": "Unpreviewed oce0_s_wlk_st_f_r motion; action interpretation not visually verified",
      "descriptionAuthority": "authored pending-preview label; exact identifier only, no visually verified action interpretation",
      "sourceArchive": "Ocelot2_layers.mtar",
      "sourceArchiveSha256": "b8d40a45d7a89fd600a58c3f487cb6cb8e06cd3a9a9001a8f425854fafba59b7",
      "payloadSha256": "e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52",
      "payloadBytes": 9856,
      "sidecars": [],
      "exporterLabel": "0034_oce0_s_wlk_st_f_r",
      "sourceArchiveOrdinal": null,
      "ordinalCaution": "Numbered exporter label only; original ordinal not asserted because export ordering differs from pre-export console order.",
      "rawFrameCount": null,
      "frameCountStatus": "not parsed in this consolidation; no guessed header offset",
      "nativeFrameRate": null,
      "previewFrameRate": null,
      "sourceSceneSpecific": false,
      "visualConfirmed": false,
      "nativePlaybackConfirmed": false,
      "trainingCompatibilityConfirmed": false,
      "status": "retained-source-hash-verified-preview-pending",
      "media": {
        "cleanSourceFramesOrVideo": null,
        "titledGif": null,
        "thumbnail": null,
        "contactSheet": null
      },
      "requiredNextEvidence": [
        "compatible documented full-character rig and mapping",
        "one decoded sample with inspected motion",
        "clean source frames/video",
        "readable titled looping GIF and still thumbnail",
        "contact-sheet visual review and exact tool/rig/frame/root-motion provenance"
      ],
      "sourceHeaderEvidence": {
        "headerIndex": 27,
        "fullPathCode64": "0xfc534f5ca9b8f779",
        "rendererBaseRelativeHashId": "34f5ca9b8f779",
        "rawHeaderFrameCount": 103
      }
    },
    "sourceChain": {
      "datVirtualPath": "master/chunk3.dat",
      "datEvidence": "historical October 26/27 identity/stat plus exact 32-byte catalogue header; no whole-DAT hash or fresh installed-currentness proof",
      "fpkVirtualPath": "/Assets/tpp/pack/mission2/free/f30050/f30050_ocelot.fpk",
      "fpkDecodedSha256": "e9330a6700eaf35d4181cfdc65ad7bfb222cfeb9dcf1891bc391cd53df9f6317",
      "mtarVirtualPath": "/Assets/tpp/motion/mtar/ocelot2/Ocelot2_layers.mtar",
      "mtarSha256": "b8d40a45d7a89fd600a58c3f487cb6cb8e06cd3a9a9001a8f425854fafba59b7",
      "mtarRehashedForThisConsolidation": true,
      "mtarIndexOffsetEquality": "retained extraction receipt, not re-extracted or re-indexed this time",
      "sourceRecords": {
        "eligibleMetadataSha256": "0c71dc03b809efe7cbf631e895e154a566747069dc1197bb1ca1ff8db17f96cf",
        "selectedMembersReceiptSha256": "e3516078cc45262f1318f97e3b8a23b8ace8cda7c8a6d12c37b824c103cc031c",
        "finalSourceReceiptSha256": "3809672e1abb14b2ae12ee04a78ba0de3270758b3f02f0c7782db9237ea681f3"
      },
      "tools": {
        "MtarTool": {
          "version": "0.2.7",
          "author": "BobDoleOwndU",
          "originalToolPins": {
            "CityHash.dll": {
              "sha256": "def6c4506d461b65e4059b2936b2cbd5f852ba5d1d8a1a527f1c0e6dc7008c8f",
              "bytes": 15872
            },
            "hashed_names.txt": {
              "sha256": "d157dd1479418dc3accaaff20e440739c54114590a53a73acef17f7553cfb54d",
              "bytes": 933
            },
            "MtarTool.Core.dll": {
              "sha256": "84b5111069c2ecccbc90394b6f52d9b7c0bff228a97f7dc4ea866c617373a9e9",
              "bytes": 15360
            },
            "MtarTool.exe": {
              "sha256": "7ef5686320b0f5817db50c7c0f8dc38b5362b366c6dd712f76c5f96b70e9070a",
              "bytes": 6656
            },
            "mtar_dictionary.txt": {
              "sha256": "30c11a1f6478db700bdb7df5327ddf8a21bab35111c3aec01e84cf8572fad591",
              "bytes": 756215
            }
          }
        }
      }
    },
    "preview": {
      "sourceGaniSha256": "e5e1e88d787f3f134ab51a7b3b8c1aa445ad8950a04d91c7ee6ec7acae274d52",
      "chosenSourceFramesPerSecond": 30,
      "nativeFrameRate": null,
      "rawFrameCount": 103,
      "decodedBodyTrackCount": 18,
      "sourceHeaderIndex": 27,
      "gifMotionFrames": 52,
      "gifDurationMilliseconds": 3430,
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
        88,
        90,
        92,
        94,
        96,
        98,
        100,
        102
      ],
      "separateEndpointFrame": 103,
      "endpointExcludedFromGif": true,
      "referenceCharacter": "Stock Ocelot full-character community reference, untextured",
      "referenceCharacterBlendSha256": "68e793fb833999c2489d9de1811d6f9b27df471c2e418b4b872a1200ea0b105c",
      "referenceCharacterIdentityLimit": "Separately pinned actual reference; do not substitute the historical different reference scene",
      "historicalDifferentReferenceSha256": "6c1cb2ead2a82b78bd1240ad880c1bac0ba2bfe1d7c8f04aa4c311852a286a28",
      "sourceToolPins": {
        "scriptSha256": "13c2fe0cc9ba420c28e2ced10c2f3b6e230d473f7ae9b698d68703bfc305adf6",
        "referenceRigSha256": "c020ff7c2c39dd82b9b084999bcbdfa35c2d171d94552fe84696a90439c59445",
        "trackMapSha256": "2755175dc333ee1320e16d732e6c0707d5f266ff7f91e5b122ca1d4ad3f34a81",
        "boneMapSha256": "b6375a070f719de38a16648081eb124d3e5a3235b872285510443ece54f47d97"
      },
      "renderBatchReceiptSha256": "0622364a22942736c9469ce17dee804e953e6f1c2b1bf34f11f4fdd825fb2d89",
      "renderReceiptSha256": "fe52dc4bf8eec8c6c1cd39696ee4913b255497a041a641947485361876773c7b",
      "encodedManifestSha256": "bbe83bf64754ff17f3c00df5e51fe7d28200ca9f4aa1269dda5eed70121aee84",
      "encoderReportedStatus": "encoded-render-awaiting-visual-review",
      "encoderReportedPublicVisualAcceptance": false,
      "rootAcceptanceSha256": "2730e330c40fc7e2ccb87653a1a7f74ff65a80650f5a67ea47a7e37da62262ec",
      "rootVisualAcceptance": true,
      "rootReviewScope": "Root reviewed sampled clean and encoded contact poses; not continuous human visual inspection",
      "rootMotion": "retained; GIF restart resets travel, not native continuity proof",
      "rawLayoutFrameRateField": "5",
      "rawLayoutFrameRateIsNativeFps": false,
      "actualWeightAuditSummary": {
        "meshCount": 21,
        "vertices": 10039,
        "maxPerVertexWeightSumError": 1.4901161193847656e-07,
        "meshes": [
          {
            "mesh": "9_-_MESH_ROOT",
            "vertices": 340,
            "sourceGroupCount": 8,
            "targetGroupCount": 6,
            "maxPerVertexWeightSumError": 5.960464477539063e-08
          },
          {
            "mesh": "8_-_MESH_ROOT",
            "vertices": 402,
            "sourceGroupCount": 3,
            "targetGroupCount": 3,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "7_-_MESH_ROOT",
            "vertices": 111,
            "sourceGroupCount": 22,
            "targetGroupCount": 22,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "6_-_MESH_ROOT",
            "vertices": 46,
            "sourceGroupCount": 6,
            "targetGroupCount": 6,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "5_-_MESH_ROOT",
            "vertices": 1247,
            "sourceGroupCount": 32,
            "targetGroupCount": 28,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "4_-_MESH_ROOT",
            "vertices": 1077,
            "sourceGroupCount": 32,
            "targetGroupCount": 31,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "3_-_MESH_ROOT",
            "vertices": 1034,
            "sourceGroupCount": 32,
            "targetGroupCount": 30,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "2_-_MESH_ROOT",
            "vertices": 499,
            "sourceGroupCount": 14,
            "targetGroupCount": 5,
            "maxPerVertexWeightSumError": 1.4901161193847656e-07
          },
          {
            "mesh": "20_-_MESH_ROOT",
            "vertices": 146,
            "sourceGroupCount": 9,
            "targetGroupCount": 9,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "1_-_MESH_ROOT",
            "vertices": 2099,
            "sourceGroupCount": 19,
            "targetGroupCount": 16,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "19_-_9df4dd0aeae",
            "vertices": 381,
            "sourceGroupCount": 13,
            "targetGroupCount": 13,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "18_-_9df4dd0aeae",
            "vertices": 160,
            "sourceGroupCount": 12,
            "targetGroupCount": 12,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "17_-_9df4dd0aeae",
            "vertices": 153,
            "sourceGroupCount": 11,
            "targetGroupCount": 11,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "16_-_9df4dd0aeae",
            "vertices": 180,
            "sourceGroupCount": 15,
            "targetGroupCount": 15,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "15_-_9df4dd0aeae",
            "vertices": 297,
            "sourceGroupCount": 20,
            "targetGroupCount": 20,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "14_-_9df4dd0aeae",
            "vertices": 300,
            "sourceGroupCount": 24,
            "targetGroupCount": 24,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "13_-_9df4dd0aeae",
            "vertices": 275,
            "sourceGroupCount": 9,
            "targetGroupCount": 9,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "12_-_MESH_hag_a",
            "vertices": 396,
            "sourceGroupCount": 1,
            "targetGroupCount": 1,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "11_-_MESH_hag_b",
            "vertices": 466,
            "sourceGroupCount": 1,
            "targetGroupCount": 1,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "10_-_MESH_ROOT",
            "vertices": 236,
            "sourceGroupCount": 2,
            "targetGroupCount": 2,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "0_-_MESH_ROOT",
            "vertices": 194,
            "sourceGroupCount": 6,
            "targetGroupCount": 4,
            "maxPerVertexWeightSumError": 2.2351741790771484e-08
          }
        ]
      },
      "actualSecondaryBoneAncestorFallbacks": {
        "SKL_610_HRAA_SIM": "SKL_004_HEAD",
        "SKL_611_HRAB_SIM": "SKL_004_HEAD",
        "SKL_612_HRBA_SIM": "SKL_004_HEAD",
        "SKL_613_HRBB_SIM": "SKL_004_HEAD",
        "SKL_614_HRCA_SIM": "SKL_004_HEAD",
        "SKL_615_HRCB_SIM": "SKL_004_HEAD",
        "SKL_616_HRFA_SIM": "SKL_004_HEAD",
        "SKL_617_HRFB_SIM": "SKL_004_HEAD",
        "SKL_618_HRTA_SIM": "SKL_004_HEAD",
        "SKL_549_SKFB_HLP": "SKL_003_NECK",
        "SKL_550_SKFA_HLP": "SKL_003_NECK",
        "SKL_635_SCLA_SIM": "SKL_002_CHEST",
        "SKL_636_SCLB_SIM": "SKL_002_CHEST",
        "SKL_640_SCRA_SIM": "SKL_002_CHEST",
        "SKL_641_SCRB_SIM": "SKL_002_CHEST",
        "SKL_600_HAGB_SIM": "SKL_001_SPINE",
        "SKL_560_HLFA_HLP": "SKL_000_WAIST",
        "SKL_561_HLFB_HLP": "SKL_000_WAIST"
      },
      "rootAcceptanceEvidence": {
        "kind": "root confirmed sampled offline contact acceptance",
        "contactSha256": "c67c00a83a4e37e0ef0ded9ecb0ef3f6f0a3bc52cb6036d186e414beccd9fa66",
        "technicalBatchReceiptSha256": null
      }
    }
  },
  "category": {
    "id": "ocelot-locomotion",
    "label": "Ocelot-package locomotion references"
  },
  "tags": [
    "walking",
    "start",
    "forward",
    "locomotion",
    "Ocelot package"
  ],
  "classificationProvenance": {
    "kind": "project-authored",
    "credit": "arsenal-pt / OpenAI Codex",
    "categoryAndCandidateTags": "Observed walking action plus retained Ocelot source package; no native actor/weapon inference",
    "postureTags": null
  },
  "locations": {
    "ganiVirtualPath": "/Assets/tpp/motion/SI_game/fani/bodies/oce0/oce0/oce0_s_wlk_st_f_r.gani",
    "ganiDirectory": "/Assets/tpp/motion/SI_game/fani/bodies/oce0/oce0",
    "archiveFile": "Ocelot2_layers.mtar",
    "recordedContainerLabel": "f30050_ocelot",
    "archiveVirtualPath": "/Assets/tpp/motion/mtar/ocelot2/Ocelot2_layers.mtar",
    "containerVirtualPath": "/Assets/tpp/pack/mission2/free/f30050/f30050_ocelot.fpk",
    "datArchive": "master/chunk3.dat",
    "containerSha256": "e9330a6700eaf35d4181cfdc65ad7bfb222cfeb9dcf1891bc391cd53df9f6317",
    "datArchiveSha256": null,
    "datOriginStatus": "historical October 26/27 identity/stat plus exact 32-byte catalogue header; no whole-DAT hash or fresh installed-currentness proof",
    "archiveVirtualPathStatus": "Retained extraction receipt binds exact FPK member/index-offset equality; not freshly re-extracted",
    "containerVirtualPathStatus": "Historical source extraction identity; current DAT membership/version unverified",
    "provenance": {
      "recordPath": "research/animation-library/reviewed/ocelot-transitions-20261029.json",
      "kind": "retained exact source bytes plus root-accepted decoded preview",
      "archiveSha256": "b8d40a45d7a89fd600a58c3f487cb6cb8e06cd3a9a9001a8f425854fafba59b7",
      "dictionarySha256": "30c11a1f6478db700bdb7df5327ddf8a21bab35111c3aec01e84cf8572fad591",
      "nameMatchLimit": "Textual PathCode64 not independently recomputed; exact payload identity/retained virtual name kept separate",
      "sourceReceiptHashes": {
        "eligibleMetadataSha256": "0c71dc03b809efe7cbf631e895e154a566747069dc1197bb1ca1ff8db17f96cf",
        "selectedMembersReceiptSha256": "e3516078cc45262f1318f97e3b8a23b8ace8cda7c8a6d12c37b824c103cc031c",
        "finalSourceReceiptSha256": "3809672e1abb14b2ae12ee04a78ba0de3270758b3f02f0c7782db9237ea681f3"
      }
    }
  },
  "motionOrigin": {
    "actor": "Ocelot-package shared-body source",
    "basis": "Retained oce0 virtual source path and Ocelot2_layers payload identity; arbitrary actor compatibility unverified",
    "referenceModelIsMotionOrigin": false
  },
  "description": {
    "text": "Starts walking forward.",
    "kind": "project-authored source-name-qualified offline observation",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Root accepted sampled full-body references; variant qualifier comes from retained source name, not community text/native proof"
  },
  "authoredDescription": {
    "text": "Starts walking forward.",
    "kind": "project-authored source-name-qualified offline observation",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Root accepted sampled full-body references; variant qualifier comes from retained source name, not community text/native proof"
  },
  "sourceDescription": {
    "status": "no-verified-community-description",
    "text": null,
    "credit": null,
    "sourceUrl": null,
    "reason": "Walking description is an authored observation; no community-text match asserted",
    "reviewRecord": "research/animation-library/reviewed/ocelot-transitions-20261029.json"
  },
  "credits": [
    {
      "name": "Konami / Kojima Productions",
      "role": "original game content"
    },
    {
      "name": "mctrollin and contributors",
      "role": "community decoder/reference rig/maps"
    },
    {
      "name": "BobDoleOwndU and contributors",
      "role": "MtarTool/FMDL tooling"
    },
    {
      "name": "Blender / Pillow contributors",
      "role": "rendering and encoding tools"
    },
    {
      "name": "arsenal-pt / OpenAI Codex",
      "role": "authored observation, metadata and integration"
    }
  ],
  "sourceBatch": "ocelot-transitions-20261029",
  "dedicatedTableSlug": "ocelot-locomotion-oce0_s_wlk_st_f_r"
}
```

</details>
