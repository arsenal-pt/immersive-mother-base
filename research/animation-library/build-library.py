"""Build the MGSV animation reference library from reviewed research records.

Requires Python 3.10+ and Pillow 12.2.0 for deterministic animated thumbnails.
No game, native converter, server or extracted game payload is required.
Original project code: GPL-3.0-only; see the repository LICENSE and CREDITS.md.
"""
from pathlib import Path
from io import BytesIO, StringIO
import argparse
import csv
import hashlib
import html
import json
import posixpath
import sys

from PIL import Image, ImageSequence, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parents[2]
LIB = "research/animation-library"
SOURCE = "research/mtar-punch-combos/animations-metadata.json"
MANIFEST = "media/animation-previews/2026-10-15/preview-manifest.json"
THUMBS = "media/animation-previews/library-thumbnails/2026-10-15"
BATCHES = [
    {"id": "cqc-starter", "source": SOURCE, "manifest": MANIFEST},
    {"id": "lmg-reloads-002", "source": "research/animation-batches/lmg-reloads/animations-metadata.json",
     "manifest": "media/animation-previews/2026-10-15-lmg-reloads/preview-manifest.json"},
]
BT = chr(96)
FENCE = BT * 3
GROUPS = [
    ("snake-cqc", "Snake CQC combo and transition candidates"),
    ("npc-receivers", "NPC receiving and reaction candidates"),
    ("special-actors", "Special / zombie actor candidates"),
    ("lmg-reloads", "LMG ready/reload candidates"),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def link_from(page, path):
    return posixpath.relpath(path, posixpath.dirname(page))


def group_for(record):
    if record.get("libraryGroup"):
        return record["libraryGroup"]
    if "zmb" in record["name"].rsplit("/", 1)[-1]:
        return "special-actors"
    if record["sourceRole"] == "player":
        return "snake-cqc"
    return "npc-receivers"


def make_thumbnail(data):
    """Resize every composited GIF frame; retain loop and display durations."""
    images, durations = [], []
    with Image.open(BytesIO(data)) as original:
        if original.info.get("loop") != 0:
            raise ValueError("Expected a looping source GIF")
        size = (160, round(original.height * 160 / original.width))
        for frame in ImageSequence.Iterator(original):
            image = frame.convert("RGB")
            image = image.resize(size, Image.Resampling.LANCZOS)
            images.append(image.quantize(colors=96, method=Image.Quantize.MEDIANCUT,
                                         dither=Image.Dither.NONE))
            durations.append(int(frame.info["duration"]))
    stream = BytesIO()
    images[0].save(stream, format="GIF", save_all=True, append_images=images[1:],
                   duration=durations, loop=0, disposal=2, optimize=False)
    result = stream.getvalue()
    with Image.open(BytesIO(result)) as check:
        check_durations = []
        for frame in ImageSequence.Iterator(check):
            frame.load()
            check_durations.append(int(frame.info["duration"]))
        assert check.size == size and check.info.get("loop") == 0
        assert sum(check_durations) == sum(durations)
        assert check.n_frames > 1
    return result, len(durations), len(check_durations), sum(durations)


def render_page(record):
    page = record["detailPage"]
    full = link_from(page, record["media"]["fullGif"]["path"])
    still = link_from(page, record["media"]["stillThumbnail"]["path"])
    catalogue = link_from(page, LIB + "/catalogue.json")
    extraction = record["originalRecords"]["extraction"]
    preview = record["originalRecords"]["preview"]
    rows = [
        ("Game", "Metal Gear Solid V: The Phantom Pain"),
        ("Library ID", BT + record["id"] + BT),
        ("Source archive", BT + record["source"]["archive"] + BT),
        ("Exact clip name", BT + record["source"]["path"] + BT),
        ("Clip hash ID", BT + record["source"]["hashId"] + BT),
        ("Original source role", extraction["sourceRole"]),
        ("Role interpretation", extraction["role"]),
        ("Family / phase", extraction["sequenceFamily"] + " / " + str(extraction["phase"])),
        ("Raw source frames", str(extraction["frameCount"])),
        ("Native frame rate / duration", "Unmeasured / unknown"),
        ("Chosen preview speed", "30 source frames/s; every second source frame sampled"),
        ("Full GIF duration", str(preview["gifDurationMilliseconds"]) + " ms"),
        ("Reference character", preview["referenceCharacter"] + " (untextured)"),
        ("Offline preview", "Actual decoded motion on a mapped reference rig"),
        ("Native gameplay / paired alignment", "Unverified / unverified"),
        ("Ordinary soldier attacker proof", "Unverified"),
        ("Archive SHA-256", BT + record["source"]["archiveSha256"] + BT),
        ("GANI SHA-256", BT + preview["sourceGaniSha256"] + BT),
    ]
    lines = [
        "# " + record["title"], "",
        "[Back to animation library](../README.md) · "
        + "[Complete library data](" + catalogue + ")", "",
        "Click the image to open the original full-size GIF. Its visible character is a "
        "reference model; the source archive below identifies the original animation.", "",
        "[![" + record["title"] + " — full-character offline preview](" + full + ")](" + full + ")", "",
        "[Open full-size GIF](" + full + ") · [Still image](" + still + ")", "",
        "## Technical data", "", "| Field | Value |", "| --- | --- |",
    ]
    lines += ["| " + k + " | " + v.replace("|", "&#124;") + " |" for k, v in rows]
    lines += [
        "", "## Interpretation and limits", "",
        extraction["relationshipNote"], "",
        "The preview speed is a presentation choice. Individual clips have no matched "
        "partner or held weapon; names alone do not prove unarmed punching. "
        "Hair, scarf and holster motion uses mapped-ancestor fallbacks. Native Fox "
        "cloth/twist behavior, timing, interaction contact and actor compatibility remain unverified.", "",
        "The historical extraction record below keeps its original confidence fields. "
        "Its original visualConfirmed=false predates the later offline preview; it is "
        "not a claim that the library has no GIF. Offline visualization and native "
        "gameplay proof are separate fields.", "",
        "<details>", "<summary>Complete extraction and preview records</summary>", "",
        FENCE + "json",
        json.dumps(record["originalRecords"], indent=2, ensure_ascii=False),
        FENCE, "", "</details>", "",
        "[Extraction method](../../mtar-punch-combos/README.md) · "
        "[Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · "
        "[Credits](../../../CREDITS.md)", "",
    ]
    return "\n".join(lines).encode("utf-8")


PAGE_SIZE = 4


def page_sets(catalogue):
    result = []
    for key, title in GROUPS:
        selected = [e for e in catalogue["entries"] if e["group"] == key]
        chunks = [selected[i:i + PAGE_SIZE] for i in range(0, len(selected), PAGE_SIZE)]
        for index, entries in enumerate(chunks, 1):
            result.append({"group": key, "title": title, "index": index,
                           "count": len(chunks), "entries": entries,
                           "animated": LIB + "/tables/" + key + "-" + str(index) + ".md",
                           "stills": LIB + "/tables/" + key + "-" + str(index) + "-stills.md"})
    return result


def render_table_page(page, stills=False):
    current = page["stills" if stills else "animated"]
    mode = "Still-image mode (no GIFs loaded)" if stills else "Animated preview mode"
    sibling = page["animated" if stills else "stills"]
    nav = []
    for i in range(1, page["count"] + 1):
        suffix = "-stills" if stills else ""
        name = page["group"] + "-" + str(i) + suffix + ".md"
        nav.append("**" + str(i) + "**" if i == page["index"] else "[" + str(i) + "](" + name + ")")
    total = sum(e["media"]["stillThumbnail" if stills else "animatedThumbnail"]["bytes"] for e in page["entries"])
    lines = ["# " + page["title"] + " - page " + str(page["index"]) + " of " + str(page["count"]), "",
             "[Library index](../README.md) · [Switch to " + ("animated previews" if stills else "still images") + "](" + link_from(current, sibling) + ")", "",
             "**" + mode + "** · " + str(len(page["entries"])) + " previews · " + f"{total / 1048576:.2f}" + " MiB of image files. "
             "Click a thumbnail or title for the larger GIF and full clip data.", "",
             "Pages: " + " · ".join(nav), "",
             "The visible model is untextured Ocelot, displaying actual decoded source motions. "
             "All entries are offline reference previews; native timing, pairing and ordinary-soldier "
             "attacker compatibility remain unverified. Durations below use a chosen preview rate.", "",
             "| Preview - click to enlarge | Animation / source | Frames / preview length | Data |",
             "| --- | --- | --- | --- |"]
    for e in page["entries"]:
        detail = link_from(current, e["detailPage"])
        image_path = e["media"]["stillThumbnail" if stills else "animatedThumbnail"]["path"]
        image = '<a href="' + detail + '"><img src="' + link_from(current, image_path) + '" width="160" height="' + str(e["media"]["animatedThumbnail"]["height"]) + '" alt="' + html.escape(e["title"], quote=True) + '"></a>'
        identity = "[" + e["title"] + "](" + detail + ")<br><code>" + e["shortIdentifier"] + "</code><br><code>" + e["source"]["archive"] + "</code>"
        timing = str(e["rawFrameCount"]) + " raw<br>" + f'{e["previewDurationMilliseconds"]/1000:g}' + " s (chosen)"
        lines.append("| " + image + " | " + identity + " | " + timing + " | [Metadata](" + detail + "#technical-data)<br>Offline preview |")
    lines += ["", "Pages: " + " · ".join(nav), "", "[All data (JSON)](../catalogue.json) · [Spreadsheet data (CSV)](../catalogue.csv) · [Research references](../references.md)", ""]
    return "\n".join(lines).encode("utf-8")


def render_readme(catalogue):
    pages = page_sets(catalogue)
    max_bytes = max(sum(e["media"]["animatedThumbnail"]["bytes"] for e in p["entries"]) for p in pages)
    lines = [
        "# MGSV Animation Reference Library", "",
        "A visual reference for researching animations in **Metal Gear Solid V: The Phantom Pain**. "
        "Browse **" + str(catalogue["entryCount"]) + " decoded clips** across explicitly scoped categories, with exact source identities, larger GIF views and complete technical records.", "",
        "**This index loads no GIFs or thumbnails.** Expand a category and choose a table page. "
        "Each animated table loads **at most four small GIFs**; still-image pages run no animations. "
        "Click a preview or title to open one larger clip. No mod, dashboard or running game is needed.", "",
        "[All data (JSON)](catalogue.json) · [Spreadsheet data (CSV)](catalogue.csv) · "
        "[Additional animation references](references.md) · [Research plan](RESEARCH-PLAN.md) · "
        "[Extraction research](../mtar-punch-combos/README.md)", "",
        "## Browse by section", "",
        "The largest current animated page contains " + f"{max_bytes / 1048576:.2f}" + " MiB of thumbnail files. "
        "Separate pages bound the number of animations loaded; collapsed HTML sections alone do not guarantee that images are deferred.", "",
    ]
    for key, title in GROUPS:
        selected = [e for e in catalogue["entries"] if e["group"] == key]
        lines += ["<details>", "<summary><strong>" + title + "</strong> - " + str(len(selected)) + " clips</summary>", "",
                  "| Page | Clip range | Animated table | Still-image table |", "| --- | --- | --- | --- |"]
        for page in [p for p in pages if p["group"] == key]:
            first = page["entries"][0]["shortIdentifier"]
            last = page["entries"][-1]["shortIdentifier"]
            label = BT + first + BT + (" to " + BT + last + BT if first != last else "")
            lines.append("| " + str(page["index"]) + " | " + label + " | [Open " + str(len(page["entries"])) + " GIFs](" + link_from(LIB + "/README.md", page["animated"]) + ") | [Open stills](" + link_from(LIB + "/README.md", page["stills"]) + ") |")
        lines += ["", "</details>", ""]
    lines += [
        "## How to read the previews", "",
        "The visible figure is untextured stock Ocelot, used as a full-character reference for original Snake/NPC source motions. "
        "All are **offline previews**. Durations use a chosen 30 source frames/s; native timing is unmeasured. "
        "Labels retain candidate, receiver, transition and special-actor distinctions. Individual clips have no "
        "matched partner or held weapon, and hair/clothing motion is approximate.", "",
        "Each detail page includes source archive and exact clip path, hash ID, frame counts, sidecar/payload hashes, "
        "role confidence, chosen preview timing and verification limits. Complete extraction/render records are in JSON; "
        "CSV supplies common searchable columns. Stable library IDs use game + archive + clip hash. "
        "Older extraction ordinals remain historical fields because repacking can renumber them. "
        "JSON media paths are relative to the repository root.", "",
        "The [original expanded gallery](../mtar-punch-combos/gallery.md) remains available for historical reference; "
        "it can load more full-size animations at once.", "",
        "## Category coverage", "",
        "The [category ledger](category-progress.json) records the selected source version/list, completed IDs, remaining IDs and next cursor. "
        "The current LMG ready/reload section has two identified entries. Completing that defined scope does not establish all-game LMG coverage. "
        "Stop at the selected category boundary; do not add another category to fill a batch cap.", "",
        "## Reuse and future expansion", "",
        "This is general MGSV animation research hosted in Immersive Mother Base. It does not depend on the mod's "
        "simulation or Infinite Heaven. Future sets can cover idle actions, locomotion, duties, services, training "
        "and reactions, including movements unrelated to Mother Base.", "",
        "A separate animation-library project is a **future direction**, not a second repository created by this update. "
        "Portable JSON/CSV, stable IDs, individual clip pages and explicit media paths support a later move while "
        "preserving provenance, credits and evidence limits. Coverage is scoped to identified source versions/lists, not every animation in the game.", "",
        "Follow the [bounded research plan](RESEARCH-PLAN.md) and [preview workflow](../animation-preview-workflow.md). Reference names from a guide or spreadsheet "
        "are discovery leads, not proof that a clip has been extracted, previewed or tested. See "
        "[reference notes](references.md) for the additional sources and their scope.", "",
        "## Rebuilding", "",
        "The existing extraction catalogue and preview manifest are the input records. Do not hand-edit generated "
        "tables, pages, CSV, JSON or thumbnails. With Python 3.10+ and Pillow 12.2.0 installed, run from the repository root:", "",
        FENCE + "console", "python research/animation-library/build-library.py",
        "python research/animation-library/build-library.py --check", FENCE, "",
        "This reads existing reviewed GIFs, deterministically downscales their composited frames, retains loop and total "
        "display duration, and writes only library documentation and new thumbnails. The full-size GIFs and original "
        "metadata stay unchanged. New batches need explicit input registration/group labels in the builder. "
        "No raw game files are copied, no game is launched, and research media stays outside software packages.", "",
        "## Credits and scope", "",
        "Original game assets/animations: **Konami / Kojima Productions**. Community motion decoding, reference rig "
        "and mappings: **mctrollin**. Model conversion: **FMDL Studio v2 / BobDoleOwndU and contributors**. "
        "Supporting tools include GzsTool, MtarTool, Blender and Pillow. See [full credits](../../CREDITS.md), "
        "[additional source credits](references.md) and the [executed recipe](../mtar-punch-combos/full-character-preview-recipe.md).", "",
        "Created under **arsenal-pt**'s direction; original library code/documentation were developed using "
        "**OpenAI Codex / AI LLMs**. Contributions and corrections are welcome. Eligible original work follows "
        "[GPL-3.0-only](../../LICENSE); rendered game-derived media retains its [asset scope](../../LICENSE-SCOPE.md). "
        "No raw model, rig scene or animation payload is included.", "",
    ]
    return "\n".join(lines).encode("utf-8")


def build(root):
    outputs, entries, identities = {}, [], set()
    batch_records, manifests = [], []
    for registration in BATCHES:
        source_path, manifest_path = registration["source"], registration["manifest"]
        source_bytes = (root / source_path).read_bytes()
        manifest_bytes = (root / manifest_path).read_bytes()
        source, manifest = json.loads(source_bytes), json.loads(manifest_bytes)
        manifests.append(manifest)
        previews = {e["id"]: e for e in manifest["entries"]}
        if len(previews) != len(manifest["entries"]):
            raise ValueError("Duplicate preview identity")
        assert len(source["animations"]) == len(previews)
        batch_records.append({"id": registration["id"], "entryCount": len(previews),
                              "extraction": {"path": source_path, "sha256": sha(source_bytes)},
                              "previews": {"path": manifest_path, "sha256": sha(manifest_bytes)}})
        for original in source["animations"]:
            p = previews[original["id"]]
            assert p["hashId"] == original["hashId"]
            assert p["sourceName"] == original["name"]
            assert p["rawFrameCount"] == original["frameCount"]
            assert p["sourceArchiveSha256"] == original["sourceMtarSha256"]
            identity = "mgsv-tpp-" + original["sourceArchive"].lower() + "-" + original["hashId"].lower()
            if identity in identities:
                raise ValueError("Duplicate stable library identity")
            identities.add(identity)
            full_path = posixpath.dirname(manifest_path) + "/" + p["titledGif"]["path"]
            full = (root / full_path).read_bytes()
            assert sha(full) == p["titledGif"]["sha256"]
            thumb, source_frames, encoded_frames, duration = make_thumbnail(full)
            assert duration == p["gifDurationMilliseconds"]
            thumb_path = THUMBS + "/" + identity + ".gif"
            outputs[thumb_path] = thumb
            still_path = posixpath.dirname(manifest_path) + "/" + p["thumbnail"]["path"]
            assert sha((root / still_path).read_bytes()) == p["thumbnail"]["sha256"]
            record = {
                "id": identity,
                "title": p["title"],
                "shortIdentifier": p["shortIdentifier"],
                "group": group_for(original),
                "source": {"game": "MGSV TPP", "archive": original["sourceArchive"],
                           "archiveSha256": original["sourceMtarSha256"],
                           "path": original["name"], "hashId": original["hashId"],
                           "originalCatalogueId": original["id"]},
                "rawFrameCount": original["frameCount"],
                "nativeFrameRate": None,
                "previewDurationMilliseconds": duration,
                "detailPage": LIB + "/clips/" + identity + ".md",
                "media": {
                    "animatedThumbnail": {"path": thumb_path, "sha256": sha(thumb),
                                          "bytes": len(thumb), "width": 160, "height": Image.open(BytesIO(thumb)).height,
                                          "sourceGifFrames": source_frames,
                                          "encodedFrames": encoded_frames,
                                          "durationMilliseconds": duration, "loop": 0},
                    "fullGif": {"path": full_path, "sha256": sha(full), "bytes": len(full)},
                    "stillThumbnail": {"path": still_path, "sha256": p["thumbnail"]["sha256"],
                                       "bytes": p["thumbnail"]["bytes"]},
                },
                "evidence": {"offlineDecodedPreview": True, "nativeGameplay": False,
                             "nativeTiming": False, "pairedAlignment": False,
                             "ordinarySoldierAttacker": False},
                "originalRecords": {"extraction": original, "preview": p},
            }
            if registration["id"] != "cqc-starter":
                record["sourceBatch"] = registration["id"]
                record["recordPathsBase"] = {"extraction": posixpath.dirname(source_path), "preview": posixpath.dirname(manifest_path)}
            entries.append(record)
            outputs[record["detailPage"]] = render_page(record)
    manifest = manifests[0]  # Preserve the starter's legacy shared reference fields.
    catalogue = {
        "schemaVersion": 1,
        "title": "MGSV Animation Reference Library",
        "game": "Metal Gear Solid V: The Phantom Pain",
        "recordedDate": "2026-10-15",
        "scope": "Reviewed explicitly scoped animation batches; general animation research",
        "pathBase": "repository-root",
        "browsing": {"indexInlineImages": 0, "maxAnimatedPreviewsPerPage": PAGE_SIZE, "stillImageMode": True},
        "identityPolicy": "game + source archive + clip hash; extraction ordinals are historical only",
        "sourceRecords": [record for batch in batch_records
                          for record in (batch["extraction"], batch["previews"])],
        "sourceBatches": batch_records,
        "originalRecordPathsBase": posixpath.dirname(SOURCE),
        "originalPreviewRecordPathsBase": posixpath.dirname(MANIFEST),
        "previewTooling": manifest["tooling"],
        "skinning": manifest["skinning"],
        "timing": manifest["timing"],
        "limits": manifest["limits"],
        "thumbnailEncoding": {"tool": "Pillow", "version": PILLOW_VERSION,
                              "width": 160, "heightPolicy": "Preserve source aspect ratio, nearest pixel", "colors": 96,
                              "resampling": "LANCZOS", "dither": "NONE",
                              "originalFullSizeMediaChanged": False},
        "groups": [{"id": key, "title": title,
                    "count": sum(e["group"] == key for e in entries)}
                   for key, title in GROUPS],
        "entryCount": len(entries),
        "entries": entries,
    }
    outputs[LIB + "/catalogue.json"] = json_bytes(catalogue)
    csv_stream = StringIO(newline="")
    fields = ["id", "title", "group", "archive", "clipName", "hashId", "rawFrames",
              "nativeFrameRate", "chosenSourceFramesPerSecond", "previewMilliseconds",
              "sourceArchiveSha256", "ganiSha256", "fullGifPath", "fullGifSha256",
              "animatedThumbnailPath", "animatedThumbnailSha256", "detailPage",
              "offlinePreview", "nativeGameplay", "pairedAlignment"]
    writer = csv.DictWriter(csv_stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for e in entries:
        writer.writerow(dict(zip(fields, [
            e["id"], e["title"], e["group"], e["source"]["archive"], e["source"]["path"],
            e["source"]["hashId"], e["rawFrameCount"], "",
            e["originalRecords"]["preview"]["chosenSourceFramesPerSecond"],
            e["previewDurationMilliseconds"], e["source"]["archiveSha256"],
            e["originalRecords"]["preview"]["sourceGaniSha256"],
            e["media"]["fullGif"]["path"], e["media"]["fullGif"]["sha256"],
            e["media"]["animatedThumbnail"]["path"],
            e["media"]["animatedThumbnail"]["sha256"], e["detailPage"], True, False, False,
        ])))
    outputs[LIB + "/catalogue.csv"] = csv_stream.getvalue().encode("utf-8")
    outputs[LIB + "/README.md"] = render_readme(catalogue)
    for page in page_sets(catalogue):
        outputs[page["animated"]] = render_table_page(page)
        outputs[page["stills"]] = render_table_page(page, stills=True)
    outputs[THUMBS + "/manifest.json"] = json_bytes({
        "schemaVersion": 1, "purpose": "Paged animation library thumbnails",
        "sourcePreviewManifests": [batch["previews"] for batch in batch_records],
        "generator": LIB + "/build-library.py", "pillowVersion": PILLOW_VERSION,
        "entries": [{"id": e["id"], "sourceFullGif": e["media"]["fullGif"],
                     "animatedThumbnail": e["media"]["animatedThumbnail"]} for e in entries],
    })
    return outputs, catalogue


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Check generated bytes without writing")
    args = parser.parse_args()
    if PILLOW_VERSION != "12.2.0":
        raise SystemExit("Use Pillow 12.2.0 to reproduce the reviewed encoding")
    outputs, catalogue = build(ROOT)
    for name, data in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit("Stale or missing generated file: " + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(json.dumps({
        "mode": "check" if args.check else "write",
        "clips": catalogue["entryCount"],
        "generatedFiles": len(outputs),
        "animatedThumbnailBytes": sum(e["media"]["animatedThumbnail"]["bytes"]
                                     for e in catalogue["entries"]),
        "originalMediaChanged": False,
        "nativeProof": False,
    }))


if __name__ == "__main__":
    main()

