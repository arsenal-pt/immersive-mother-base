# Stock motion reference: enetasr_s_rdy_ris

[Library index](../README.md) · [Complete catalogue](../catalogue.json)

Decoded stock body-motion reference enetasr_s_rdy_ris; action interpretation unverified.

[![Stock motion reference: enetasr_s_rdy_ris - offline full-character reference](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.gif)](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.gif)

[Full GIF](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.gif) · [Still image](../../../media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.png)

**Exact identifier:** `enetasr_s_rdy_ris`. **Tags:** stock body motion, Soldier_common, source-derived label, Ocelot reference mesh.

Source-derived motion label; shared pipeline approved. Per-clip visual review status is in provenance; no action or native compatibility is inferred.

## Technical data

| Field | Value |
| --- | --- |
| Virtual GANI | /Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_s_rdy_ris.gani |
| MTAR | Unverified |
| Historical FPK | Unverified |
| Historical DAT | Unverified |
| Source archive SHA256 | 6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e |
| GANI SHA256 | a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d |
| Source identity limit | Payload SHA256 identity; name PathCode64 not independently recomputed; exporter prefix is not an ordinal |
| Source header / decoded body tracks / raw frames | 1064 / 18 / 20 |
| Chosen source rate / native rate | 30 source frames/s / unknown |
| GIF frames / duration | 10 / 670 ms; separate endpoint20 excluded |
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

[Full credits](../../../CREDITS.md) · [License scope](../../../LICENSE-SCOPE.md) · [Exact reviewed source/provenance](../reviewed/animation-500-cf612f40346e5dfb27fc.json)

<details>
<summary>Complete source and preview provenance</summary>

```json
{
  "id": "mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d",
  "title": "Stock motion reference: enetasr_s_rdy_ris",
  "shortIdentifier": "enetasr_s_rdy_ris",
  "group": "stock-soldier",
  "source": {
    "game": "MGSV TPP",
    "archive": "Soldier_common",
    "archiveSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
    "path": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_s_rdy_ris",
    "hashId": "327355612aa80",
    "payloadSha256": "a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d",
    "originalCatalogueId": "mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d"
  },
  "identityBasis": "Exact retained archive plus full payload SHA256; header index and textual name retained separately",
  "rawFrameCount": 20,
  "nativeFrameRate": null,
  "previewDurationMilliseconds": 670,
  "detailPage": "research/animation-library/clips/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.md",
  "media": {
    "fullGif": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.gif",
      "sha256": "bb18b2e54e625d04adfcafc933d737f796ef8457d9ed1dd4553e1fd996b26135",
      "bytes": 651053
    },
    "animatedThumbnail": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.gif",
      "sha256": "bb18b2e54e625d04adfcafc933d737f796ef8457d9ed1dd4553e1fd996b26135",
      "bytes": 651053,
      "width": 480,
      "height": 614,
      "displayWidth": 160,
      "displayHeight": 205,
      "kind": "Full GIF displayed small; download bytes unchanged",
      "encodedFrames": 10,
      "durationMilliseconds": 670,
      "loop": 0
    },
    "stillThumbnail": {
      "path": "media/animation-previews/animation-500-20261029/mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d.png",
      "sha256": "0d3ed68d655895e708cb0050c03efcd4b2a16262ce06ed1ef146df246020a396",
      "bytes": 99700,
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
      "headerIndex": 1064,
      "fullArchivePathHash": "0xfc5327355612aa80",
      "hashId": "327355612aa80",
      "payloadSha256": "a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d",
      "payloadBytes": 2944,
      "tracksOffset": 8155568,
      "rawFrameCount": 20,
      "retainedNameCandidates": [
        "Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/0730_enetasr_s_rdy_ris.gani"
      ],
      "selectionStatus": "eligible-source-bound-decoder-and-mapping-pending",
      "exporterPath": "Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/0730_enetasr_s_rdy_ris.gani",
      "shortIdentifier": "enetasr_s_rdy_ris",
      "name": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_s_rdy_ris",
      "id": "mgsv-tpp-soldier_common-payloadsha256-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d",
      "sourceArchive": "Soldier_common",
      "sourceMtarSha256": "6f535a29e1c5b6da70514984a47f8a5c988aa468f1d5c87c37f212263dcc001e",
      "frameCount": 20,
      "sourceRole": "authentic-stock-body-reference-pending-decode",
      "role": "stock_soldier_body_reference",
      "sequenceFamily": "source-name-only",
      "phase": null,
      "phaseKind": "unclassified",
      "sidecars": [
        {
          "extension": ".gani",
          "sha256": "a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d"
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
      "sourceGaniSha256": "a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d",
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
        18
      ],
      "separateEndpointFrame": 20,
      "gifDurationMilliseconds": 670,
      "referenceCharacterBlendSha256": "68e793fb833999c2489d9de1811d6f9b27df471c2e418b4b872a1200ea0b105c",
      "historicalDifferentReferenceSha256": "6c1cb2ead2a82b78bd1240ad880c1bac0ba2bfe1d7c8f04aa4c311852a286a28",
      "sourceToolPins": {
        "scriptSha256": "13c2fe0cc9ba420c28e2ced10c2f3b6e230d473f7ae9b698d68703bfc305adf6",
        "referenceRigSha256": "c020ff7c2c39dd82b9b084999bcbdfa35c2d171d94552fe84696a90439c59445",
        "trackMapSha256": "2755175dc333ee1320e16d732e6c0707d5f266ff7f91e5b122ca1d4ad3f34a81",
        "boneMapSha256": "b6375a070f719de38a16648081eb124d3e5a3235b872285510443ece54f47d97"
      },
      "renderBatchReceiptSha256": "e03cdfd59bf91e39e9b0b9a8bf5fe04ce76f0c00adf4c70491899b8bfaf268c8",
      "renderReceiptSha256": "6d1fac02eb34fd90db9ec3966e86139ba32a1a98d6ae6538aa43654319da1d2e",
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
      "rawFrameCount": 20,
      "decodedBodyTrackCount": 18,
      "sourceHeaderIndex": 1064,
      "gifMotionFrames": 10,
      "encodedManifestSha256": "970379b1715c12b715851c7a0e9328dc45c8d4faa640c080a92c4fd813b44984",
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
    "ganiVirtualPath": "/Assets/tpp/motion/SI_game/fani/bodies/enet/enetasr/enetasr_s_rdy_ris.gani",
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
      "recordPath": "research/animation-library/reviewed/animation-500-cf612f40346e5dfb27fc.json",
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
    "text": "Decoded stock body-motion reference enetasr_s_rdy_ris; action interpretation unverified.",
    "kind": "project-authored source-identifier-qualified reference",
    "credit": "arsenal-pt / OpenAI Codex",
    "basis": "Exact source identity; no per-clip action observation inferred"
  },
  "authoredDescription": {
    "text": "Decoded stock body-motion reference enetasr_s_rdy_ris; action interpretation unverified.",
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
    "reviewRecord": "research/animation-library/reviewed/animation-500-cf612f40346e5dfb27fc.json"
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
  "sourceBatch": "animation-500-cf612f40346e5dfb27fc",
  "dedicatedTableSlug": "stock-a708587bcad40eaba89a8bda75b6e8edeff0d873dddb69aa4a7a1747b1fb7f0d"
}
```

</details>
