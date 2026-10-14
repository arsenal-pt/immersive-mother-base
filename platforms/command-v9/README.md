# Optional Command Platform 1 — v9.1 / v9-E

This is the frozen **v9 family** geometry experiment requested for the repository. **V9.1** uses original native resource paths and supersedes the original v9 diagnostic that crashed on loading. It is not a completed interior/access fix and is separate from the daily-life core. Prior native loading succeeded; current source packaging is checked offline only.

## What it contains

- Floors, openings, inward-face work and the shared lower-bay layout retained from v8-A.
- The modeled static-mesh no-cull diagnostic on 439 source models / 747 mesh records, including 26 shared prop models.
- Original-path resources; native draw enum `0x20` is used for all targeted mesh records. It also alters routing for glass/decal/alpha/OMBS materials; it does not globally disable engine occlusion, LOD, streaming, characters or particles.
- Three exact rebuilt packs identified by manifest hashes. Shared common props also affect matching props on other department platforms.

**Known failures:** narrow/blocked upright doorway passage, lower-bay floor contact/falling through, inward wall contact, red decals, material/angle popping and incomplete interior visibility. The 32 editor light-plane placeholders are not registered native lights. Do not call this a finished room mod or propagate these collision methods as proven.

## Rebuild locally

Only a BSDIFF40 transformation patch, input/output manifest and original helpers are supplied. The full extracted Blender scene and original/modified game packs are not uploaded. Use your legally obtained local game and keep reconstructed output private.

1. Extract the exact stock packages listed in manifest.json from your owned game, using a separately acquired MGSV archive tool such as [GzsTool](https://github.com/Atvaark/GzsTool). Preserve the listed `Assets/tpp/pack/...` folder layout under a new `stock` folder. Use untouched stock inputs, not previously modded `00.dat` overrides. All listed inputs are stock Mother Base unique/common packs; exact SHA256 verification rejects unsupported versions.
2. Use Python 3.10–3.13 with external [bsdiff4 1.2.6](https://pypi.org/project/bsdiff4/), ideally in a local virtual environment:

```powershell
python -m pip install -r requirements.txt
python rebuild.py --originals-root "D:/MBLab/stock" --output-dir "D:/MBLab/rebuilt-v9.1" --check-only
python rebuild.py --originals-root "D:/MBLab/stock" --output-dir "D:/MBLab/rebuilt-v9.1"
```

The helper verifies every source, patch and target hash, refuses existing output, writes only a new staging folder and never installs, changes saves or launches MGSV. Three packs plus a local receipt are produced. Packaging/install through [SnakeBite/MakeBite](https://github.com/TinManTex/SnakeBite) is a separate manual experimental step. Back up and record replaced resources before testing; restore through that manager/backups. No installer or native acceptance is implied.

## Editing and reproduction

`manifest.json` records byte-exact stock and frozen edited targets. `make_patch.py` regenerates the same patch when given those original and rebuilt folders. To examine/edit the game-derived geometry, unpack your locally rebuilt FPK/FPKD and import local FMDLs through [FMDL Studio v2](https://github.com/BobDoleOwndU/FMDL-Studio-v2/wiki). Keep stock originals immutable and use versioned copies. Rendering, collision GPFP/GEOMS, FOX2 placement and navigation are separate resources; a Blender shader toggle alone cannot fix native collision.

The delta is the frozen editable transformation artifact; the original helper source is included. New geometry work should contribute authored layout/mesh definitions and local reconstruction recipes, with game data external. A fuller parametric platform editor/export pipeline remains on the roadmap. Do not publish extracted/reconstructed game assets with a contribution.

Original helper code is GPL-3.0-only. Underlying game resources and external bsdiff4/tools retain their own rights/terms; see ../../LICENSE-SCOPE.md. Patch format/API reference: [bsdiff4 upstream](https://github.com/ilanschnell/bsdiff4). Inputs total about46.4MB; rebuilt targets total about27.7MB. The patch requires those originals, rather than containing full game packages.
