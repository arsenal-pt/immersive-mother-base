"""Regenerate the frozen delta from exact owned originals and exact edited packs.
GPL-3.0-only original helper. No game files, install, launch or automatic upload.
"""
import argparse
from pathlib import Path
import json
import bsdiff4
from rebuild import HERE, child, originals, sha

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--originals-root", type=Path, required=True)
    parser.add_argument("--edited-root", type=Path, required=True)
    parser.add_argument("--output-patch", type=Path, required=True)
    args = parser.parse_args()
    if args.output_patch.exists():
        raise ValueError("New output patch required")
    manifest = json.loads((HERE / "manifest.json").read_text())
    base = originals(args.originals_root, manifest)
    parts = []
    root = args.edited_root.resolve(strict=True)
    for entry in manifest["targets"]:
        data = child(root, entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise ValueError("Frozen edited target mismatch: " + entry["path"])
        parts.append(data)
    target = b"".join(parts)
    patch = bsdiff4.diff(base, target)
    if bsdiff4.patch(base, patch) != target or sha(patch) != manifest["patchSha256"]:
        raise ValueError("Delta reproduction mismatch")
    args.output_patch.parent.mkdir(parents=True, exist_ok=True)
    with args.output_patch.open("xb") as handle:
        handle.write(patch)
    print(json.dumps({"patchSha256": sha(patch), "bytes": len(patch), "installed": False}))

if __name__ == "__main__":
    main()
