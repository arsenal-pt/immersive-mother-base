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
METADATA_REVIEW = LIB + "/metadata-source-review.json"
CONTAINER_REVIEW = LIB + "/container-provenance.json"
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



def enrich_metadata(record, archive, source, source_path, review, container_review):
    """Keep authored labels, source locations and external descriptions distinct."""
    original = record["originalRecords"]["extraction"]
    category = dict(GROUPS)[record["group"]]
    tags = ["offline-reference", "source-" + original["sourceRole"]]
    if record["group"] == "snake-cqc":
        tags += ["cqc", "combo-candidate"]
        if original["sequenceFamily"] == "related_combo_transition":
            tags += ["transition-candidate"]
    elif record["group"] == "npc-receivers":
        tags += ["cqc", "receiver-candidate", "reaction-candidate"]
    elif record["group"] == "special-actors":
        tags += ["special-actor", "zombie-namespace", "punch-candidate"]
    elif record["group"] == "lmg-reloads":
        tags += ["lmg", "reload-candidate"]
    else:
        raise ValueError("Unclassified library category: " + record["group"])
    if original["sequenceFamily"] in ("front", "back"):
        tags += [original["sequenceFamily"] + "-family"]
    if original.get("phase") is not None:
        tags += ["phase-" + str(original["phase"])]
    if original.get("phaseKind") in ("start", "ending"):
        tags += [original["phaseKind"] + "-candidate"]
    posture = next((x for x in ("kneeling", "standing") if x in record["title"].lower()), None)
    if posture:
        tags += [posture]
    dictionary = source.get("toolRuntimeHashes", {}).get("mtar", {}).get("mtar_dictionary.txt")
    if not dictionary:
        dictionary = next((x["sha256"] for x in source.get("provenance", {}).get("MtarToolRuntimeFileHashes", []) if x["path"] == "mtar_dictionary.txt"), None)
    locations = {
        "ganiVirtualPath": original["name"] + ".gani",
        "ganiDirectory": posixpath.dirname(original["name"]),
        "archiveFile": archive["name"] + ".mtar",
        "recordedContainerLabel": archive.get("pack"),
        "archiveVirtualPath": None,
        "containerVirtualPath": None,
        "containerLocationStatus": "label-only; exact virtual container/archive path is not recorded in the portable input",
        "provenance": {"kind": "retained-extraction-record", "recordPath": source_path,
                       "archiveSha256": original["sourceMtarSha256"], "dictionarySha256": dictionary,
                       "pathRule": "Exact resolved member stem plus the extracted .gani payload extension; no extraction ordinal used"},
    }
    origins = [x for x in container_review["archives"] if x["archiveFile"] == locations["archiveFile"] and x["archiveSha256"] == original["sourceMtarSha256"]]
    if len(origins) > 1:
        raise ValueError("Ambiguous container source identity")
    locations.update(datArchive=None, datArchiveSha256=None)
    if origins:
        origin = origins[0]
        for key in ("archiveVirtualPath", "containerVirtualPath", "containerSha256", "datArchive", "datArchiveSha256", "datOriginStatus"):
            locations[key] = origin[key]
        locations["containerLocationStatus"] = "known historical virtual paths; exact retained FPK/MTAR hashes verified"
        locations["provenance"]["containerReview"] = CONTAINER_REVIEW
        locations["provenance"]["containerEvidence"] = origin["evidence"]
        locations["provenance"]["containerVerification"] = origin["verification"]
    key = (locations["archiveFile"], original["sourceMtarSha256"], locations["ganiVirtualPath"], original["hashId"])
    matches = []
    for candidate in review["verifiedDescriptions"]:
        identity = candidate["identity"]
        candidate_key = (identity["archiveFile"], identity["archiveSha256"], identity["ganiVirtualPath"], identity["hashId"])
        if candidate_key == key:
            matches.append(candidate)
    if len(matches) > 1:
        raise ValueError("Ambiguous external description identity: " + record["id"])
    description = {"status": "unavailable-no-verified-exact-match", "text": None, "credit": None,
                   "sourceUrl": None, "reason": review["unavailableReason"], "reviewRecord": METADATA_REVIEW}
    if matches:
        match = matches[0]
        if not all(match.get(x) for x in ("text", "credit", "sourceUrl", "sourceRevision", "verification")):
            raise ValueError("Missing description provenance")
        description = {"status": "verified-exact-source-match", **match, "reviewRecord": METADATA_REVIEW}
    credits = [
        {"name": "Konami / Kojima Productions", "role": "original game animation"},
        {"name": "mctrollin and contributors", "role": "community motion decoder, reference rig and mappings"},
        {"name": "arsenal-pt / OpenAI Codex", "role": "authored catalogue category, tags and preview summary"},
    ]
    discovery = original.get("discoverySource", {})
    if discovery.get("workbookCredit"):
        credits.append({"name": discovery["workbookCredit"], "role": "selected workbook discovery", "sourceCell": discovery["sourceCell"], "sourceSha256": discovery["workbookSha256"]})
    if description["credit"]:
        credits.append({"name": description["credit"], "role": "verified external description", "sourceUrl": description["sourceUrl"]})
    record.update(
        category={"id": record["group"], "label": category}, tags=list(dict.fromkeys(tags)),
        classificationProvenance={"kind": "project-authored", "credit": "arsenal-pt / OpenAI Codex",
            "categoryAndCandidateTags": "Retained source namespace, role, family and phase metadata; interpretations remain candidates",
            "postureTags": "Previously reviewed offline preview title" if posture else None,
            "extractionRecordPath": source_path, "nativeGameplayProof": False},
        locations=locations,
        authoredDescription={"text": record["title"] + " on an untextured reference character.",
            "kind": "project-authored preview summary", "credit": "arsenal-pt / OpenAI Codex",
            "basis": "Previously reviewed titled offline preview; source meanings/native use remain unverified"},
        sourceDescription=description, credits=credits)


def html_code(value):
    return "<code>" + html.escape(value or "Unrecorded", quote=True).replace("|", "&#124;") + "</code>"


def render_csv(entries):
    stream = StringIO(newline="")
    fields = ["id", "title", "group", "archive", "clipName", "hashId", "rawFrames",
              "nativeFrameRate", "chosenSourceFramesPerSecond", "previewMilliseconds",
              "sourceArchiveSha256", "ganiSha256", "fullGifPath", "fullGifSha256",
              "animatedThumbnailPath", "animatedThumbnailSha256", "detailPage",
              "offlinePreview", "nativeGameplay", "pairedAlignment",
              "category", "tags", "ganiVirtualPath", "ganiDirectory", "archiveFile",
              "containerLabel", "archiveVirtualPath", "containerVirtualPath", "datArchive", "datOriginStatus",
              "sourceDescriptionStatus", "sourceDescription", "sourceDescriptionCredit", "sourceDescriptionUrl",
              "authoredDescription", "classificationCredit", "discoveryCredit",
              "tagProvenance", "locationProvenance", "sourceDescriptionReview", "credits"]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for e in entries:
        loc, desc = e["locations"], e["sourceDescription"]
        writer.writerow({
            "id": e["id"], "title": e["title"], "group": e["group"], "archive": e["source"]["archive"],
            "clipName": e["source"]["path"], "hashId": e["source"]["hashId"], "rawFrames": e["rawFrameCount"],
            "nativeFrameRate": "", "chosenSourceFramesPerSecond": e["originalRecords"]["preview"]["chosenSourceFramesPerSecond"],
            "previewMilliseconds": e["previewDurationMilliseconds"], "sourceArchiveSha256": e["source"]["archiveSha256"],
            "ganiSha256": e["originalRecords"]["preview"]["sourceGaniSha256"], "fullGifPath": e["media"]["fullGif"]["path"],
            "fullGifSha256": e["media"]["fullGif"]["sha256"], "animatedThumbnailPath": e["media"]["animatedThumbnail"]["path"],
            "animatedThumbnailSha256": e["media"]["animatedThumbnail"]["sha256"], "detailPage": e["detailPage"],
            "offlinePreview": True, "nativeGameplay": False, "pairedAlignment": False,
            "category": e["category"]["label"], "tags": ";".join(e["tags"]), "ganiVirtualPath": loc["ganiVirtualPath"],
            "ganiDirectory": loc["ganiDirectory"], "archiveFile": loc["archiveFile"], "containerLabel": loc["recordedContainerLabel"],
            "archiveVirtualPath": loc["archiveVirtualPath"], "containerVirtualPath": loc["containerVirtualPath"],
            "datArchive": loc["datArchive"], "datOriginStatus": loc.get("datOriginStatus", "Unrecorded"),
            "sourceDescriptionStatus": desc["status"], "sourceDescription": desc["text"],
            "sourceDescriptionCredit": desc["credit"], "sourceDescriptionUrl": desc["sourceUrl"],
            "authoredDescription": e["authoredDescription"]["text"], "classificationCredit": e["classificationProvenance"]["credit"],
            "discoveryCredit": ";".join(c["name"] for c in e["credits"] if c["role"] == "selected workbook discovery"),
            "tagProvenance": e["classificationProvenance"]["categoryAndCandidateTags"] + ("; posture: " + e["classificationProvenance"]["postureTags"] if e["classificationProvenance"]["postureTags"] else ""),
            "locationProvenance": loc["provenance"]["recordPath"], "sourceDescriptionReview": desc["reviewRecord"],
            "credits": ";".join(c["name"] + ": " + c["role"] for c in e["credits"]),
        })
    return stream.getvalue().encode("utf-8")


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
    extraction, preview = record["originalRecords"]["extraction"], record["originalRecords"]["preview"]
    loc, desc = record["locations"], record["sourceDescription"]
    source_note = link_from(page, LIB + "/description-sources.md")
    rows = [
        ("Game", "Metal Gear Solid V: The Phantom Pain"),
        ("Library ID", BT + record["id"] + BT),
        ("Category", record["category"]["label"]),
        ("Tags (authored retrieval labels)", ", ".join(record["tags"])),
        ("Source archive", BT + record["source"]["archive"] + BT),
        ("Exact clip stem (retained)", BT + record["source"]["path"] + BT),
        ("Virtual GANI file", BT + loc["ganiVirtualPath"] + BT),
        ("Virtual GANI directory", BT + loc["ganiDirectory"] + BT),
        ("MTAR file", BT + loc["archiveFile"] + BT),
        ("Recorded container label", loc["recordedContainerLabel"] or "Unrecorded"),
        ("Virtual MTAR path", loc["archiveVirtualPath"] or "Unrecorded"),
        ("Virtual FPK path", loc["containerVirtualPath"] or "Unrecorded"),
        ("Recorded DAT origin", loc["datArchive"] or "Unrecorded"),
        ("DAT version limit", loc.get("datOriginStatus", "Unrecorded")),
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
        ("Dictionary snapshot SHA-256", BT + loc["provenance"]["dictionarySha256"] + BT if loc["provenance"]["dictionarySha256"] else "Unrecorded"),
    ]
    description = desc["text"] if desc["text"] is not None else "Unavailable. " + desc["reason"]
    lines = ["# " + record["title"], "",
        "[Back to animation library](../README.md) · [Complete library data](" + link_from(page, LIB + "/catalogue.json") + ")", "",
        "Click the image to open the original full-size GIF. Its visible character is a reference model; source identity is recorded separately below.", "",
        "[![" + record["title"] + " — full-character offline preview](" + full + ")](" + full + ")", "",
        "[Open full-size GIF](" + full + ") · [Still image](" + still + ")", "",
        "## Classification and descriptions", "",
        "**Category:** " + record["category"]["label"] + ". **Tags:** " + ", ".join(BT + x + BT for x in record["tags"]) + ".", "",
        "**Authored preview description:** " + record["authoredDescription"]["text"] + " Credit: " + record["authoredDescription"]["credit"] + ". " + record["authoredDescription"]["basis"] + ".", "",
        "**Community source description:** " + description, "",
        "Match status: " + BT + desc["status"] + BT + ". [Description sources and matching rules](" + source_note + ").", "",
        "The source directory is a virtual game-asset directory. The retained clip stem and the .gani file path are separate fields. [Container provenance](../container-provenance.json) joins retained FPK/MTAR hashes and historical extraction logs; recorded DAT origins do not verify current DAT contents.", "",
        "## Technical data", "", "| Field | Value |", "| --- | --- |"]
    lines += ["| " + k + " | " + v.replace("|", "&#124;") + " |" for k, v in rows]
    lines += ["", "## Credits and evidence", ""]
    lines += ["- **" + c["name"] + "** — " + c["role"] + ("; " + c["sourceCell"] if c.get("sourceCell") else "") + "." for c in record["credits"]]
    lines += ["", "Categories/tags and preview summaries are project-authored. Candidate roles/families come from retained naming metadata; posture labels come from the already reviewed offline preview. An unavailable community description has no attributed per-entry source author. [Full tool/model credits](../../../CREDITS.md).", "",
        "## Interpretation and limits", "", extraction["relationshipNote"], "",
        "Preview speed is a presentation choice. Individual clips have no matched partner or held weapon. Labels alone do not prove native weapon handling, interaction contact or actor compatibility. Hair, scarf and holster motion uses mapped-ancestor fallbacks; native Fox cloth/twist and timing remain unverified.", "",
        "Historical extraction confidence fields below are unchanged. Original visualConfirmed=false predates the later offline preview; offline visualization and native gameplay proof remain separate fields.", "",
        "<details>", "<summary>Classification, location and description provenance</summary>", "", FENCE + "json",
        json.dumps({k: record[k] for k in ("category", "tags", "classificationProvenance", "locations", "authoredDescription", "sourceDescription", "credits")}, indent=2, ensure_ascii=False),
        FENCE, "", "</details>", "", "<details>", "<summary>Complete original extraction and preview records</summary>", "", FENCE + "json",
        json.dumps(record["originalRecords"], indent=2, ensure_ascii=False), FENCE, "", "</details>", "",
        "[Exact extraction catalogue](" + link_from(page, loc["provenance"]["recordPath"]) + ") · [Full-character recipe](../../mtar-punch-combos/full-character-preview-recipe.md) · [Credits](../../../CREDITS.md)", ""]
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
    sibling = page["animated" if stills else "stills"]
    mode = "Still-image mode (no GIFs loaded)" if stills else "Animated preview mode"
    nav = []
    for i in range(1, page["count"] + 1):
        name = page["group"] + "-" + str(i) + ("-stills" if stills else "") + ".md"
        nav.append("**" + str(i) + "**" if i == page["index"] else "[" + str(i) + "](" + name + ")")
    total = sum(e["media"]["stillThumbnail" if stills else "animatedThumbnail"]["bytes"] for e in page["entries"])
    lines = ["# " + page["title"] + " - page " + str(page["index"]) + " of " + str(page["count"]), "",
        "[Library index](../README.md) · [Switch to " + ("animated previews" if stills else "still images") + "](" + link_from(current, sibling) + ")", "",
        "**" + mode + "** · " + str(len(page["entries"])) + " previews · " + f"{total / 1048576:.2f}" + " MiB of image files. Click a preview or title for its larger GIF and complete data.", "",
        "Pages: " + " · ".join(nav), "",
        "Categories/tags are authored retrieval labels; candidate source roles and observed reference posture remain distinct. GANI paths are virtual asset locations. Recorded container chains are historical source locations; current DAT contents are unverified. [Description matching and credits](../description-sources.md) explain why a community description may be unavailable.", "",
        "All clips are offline Ocelot reference previews. Native timing, weapon/contact, pairing and actor compatibility remain unverified; duration uses a chosen preview rate.", "",
        "| Preview | Animation | Category | Tags | Virtual GANI directory / file | MTAR / container location | Community source description | Credits | Frames / data |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for e in page["entries"]:
        detail = link_from(current, e["detailPage"])
        img = e["media"]["stillThumbnail" if stills else "animatedThumbnail"]["path"]
        image = '<a href="' + detail + '"><img src="' + link_from(current, img) + '" width="160" height="' + str(e["media"]["animatedThumbnail"]["height"]) + '" alt="' + html.escape(e["title"], quote=True) + '"></a>'
        identity = "[" + e["title"].replace("|", "&#124;") + "](" + detail + ")<br>" + html_code(e["shortIdentifier"]) + "<br>Authored preview label"
        loc, desc = e["locations"], e["sourceDescription"]
        gani = html_code(loc["ganiDirectory"] + "/") + "<br>" + html_code(posixpath.basename(loc["ganiVirtualPath"]))
        container = "DAT: " + html_code(loc["datArchive"]) + "<br>FPK: " + html_code(loc["containerVirtualPath"] or loc["recordedContainerLabel"]) + "<br>MTAR: " + html_code(loc["archiveVirtualPath"] or loc["archiveFile"]) + "<br>Historical source receipt"
        description = html.escape(desc["text"], quote=True).replace("|", "&#124;") if desc["text"] is not None else "Unavailable: no verified exact source match."
        if desc["credit"]:
            description += "<br>" + html.escape(desc["credit"], quote=True)
        credit = "Game: Konami / Kojima Productions<br>Labels: arsenal-pt / Codex"
        if any(c["role"] == "selected workbook discovery" for c in e["credits"]):
            credit += "<br>Discovery: KnochenGott (human supplied)"
        credit += "<br>[Per-entry provenance](" + detail + "#credits-and-evidence)"
        timing = str(e["rawFrameCount"]) + " raw<br>" + f'{e["previewDurationMilliseconds"]/1000:g}' + " s (chosen)<br>[Full data](" + detail + "#technical-data)"
        cells = [image, identity, html.escape(e["category"]["label"]), "<br>".join(html_code(x) for x in e["tags"]), gani, container, description, credit, timing]
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "Pages: " + " · ".join(nav), "", "[All data (JSON)](../catalogue.json) · [Spreadsheet data (CSV)](../catalogue.csv) · [Source review](../description-sources.md)", ""]
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
        "## Metadata columns", "",
        "Tables, JSON/CSV and detail pages separate **category**, **authored tags**, **virtual GANI directory/file**, **MTAR/container location**, **community source description** and **per-entry credits**. "
        "Existing title-based preview summaries are project-authored; missing external descriptions remain unavailable. "
        "The reviewed BossQuiet2_layers notes match none of the current 27 paths. Read [description sources and matching rules](description-sources.md), the [machine-readable source review](metadata-source-review.json) and [retained container provenance](container-provenance.json).", "",
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
        "python research/animation-library/build-library.py --check",
        "# Metadata changes only: preserve existing reviewed media",
        "python research/animation-library/build-library.py --metadata-only",
        "python research/animation-library/build-library.py --metadata-only --check", FENCE, "",
        "This reads existing reviewed GIFs, deterministically downscales their composited frames, retains loop and total "
        "display duration, and writes only library documentation and new thumbnails. The full-size GIFs and original "
        "metadata stay unchanged. New batches need explicit input registration/group labels in the builder. "
        "The --metadata-only option reuses hash-verified existing thumbnails and writes no media. "
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


def build(root, metadata_only=False):
    outputs, entries, identities = {}, [], set()
    review_bytes = (root / METADATA_REVIEW).read_bytes()
    description_review = json.loads(review_bytes)
    container_review_bytes = (root / CONTAINER_REVIEW).read_bytes()
    container_review = json.loads(container_review_bytes)
    cache = {}
    if metadata_only:
        cached_manifest = json.loads((root / THUMBS / "manifest.json").read_bytes())
        cache = {e["id"]: e for e in cached_manifest["entries"]}
        if len(cache) != len(cached_manifest["entries"]):
            raise ValueError("Duplicate cached thumbnail identity")
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
            thumb_path = THUMBS + "/" + identity + ".gif"
            if metadata_only:
                cached = cache[identity]
                assert cached["sourceFullGif"] == {"path": full_path, "sha256": sha(full), "bytes": len(full)}
                thumbnail = dict(cached["animatedThumbnail"])
                thumb = (root / thumbnail["path"]).read_bytes()
                assert thumbnail["path"] == thumb_path and sha(thumb) == thumbnail["sha256"]
                assert len(thumb) == thumbnail["bytes"]
                duration = thumbnail["durationMilliseconds"]
            else:
                thumb, source_frames, encoded_frames, duration = make_thumbnail(full)
                outputs[thumb_path] = thumb
                thumbnail = {"path": thumb_path, "sha256": sha(thumb),
                             "bytes": len(thumb), "width": 160, "height": Image.open(BytesIO(thumb)).height,
                             "sourceGifFrames": source_frames, "encodedFrames": encoded_frames,
                             "durationMilliseconds": duration, "loop": 0}
            assert duration == p["gifDurationMilliseconds"]
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
                    "animatedThumbnail": thumbnail,
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
            archive = next(a for a in source["archives"] if a["name"] == original["sourceArchive"])
            assert archive["mtarSha256"] == original["sourceMtarSha256"]
            enrich_metadata(record, archive, source, source_path, description_review, container_review)
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
        "metadataSourceReview": {"path": METADATA_REVIEW, "sha256": sha(review_bytes)},
        "metadataContainerProvenance": {"path": CONTAINER_REVIEW, "sha256": sha(container_review_bytes)},
        "metadataPolicy": "Authored categories/tags/preview summaries are separate from exact-match external descriptions and retained original records",
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
    outputs[LIB + "/catalogue.csv"] = render_csv(entries)
    outputs[LIB + "/README.md"] = render_readme(catalogue)
    for page in page_sets(catalogue):
        outputs[page["animated"]] = render_table_page(page)
        outputs[page["stills"]] = render_table_page(page, stills=True)
    if not metadata_only:
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
    parser.add_argument("--metadata-only", action="store_true",
                        help="Reuse hash-verified reviewed thumbnails; write/check documentation and catalogue only")
    args = parser.parse_args()
    if PILLOW_VERSION != "12.2.0":
        raise SystemExit("Use Pillow 12.2.0 to reproduce the reviewed encoding")
    outputs, catalogue = build(ROOT, metadata_only=args.metadata_only)
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
        "metadataOnly": args.metadata_only,
        "clips": catalogue["entryCount"],
        "generatedFiles": len(outputs),
        "animatedThumbnailBytes": sum(e["media"]["animatedThumbnail"]["bytes"]
                                     for e in catalogue["entries"]),
        "originalMediaChanged": False,
        "nativeProof": False,
    }))


if __name__ == "__main__":
    main()

