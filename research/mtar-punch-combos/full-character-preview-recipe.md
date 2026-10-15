# Full-character animation preview recipe

The previews show actual selected MGSV animations decoded by mctrollin's community MTAR tools. The visible character is the stock Ocelot model, used as a consistent offline reference for all 25 clips. Snake clip names identify the source animation, not the model's appearance. No animation was generated, manually recreated or smoothed for these GIFs.

The catalogue separates 11 Snake attack/transition candidates, 8 NPC hit receivers, and 6 special/zombie punch candidates. A hit receiver is not proof that ordinary Mother Base soldiers have an attacker combo. The front/back phase links remain name-based hypotheses; separate previews do not establish native contact, timing or paired alignment. Each body clip is shown alone, without its partner or a held weapon/equipment prop. CQC/asr family names do not by themselves prove unarmed punching semantics; original role confidence remains naming-based without native contextual verification.

## Tested community route

1. Read the indexed stock `chunk0.dat` through Atvaark's `GzsTool.Core.Qar.QarFile` in read-only mode. Check the current entry hash/offset against the source index, then export only `/Assets/tpp/pack/mission2/common/mis_com_ocelot.fpk`. Run actual GzsTool 0.5.3 on a staged copy. The FPK SHA256 is `bd493cbfb2edfa534a932b5001ebd87d7eaf6458bd22510245daa403c4c9d893`.
2. Use `/Assets/tpp/chara/oce/Scenes/oce0_main0_def.fmdl`, SHA256 `54b95f689a5d4e9e0299e9a6ab128eff8d89e23feab3e86104179a7be08ed854`. It contains the complete head/body and 21 weighted meshes. Generic DDS3/PRS2 body files were rejected as final references because their heads are separate; face `_cov` files did not solve that assembly. Those diagnostics did not become final media.
3. In a fresh private copy of the installed FMDL Studio Unity project, call `FmdlImporter.ReadWithoutAssetImportContext(input)` and `COLLADAConverter.ConvertToCOLLADA(model.gameObject, output)`. [PreviewPartsExport.cs](preview-tools/PreviewPartsExport.cs) is authored API glue used by this run. It reads `MGSV_CHARACTER_PARTS_DIR`, imports copied FMDLs from its `inputs` folder and writes COLLADA/mesh inventories beside it. Run Unity with `-batchmode -nographics -job-worker-count 2 -executeMethod PreviewPartsExport.Run`. Its host must contain the installed community plugin and required references. Preserve its import cache: the initial cold host imported 1508 shader assets and hit a 420s startup limit; the warm retry reached the exporter and passed. Do not repeat a cold host for each character.
4. Import COLLADA with Blender 3.6.23's standard importer using [Import-Character-Collada.py](preview-tools/Import-Character-Collada.py). This verifies weighted vertices/armatures and saves a new private `.blend`. Blender 5.2.2 then reads that scene. This run used untextured studio shading; missing texture notices were recorded, not hidden as successful texture conversion.
5. Decode each selected original MTAR with the installed mctrollin tools and import only the exact matching member into the author's reference rig. [Render-MtarCharacter.py](preview-tools/Render-MtarCharacter.py) uses the full path hash and checks the decoded frame count against the extraction catalogue. MtarTool's numbered/XML ordinal is not the original MTAR header index: Snake front 1 is header 6/data 86, while the NPC front 1 receiver is header 965/data 117. Select by full hash rather than assuming those ordinals match.
6. Keep the original stock mesh geometry and weight values. Map native groups using the author's `human_finger_mapping_bones.txt`; merge groups that resolve to the same target while preserving every vertex's weight sum within0.00001. Blender's standard Armature modifier targets the author's `Skeleton_mgs5_Rigify`, evaluated from the actual imported animation. A manual native-bone matrix assignment was tested, visibly distorted and rejected; it is not the published route.
7. Render clean PNGs before text. Fit one fixed camera per clip to all evaluated mesh vertices at every integer frame from 0 through N, including root travel. Render every second frame in 0..N-1 and save endpoint N separately. [Encode-MtarCharacterGIFs.py](preview-tools/Encode-MtarCharacterGIFs.py) produces separate clean GIFs, titled GIFs, thumbnails, contact sheets and a metadata manifest. It verifies clean-frame hashes and decodes every generated GIF to check frame count, dimensions and delays.

All four helpers are authored orchestration/interchange glue; they import or call community implementations rather than embedding an animation/FMDL decoder. Installed binaries, upstream source, models, rigs, `.mtar`, `.gani`, companions, `.blend` and clean source renders stay private.

## Reference rig and secondary motion

The community example's referenced mesh scenes were absent, so the stock Ocelot character was independently converted through FMDL Studio. The example rig and its supplied track/native-bone maps remain the motion/deformation reference. Native calf names have two authored split-segment mappings; the renderer chooses the first/proximal segment and records the alternatives.

Ocelot has 18 hair, scarf and holster simulation/helper bones outside the generic map. Those weighted bones inherit the nearest mapped native ancestor's transform. The exact 18 names and ancestors are in the preview manifest. This is an explicit offline display approximation: it adds no limb motion or native secondary simulation. The community rig also does not implement the complete Fox twist/cloth/physics system. Clothing intersections and deformation differences on a reference character must not be treated as native gameplay behavior.

## Timing and visual meaning

The source catalogue supplies raw frame counts, not measured playback rates. These previews choose 30 source frames per second and sample every 2 frames, nominally15 GIF frames per second. GIF delays use cumulative 10ms rounding; an odd final source interval is shorter. `nativeFrameRate` remains null. The raw layout rate field is retained as an unverified value/enum rather than interpreted as FPS.

The endpoint pose is preserved in a separate clean PNG but excluded from the GIF so the selected interval lasts N/30 seconds at the chosen rate. Each GIF loops its individual extracted segment. A jump at the loop boundary can reflect a phase intended to transition into another clip; no easing, root removal or time warp was added.

Exact archive identity, payload hashes, decoded frame counts, action isolation, weight conservation and offline renders are checked. Native animation compatibility, ordinary-soldier attack behavior, actor contact and game timing remain unproved.

## Replaying the authored helpers

Supply your own private copies of the original MTARs, installed community add-on/reference rig/maps, converted weighted character scene, and the existing `animations-metadata.json`. The renderer accepts only a fresh output directory. Example PowerShell argument structure:

```powershell
& $Blender52 --background --factory-startup --disable-autoexec --threads 2 `
  --python Render-MtarCharacter.py -- `
  --tool-dir $CommunityAddon --rig-file $ReferenceRig `
  --track-map $TrackMap --bone-map $NativeBoneMap `
  --character-blend $PrivateWeightedCharacter `
  --catalogue $Catalogue --mtar-root $PrivateMtarRoot --output $FreshCleanRenderDirectory

& $Python Encode-MtarCharacterGIFs.py `
  --renders $FreshCleanRenderDirectory --media-output $FreshPublicMediaDirectory `
  --clean-gif-output $FreshPrivateCleanGifDirectory --contact-output $FreshPrivateContactDirectory `
  --font $InstalledFontFile --tool-dir $CommunityAddon
```

The MTAR root has `<archive-name>/<archive-name>.mtar` beneath it. `--clip-id` can select one member for the renderer; omit it for the bounded25-entry catalogue. The encoder intentionally requires 25 render receipts for this published batch. The renderer and encoder were actually executed on all 25 entries; the parameterized COLLADA importer was also executed on a new copy.

The reference commit below is a cited source/catalog pin. A caller-supplied add-on directory is not automatically proven to equal that revision. The manifest therefore records the actual installed Python file hashes used for this run separately from the reference revision. Verify your installation and retain its receipts.

## Credits and pinned API references

- [mctrollin, fox_engine_mtar_tools_blender](https://github.com/mctrollin/fox_engine_mtar_tools_blender/tree/7fa90e589349ad4ba87102f0061a8d8d343a8bf4): MTAR/GANI decoding, import, reference rig and mappings. Its documented limitations apply.
- [BobDoleOwndU, FMDL Studio v2 COLLADA converter](https://github.com/BobDoleOwndU/FMDL-Studio-v2/blob/d580b94215cc007df6c38bdb0bfce6a0f30e4701/FMDL-Studio-v2/Assets/Fmdl%20Studio/Scripts/Static/COLLADAConverter.cs), [FMDL importer](https://github.com/BobDoleOwndU/FMDL-Studio-v2/blob/d580b94215cc007df6c38bdb0bfce6a0f30e4701/FMDL-Studio-v2/Assets/Fmdl%20Studio/Scripts/Classes/FmdlImporter.cs), and [author setup guide](https://github.com/BobDoleOwndU/FMDL-Studio-v2/wiki/Setting-up-Fmdl-Studio-v2/2cdaa4eefe9b8f57357e865870d902e961fb82d9). Tested portable DLL SHA256: `ec5ded0406f28c2d7bbdf7d7d138ec7d5c5c2068f60751a730ba0fb1685472c9`.
- [Atvaark, GzsTool 0.5.3](https://github.com/Atvaark/GzsTool/releases/tag/v0.5.3), and BobDoleOwndU's tool/hash contributions. [MGSV wiki tool guidance](https://github.com/mgsvmoddingwiki/mgsvmoddingwiki.github.io/blob/2326cdf753a6fcfefb1867dd66ed97a078d4d114/wiki/GzsTool.md).
- [BobDoleOwndU, MtarTool](https://github.com/BobDoleOwndU/MtarTool) supplied the original extraction. This preview stage reads those immutable source archives; it does not repack or replace game files.
- Blender Foundation/community for Blender and COLLADA import; Unity Technologies for the converter host; Pillow contributors for GIF/title encoding. Original MGSV character and animation content belongs to its rights holders; the authored software license does not relicense game content.
