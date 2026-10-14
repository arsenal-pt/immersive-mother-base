"""Rebuild frozen v9.1 packs from owned originals, into a NEW staging directory only.
Original helper: GPL-3.0-only. External bsdiff4 and underlying game assets keep their terms.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def child(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts or ":" in relative or "\\" in relative:
        raise ValueError("Invalid manifest path")
    result = (root / str(rel)).resolve()
    if not result.is_relative_to(root):
        raise ValueError("Path escapes selected root")
    return result

def originals(root, manifest):
    root = root.resolve(strict=True)
    parts = []
    for entry in manifest["sources"]:
        path = child(root, entry["path"])
        data = path.read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise ValueError("Original package mismatch: " + entry["path"])
        parts.append(data)
    bundle = b"".join(parts)
    if sha(bundle) != manifest["baseBundleSha256"]:
        raise ValueError("Original bundle mismatch")
    return bundle

def reconstruct(root, component=HERE):
    import bsdiff4
    manifest = json.loads((component / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != 1 or manifest.get("patchFormat") != "BSDIFF40":
        raise ValueError("Unsupported manifest")
    patch = child(component.resolve(), manifest["patchFile"]).read_bytes()
    if len(patch) != manifest["patchBytes"] or sha(patch) != manifest["patchSha256"]:
        raise ValueError("Patch checksum mismatch")
    base = originals(root, manifest)
    result = bsdiff4.patch(base, patch)
    if sha(result) != manifest["targetBundleSha256"]:
        raise ValueError("Reconstructed bundle mismatch")
    outputs = []
    offset = 0
    for entry in manifest["targets"]:
        data = result[offset:offset + entry["bytes"]]
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            raise ValueError("Reconstructed target mismatch: " + entry["path"])
        outputs.append((entry["path"], data))
        offset += entry["bytes"]
    if offset != len(result):
        raise ValueError("Unexpected trailing target data")
    return manifest, outputs

def rebuild(root, output, component=HERE, check_only=False):
    root = root.resolve(strict=True)
    output = output.resolve()
    if output.exists():
        raise ValueError("Output directory must be new; refusing to overwrite")
    if output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError("Separate input and output directories required")
    manifest, outputs = reconstruct(root, component)
    planned = [(child(output, name), data) for name, data in outputs]
    if check_only:
        return {"verified": len(planned), "version": manifest["component"], "written": False}
    output.mkdir(parents=True, exist_ok=False)
    for path, data in planned:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
    receipt = {"version": manifest["component"], "targets": manifest["targets"],
               "offlineByteExact": True, "installed": False, "nativeAcceptance": False}
    (output / "Rebuild-Receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return {"verified": len(planned), "version": manifest["component"], "written": True}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--originals-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(rebuild(args.originals_root, args.output_dir, check_only=args.check_only)))
    except (OSError, ValueError, ImportError) as error:
        parser.exit(1, "Could not rebuild: " + str(error) + "\n")
