# Stock motion reference: enetasr_q_die_rd_bdf_b_l

[Library index](../README.md) · [Complete catalogue](../catalogue.json)

Decoded stock body-motion reference enetasr_q_die_rd_bdf_b_l; action interpretation unverified.

[![Stock motion reference: enetasr_q_die_rd_bdf_b_l - offline full-character reference](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.gif)](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.gif)

[Full GIF](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.gif) · [Still image](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.png)

**Exact identifier:** `enetasr_q_die_rd_bdf_b_l`. **Tags:** stock body motion, Soldier_common, source-derived label, Ocelot reference mesh.

Source-derived motion label; shared pipeline approved. Per-clip visual review status is in provenance; no action or native compatibility is inferred.

## Technical data

| Field | Value |
| --- | --- |
| Virtual GANI | /Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_q_die_rd_bdf_b_l.gani |
| MTAR | Unverified |
| Historical FPK | Unverified |
| Historical DAT | Unverified |
| Source archive SHA256 | 6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e |
| GANI SHA256 | 544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9 |
| Source identity limit | Payload SHA256 identity; name PathCode64 not independently recomputed; exporter prefix is not an ordinal |
| Source header / decoded body tracks / raw frames | 169 / 18 / 75 |
| Chosen source rate / native rate | 30 source frames/s / unknown |
| GIF frames / duration | 38 / 2500 ms; separate endpoint75 excluded |
| Reference character | Stock Ocelot full-character community reference, untextured |
| Actual reference scene SHA256 | 68e793fb833999c2489d9de1811d6f9b27df471c2e418b4b872a1200ea0b105c |
| Weight audit | 21 meshes; max per-vertex sum error 1.4901161193847656e-07 |
| Secondary ancestor fallbacks | 18; hair/cloth/holster are approximate |
| Root motion | Retained root travel; GIF restart is not native continuity |
| Root visual QA | Shared pipeline sampled/approved; this clip has not been visually reviewed |
| DAT limit | Unverified outer DAT/FPK membership; no installed-currentness or whole-DAT hash claim |

Native timing, floor/contact, paired motion, cloth/twist and arbitrary actor compatibility remain unverified. This is not a training-posture fix.

## Credits

- Konami / Kojima Productions: original game content.
- mctrollin and contributors: community decoder/reference rig/maps.
- BobDoleOwndU and contributors: MtarTool/FMDL tooling.
- Blender / Pillow contributors: rendering/encoding tools.
- arsenal-pt / OpenAI Codex: authored pipeline/integration.

[Full credits](../../../CREDITS.md) · [License scope](../../../LICENSE-SCOPE.md) · [Exact reviewed source/provenance](../reviewed/animation-500-45d9ae07917a78d9e735.json)

<details>
<summary>Complete source and preview provenance</summary>

```json
{
  "id": "mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9",
  "title": "Stock motion reference: enetasr_q_die_rd_bdf_b_l",
  "shortIdentifier": "enetasr_q_die_rd_bdf_b_l",
  "group": "stock-soldier",
  "source": {
    "game": "MGSV TPP",
    "archive": "Soldier_common",
    "archiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "path": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_q_die_rd_bdf_b_l",
    "hashId": "7fabc5748c16",
    "payloadSha256": "544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9",
    "originalCatalogueId": "mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9"
  },
  "identityBasis": "Exact retained archive plus full payload SHA256; header index and textual name retained separately",
  "rawFrameCount": 75,
  "nativeFrameRate": null,
  "previewDurationMilliseconds": 2500,
  "detailPage": "research/animation-library/clips/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.md",
  "media": {
    "fullGif": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.gif",
      "sha256": "0c0b32286d32ea9161dac20ec8b9aeaa15262ddc73054b6bccf58d9b4e118785",
      "bytes": 2418118
    },
    "animatedThumbnail": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.gif",
      "sha256": "0c0b32286d32ea9161dac20ec8b9aeaa15262ddc73054b6bccf58d9b4e118785",
      "bytes": 2418118,
      "width": 480,
      "height": 614,
      "displayWidth": 160,
      "displayHeight": 205,
      "kind": "Full GIF displayed small; download bytes unchanged",
      "encodedFrames": 38,
      "durationMilliseconds": 2500,
      "loop": 0
    },
    "stillThumbnail": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9.png",
      "sha256": "524efecd7bb5d8f3e79301527ba8dab12ff7e163e369ce7c0cddb21a563c5884",
      "bytes": 86162,
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
    "sampledRootVisualAcceptance": false,
    "continuousHumanVisualReview": false,
    "rootApprovedPipeline": true,
    "perClipVisualReviewPending": true
  },
  "originalRecords": {
    "extraction": {
      "headerIndex": 169,
      "fullArchivePathHash": "0xfc507fabc5748c16",
      "hashId": "7fabc5748c16",
      "payloadSha256": "544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9",
      "payloadBytes": 12560,
      "tracksOffset": 2521440,
      "rawFrameCount": 75,
      "retainedNameCandidates": [
        "Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/0206_enetasr_q_die_rd_bdf_b_l.gani"
      ],
      "selectionStatus": "eligible-source-bound-decoder-and-mapping-pending",
      "exporterPath": "Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/0206_enetasr_q_die_rd_bdf_b_l.gani",
      "shortIdentifier": "enetasr_q_die_rd_bdf_b_l",
      "name": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_q_die_rd_bdf_b_l",
      "id": "mgsv-tpp-soldier_common-payloadsha256-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9",
      "sourceArchive": "Soldier_common",
      "sourceMtarSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
      "frameCount": 75,
      "sourceRole": "authentic-stock-body-reference-pending-decode",
      "role": "stock_soldier_body_reference",
      "sequenceFamily": "source-name-only",
      "phase": null,
      "phaseKind": "unclassified",
      "sidecars": [
        {
          "extension": ".gani",
          "sha256": "544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9"
        }
      ],
      "nativeFrameRate": null,
      "actionInterpretation": "unverified source-derived identifier",
      "visualReview": "awaiting-root-or-human-batch-sample",
      "actualDecoded": false,
      "newPublishedCredit": 0
    },
    "sourceChain": {
      "archiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
      "archiveBytes": 15897168,
      "header": {
        "version": 201403250,
        "fileCount": 1345,
        "trackCount": 18,
        "segmentCount": 56,
        "shaderNodeCount": 0,
        "shaderUnitCount": 0,
        "motionPointUnits": 9,
        "flags": 4096,
        "commonInfoOffset": 43072,
        "padding": 0
      },
      "originalStockOnly": true,
      "nameBinding": "retained MtarTool manifest/XML plus exact original table block SHA; canonical text PathCode not independently recomputed",
      "layout": "full original CommonInfo/MTAR retained; no loose GANI reconstruction",
      "metadataPins": {
        "manifestSha256": "156eabf438ecfa783fbbda2d7b96c2b8a1f6f9db3b0a2a27333a346edae3fc65",
        "xmlSha256": "c782c00c7a391b13daeb21417a595fa2a5dea63b1eb7059afdaedde3db4d100e",
        "exclusionCatalogueSha256": "4accbb6988c9e7f6a6ab314a6d7f68f206b96a5b6ee39b442d4540b7c5294fd1"
      }
    },
    "preview": {
      "sourceGaniSha256": "544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9",
      "chosenSourceFramesPerSecond": 30,
      "nativeFrameRate": null,
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
      "separateEndpointFrame": 75,
      "gifDurationMilliseconds": 2500,
      "referenceCharacterBlendSha256": "68e793fb833999c2489d9de1811d6f9b27df471c2e418b4b872a1200ea0b105c",
      "historicalDifferentReferenceSha256": "6c1cb2ead2a82b78bd1240ad880c1bac0ba2bfe1d7c8f04aa4c311852a286a28",
      "sourceToolPins": {
        "scriptSha256": "13c2fe0cc9ba420c28e2ced10c2f3b6e230d473f7ae9b698d68703bfc305adf6",
        "referenceRigSha256": "c020ff7c2c39dd82b9b084999bcbdfa35c2d171d94552fe84696a90439c59445",
        "trackMapSha256": "2755175dc333ee1320e16d732e6c0707d5f266ff7f91e5b122ca1d4ad3f34a81",
        "boneMapSha256": "b6375a070f719de38a16648081eb124d3e5a3235b872285510443ece54f47d97"
      },
      "renderBatchReceiptSha256": "63ca54be7b9d2bb87338ee28d577318afc427764735c0df943d60ea008795b96",
      "renderReceiptSha256": "565af9105a953151e6c11948245a18ebe57bc7b9b42fc3d7c70da78e11e5a42e",
      "rawLayoutFrameRateField": "5",
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
      "rawFrameCount": 75,
      "decodedBodyTrackCount": 18,
      "sourceHeaderIndex": 169,
      "gifMotionFrames": 38,
      "encodedManifestSha256": "92cd450fd2c57947d059f80cef18c52853be7e8d969ce9fc8a07ccc2bbc5660f",
      "encoderReportedStatus": "encoded-render-awaiting-visual-review",
      "encoderReportedPublicVisualAcceptance": false,
      "rootAcceptanceSha256": "99860bddf0c36bc36c9c28c186bc713b565c4ac3bda18bf7268bfc72697e013d",
      "rootVisualAcceptance": false,
      "perClipVisualReviewPending": true,
      "rootReviewScope": "Shared pipeline sampled/approved; this clip has not been visually reviewed",
      "referenceCharacter": "Stock Ocelot full-character community reference, untextured",
      "rootMotion": "Retained root travel; GIF restart is not native continuity",
      "actualWeightAuditSummary": {
        "meshCount": 21,
        "vertices": 10039,
        "maxPerVertexWeightSumError": 1.4901161193847656e-07,
        "meshes": [
          {
            "mesh": "9_-_MESH_ROOT",
            "vertices": 340,
            "maxPerVertexWeightSumError": 5.960464477539063e-08
          },
          {
            "mesh": "8_-_MESH_ROOT",
            "vertices": 402,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "7_-_MESH_ROOT",
            "vertices": 111,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "6_-_MESH_ROOT",
            "vertices": 46,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "5_-_MESH_ROOT",
            "vertices": 1247,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "4_-_MESH_ROOT",
            "vertices": 1077,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "3_-_MESH_ROOT",
            "vertices": 1034,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "2_-_MESH_ROOT",
            "vertices": 499,
            "maxPerVertexWeightSumError": 1.4901161193847656e-07
          },
          {
            "mesh": "20_-_MESH_ROOT",
            "vertices": 146,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "1_-_MESH_ROOT",
            "vertices": 2099,
            "maxPerVertexWeightSumError": 2.9802322387695312e-08
          },
          {
            "mesh": "19_-_9df4dd0aeae",
            "vertices": 381,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "18_-_9df4dd0aeae",
            "vertices": 160,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "17_-_9df4dd0aeae",
            "vertices": 153,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "16_-_9df4dd0aeae",
            "vertices": 180,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "15_-_9df4dd0aeae",
            "vertices": 297,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "14_-_9df4dd0aeae",
            "vertices": 300,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "13_-_9df4dd0aeae",
            "vertices": 275,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "12_-_MESH_hag_a",
            "vertices": 396,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "11_-_MESH_hag_b",
            "vertices": 466,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "10_-_MESH_ROOT",
            "vertices": 236,
            "maxPerVertexWeightSumError": 0.0
          },
          {
            "mesh": "0_-_MESH_ROOT",
            "vertices": 194,
            "maxPerVertexWeightSumError": 2.2351741790771484e-08
          }
        ]
      }
    }
  },
  "category": {
    "id": "stock-soldier",
    "label": "Stock Soldier_common motion references"
  },
  "tags": [
    "stock body motion",
    "Soldier_common",
    "source-derived label",
    "Ocelot reference mesh"
  ],
  "classificationProvenance": {
    "kind": "source-identity only",
    "credit": "arsenal-pt / OpenAI Codex",
    "actionClassificationVerified": false,
    "categoryAndCandidateTags": "Retained source archive/identity only; action interpretation unverified",
    "postureTags": null
  },
  "locations": {
    "ganiVirtualPath": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_q_die_rd_bdf_b_l.gani",
    "ganiDirectory": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr",
    "archiveFile": "Soldier_common.mtar",
    "recordedContainerLabel": "Unverified",
    "archiveVirtualPath": null,
    "containerVirtualPath": null,
    "datArchive": null,
    "containerSha256": null,
    "datArchiveSha256": null,
    "datOriginStatus": "Unverified outer DAT/FPK membership; no installed-currentness or whole-DAT hash claim",
    "provenance": {
      "recordPath": "research/animation-library/reviewed/animation-500-45d9ae07917a78d9e735.json",
      "kind": "exact stock archive/payload/header and technical preview manifest",
      "selectionSha256": "9e9f62c0490a030d8ac3e2d52b439c1c5fd8bba53732c58bb8de1304a313b7a1",
      "nameMatchLimit": "Textual PathCode64 not independently recomputed; exporter prefix is not an ordinal"
    }
  },
  "motionOrigin": {
    "actor": "Stock Soldier_common body-motion source; exact native actor unverified",
    "basis": "Source archive/namespace, not reference model identity",
    "referenceModelIsMotionOrigin": false
  },
  "description": {
    "text": "Decoded stock body-motion reference enetasr_q_die_rd_bdf_b_l; action interpretation unverified.",
    "kind": "project-authored source-identifier-qualified reference",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Exact source identity; no per-clip action observation inferred"
  },
  "authoredDescription": {
    "text": "Decoded stock body-motion reference enetasr_q_die_rd_bdf_b_l; action interpretation unverified.",
    "kind": "project-authored source-identifier-qualified reference",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Exact source identity; no per-clip action observation inferred"
  },
  "sourceDescription": {
    "status": "no-verified-community-description",
    "text": null,
    "credit": null,
    "sourceUrl": null,
    "reason": "Unclassified exact source identifier",
    "reviewRecord": "research/animation-library/reviewed/animation-500-45d9ae07917a78d9e735.json"
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
      "role": "rendering/encoding tools"
    },
    {
      "name": "arsenal-pt / OpenAI Codex",
      "role": "authored pipeline/integration"
    }
  ],
  "sourceBatch": "animation-500-45d9ae07917a78d9e735",
  "dedicatedTableSlug": "stock-544f74e2ef58fd6a79996b72adb0f5ae0790e0ed9f4f5ac7105897b796db7cc9"
}
```

</details>
