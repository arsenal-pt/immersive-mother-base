"""Offline platform patch contract tests. No live game root or installation.
Run with separately installed bsdiff4; --originals-root optionally checks real owned inputs.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--originals-root", type=Path)
parser.add_argument("--library-dir", type=Path)
args = parser.parse_args()
if args.library_dir:
    sys.path.insert(0, str(args.library_dir.resolve()))
import bsdiff4
spec = importlib.util.spec_from_file_location("platform_rebuild", ROOT / "platforms/command-v9/rebuild.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def sha(data):
    return hashlib.sha256(data).hexdigest()

class Contract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="imb-patch-contract-")
        self.root = Path(self.temp.name)
        self.stock = self.root / "stock"
        self.component = self.root / "component"
        self.stock.mkdir()
        self.component.mkdir()
        self.base = b"synthetic original " * 100
        self.target = self.base[:200] + b"authored change" + self.base[215:]
        patch = bsdiff4.diff(self.base, self.target)
        (self.stock / "source.fpk").write_bytes(self.base)
        (self.component / "synthetic.bsdiff").write_bytes(patch)
        self.manifest = {"schema": 1, "component": "synthetic", "patchFormat": "BSDIFF40",
                         "patchFile": "synthetic.bsdiff", "patchSha256": sha(patch), "patchBytes": len(patch),
                         "baseBundleSha256": sha(self.base), "targetBundleSha256": sha(self.target),
                         "sources": [{"path": "source.fpk", "bytes": len(self.base), "sha256": sha(self.base)}],
                         "targets": [{"path": "Assets/result.fpk", "bytes": len(self.target), "sha256": sha(self.target)}]}
        self.save()

    def save(self):
        (self.component / "manifest.json").write_text(json.dumps(self.manifest))

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_exact_new_staging_and_no_overwrite(self):
        out = self.root / "new"
        self.assertTrue(module.rebuild(self.stock, out, self.component)["written"])
        self.assertEqual((out / "Assets/result.fpk").read_bytes(), self.target)
        with self.assertRaises(ValueError):
            module.rebuild(self.stock, out, self.component)
        self.assertEqual((self.stock / "source.fpk").read_bytes(), self.base)

    def test_check_only_writes_nothing(self):
        out = self.root / "new"
        self.assertFalse(module.rebuild(self.stock, out, self.component, True)["written"])
        self.assertFalse(out.exists())

    def test_wrong_base_writes_nothing(self):
        (self.stock / "source.fpk").write_bytes(b"wrong")
        with self.assertRaises(ValueError):
            module.rebuild(self.stock, self.root / "new", self.component)
        self.assertFalse((self.root / "new").exists())

    def test_corrupt_patch_rejected(self):
        (self.component / "synthetic.bsdiff").write_bytes(b"wrong")
        with self.assertRaises(ValueError):
            module.rebuild(self.stock, self.root / "new", self.component)
        self.assertFalse((self.root / "new").exists())

    def test_target_checksum_and_path_escape_rejected(self):
        self.manifest["targets"][0]["sha256"] = "0" * 64
        self.save()
        with self.assertRaises(ValueError):
            module.rebuild(self.stock, self.root / "new", self.component)
        for path in ["../escape", "/absolute", "C:/drive", "a\\b"]:
            with self.assertRaises(ValueError):
                module.child(self.root.resolve(), path)

    def test_input_output_overlap_rejected(self):
        with self.assertRaises(ValueError):
            module.rebuild(self.stock, self.stock / "new", self.component)

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.originals_root:
        manifest, outputs = module.reconstruct(args.originals_root)
        print(json.dumps({"nativeAcceptance": False, "frozenTargetsByteExact": len(outputs),
                          "targetHashes": [sha(data) for _, data in outputs]}))
