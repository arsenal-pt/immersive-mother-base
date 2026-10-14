# SPDX-License-Identifier: GPL-3.0-only
"""Real filesystem transaction tests; all install roots are temporary fake games."""
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("imb_installer", HERE.parent / "installer/install.py")
im = importlib.util.module_from_spec(spec)
spec.loader.exec_module(im)


def pe(identity=b""):
    blob = bytearray(128)
    blob[:2] = b"MZ"
    struct.pack_into("<I", blob, 60, 64)
    blob[64:68] = b"PE\0\0"
    return bytes(blob) + identity


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="imb-installer-test-")
        self.root = Path(self.tmp.name)
        self.game = self.root / "MGS_TPP"
        self.game.mkdir()
        self.package = self.root / "package"
        self.package.mkdir()
        self.write(self.game / "mgsvtpp.exe", pe())
        self.write(self.game / "dinput8.dll", pe(b"IHHook r25"))
        self.write(self.game / "mod/modules/InfMenu.lua", b"-- external Infinite Heaven menu\n")
        self.write(self.game / "mod/modules/InfMenuDefs.lua", b"-- external definitions\n")
        self.write(self.game / "mod/third-party-settings.lua", b"do not modify settings")
        self.write(self.game / "mod/nlab/imb-life-save.lua", b"private runtime data")
        self.write(self.game / "00.dat", b"private game archive")
        self.make_package()
        self.base = self.inventory(self.game)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def inventory(self, root):
        return {str(p.relative_to(root)).replace("\\", "/"):p.read_bytes()
                for p in root.rglob("*") if p.is_file() and "imb-install-backups" not in p.parts}

    def make_package(self, version="0.1.0-alpha.1", marker="v1"):
        files = []
        for target in sorted(im.OWNED_TARGETS):
            data = ("-- authored fake payload " + marker + " " + target + "\n").encode("utf-8")
            self.write(self.package / ("core/GameDir/" + target), data)
            files.append({"source":"core/GameDir/" + target, "target":target,
                          "size":len(data), "sha256":im.digest(data)})
        self.manifest = {"schemaVersion":1, "product":"Immersive Mother Base", "version":version,
                         "license":"GPL-3.0-only", "nativeAcceptance":False,
                         "sourceTag":"v"+version, "sourceCommit":None, "files":files,
                         "supportedFeatures":["owned menu and regular-soldier logical needs"],
                         "unavailableFeatures":["native resources and gameplay acceptance"]}
        self.save_manifest()
        self.write(self.package / "VERSION", (version+"\n").encode())

    def save_manifest(self):
        self.write(self.package / "installer/package-manifest.json", im.json_bytes(self.manifest))

    def install(self, **kwargs):
        return im.install(self.game, self.package, process_checker=lambda:False, **kwargs)

    def uninstall(self, **kwargs):
        return im.uninstall(self.game, process_checker=lambda:False, **kwargs)

    def assert_baseline(self, baseline=None):
        self.assertEqual(self.inventory(self.game), baseline or self.base)

    def test_new_install_and_uninstall_keep_unrelated_files(self):
        receipt = self.install()
        self.assertEqual(im.load_receipt(self.game, receipt)["state"], "installed")
        self.assertEqual(len(im.load_receipt(self.game, receipt)["files"]), 20)
        self.uninstall()
        self.assert_baseline()
        self.assertTrue(receipt.exists())
        self.assertFalse((self.game / im.BACKUP_ROOT / "active.json").exists())

    def test_existing_files_including_empty_are_restored(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"earlier user implementation")
        self.write(self.game / "mod/nlab/NpcLifeCore.lua", b"")
        baseline = self.inventory(self.game)
        self.install()
        self.uninstall()
        self.assert_baseline(baseline)

    def test_missing_external_framework_refuses_before_targets(self):
        (self.game / "mod/modules/InfMenu.lua").unlink()
        baseline = self.inventory(self.game)
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline(baseline)
        self.assertFalse((self.game / im.BACKUP_ROOT).exists())

    def test_unrecognized_proxy_dll_is_not_accepted_as_ihhook(self):
        self.write(self.game / "dinput8.dll", pe(b"another loader"))
        baseline = self.inventory(self.game)
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline(baseline)

    def test_plugin_ihhook_alternative(self):
        self.write(self.game / "dinput8.dll", pe(b"external plugin loader"))
        self.write(self.game / "plugins/IHHook.asi", pe("IHHook".encode("utf-16le")))
        self.install()
        self.uninstall()

    def test_non_pe_game_rejected(self):
        self.write(self.game / "mgsvtpp.exe", b"not an executable")
        with self.assertRaises(im.InstallError): self.install()
        self.assertFalse((self.game / im.BACKUP_ROOT).exists())

    def test_game_running_refuses_before_backup_or_targets(self):
        with self.assertRaises(im.InstallError):
            im.install(self.game, self.package, process_checker=lambda:True)
        self.assert_baseline()
        self.assertFalse((self.game / im.BACKUP_ROOT).exists())

    def test_corrupt_package_refuses_before_targets(self):
        item = self.manifest["files"][0]
        self.write(self.package / item["source"], b"corrupt")
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline()
        self.assertFalse((self.game / im.BACKUP_ROOT).exists())

    def test_path_traversal_and_foreign_targets(self):
        original = dict(self.manifest["files"][0])
        for target in ("../outside.lua", "mod/modules/../InfMenu.lua", "mod/modules/InfMenu.lua", "C:/outside.lua", "mod\\modules\\NpcLife.lua"):
            with self.subTest(target=target):
                self.manifest["files"][0] = {**original, "target":target}
                self.save_manifest()
                with self.assertRaises(im.InstallError): self.install()
                self.assert_baseline()
        self.manifest["files"][0] = {**original, "source":"../outside.lua"}
        self.save_manifest()
        with self.assertRaises(im.InstallError): self.install()

    def test_duplicate_manifest_targets(self):
        self.manifest["files"][1] = dict(self.manifest["files"][0])
        self.save_manifest()
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline()

    def test_version_mismatch_and_false_native_claim(self):
        self.write(self.package / "VERSION", b"99.0.0\n")
        with self.assertRaises(im.InstallError): self.install()
        self.write(self.package / "VERSION", b"0.1.0-alpha.1\n")
        self.manifest["nativeAcceptance"] = True
        self.save_manifest()
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline()

    def test_repeat_install_keeps_first_original_provenance(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original authored elsewhere")
        baseline = self.inventory(self.game)
        first = self.install()
        first_snapshot = first.read_bytes()
        second = self.install()
        self.assertNotEqual(first, second)
        self.assertEqual(first.read_bytes(), first_snapshot)
        self.make_package(version="0.1.1-alpha.1", marker="v2")
        third = self.install()
        data = im.load_receipt(self.game, third)
        item = next(e for e in data["files"] if e["target"] == "mod/modules/NpcLife.lua")
        self.assertEqual(item["originalSha256"], im.digest(b"original authored elsewhere"))
        self.assertEqual(data["priorActive"]["receipt"], str(second.relative_to(self.game)).replace("\\", "/"))
        self.uninstall()
        self.assert_baseline(baseline)

    def test_modified_installed_file_refuses_uninstall_and_reinstall(self):
        self.install()
        self.write(self.game / "mod/modules/NpcLife.lua", b"new user changes")
        changed = self.inventory(self.game)
        with self.assertRaises(im.InstallError): self.uninstall()
        self.assert_baseline(changed)
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline(changed)

    def test_corrupted_backup_refuses_all_uninstall_writes(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        receipt = self.install()
        installed = self.inventory(self.game)
        self.write(receipt.parent / "original/mod/modules/NpcLife.lua", b"corrupt original")
        with self.assertRaises(im.InstallError): self.uninstall()
        self.assert_baseline(installed)

    def test_partial_install_failure_rolls_back_every_target(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        baseline = self.inventory(self.game)
        count = 0
        def fail_on_third(path, data):
            nonlocal count
            count += 1
            if count == 3: raise OSError("injected disk error")
            im.atomic_write(path, data)
        with self.assertRaisesRegex(im.InstallError, "planned targets restored"):
            self.install(write_file=fail_on_third)
        self.assert_baseline(baseline)
        receipts = list((self.game / im.BACKUP_ROOT).rglob("install-receipt.json"))
        self.assertEqual(im.load_receipt(self.game, receipts[0])["state"], "rolled_back")

    def test_partial_uninstall_failure_restores_installed_state(self):
        for target in ("mod/modules/ImmersiveMotherBase.lua", "mod/modules/NlabActionRecorder.lua"):
            self.write(self.game / target, b"old user file " + target.encode())
        receipt = self.install()
        installed = self.inventory(self.game)
        count = 0
        def fail_on_second(path, data):
            nonlocal count
            count += 1
            if count == 2: raise OSError("injected restore disk error")
            im.atomic_write(path, data)
        with self.assertRaisesRegex(im.InstallError, "installed files restored"):
            self.uninstall(write_file=fail_on_second)
        self.assert_baseline(installed)
        self.assertEqual(im.load_receipt(self.game, receipt)["state"], "installed")

    def test_game_started_mid_install_requires_later_safe_recovery(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        baseline = self.inventory(self.game)
        calls = 0
        def starts_running():
            nonlocal calls
            calls += 1
            return calls >= 5
        with self.assertRaisesRegex(im.InstallError, "restore --receipt"):
            im.install(self.game, self.package, process_checker=starts_running)
        receipt = next((self.game / im.BACKUP_ROOT).rglob("install-receipt.json"))
        self.assertEqual(im.load_receipt(self.game, receipt)["state"], "recovery_required")
        im.recover(self.game, receipt, process_checker=lambda:False)
        self.assert_baseline(baseline)
        self.assertEqual(im.load_receipt(self.game, receipt)["state"], "rolled_back")

    def test_interrupted_uninstall_recovery_restores_installed_files(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        receipt_path = self.install()
        installed = self.inventory(self.game)
        receipt = im.load_receipt(self.game, receipt_path)
        for e in receipt["files"]:
            self.write(receipt_path.parent / ("uninstall-before/" + e["target"]), (self.game / e["target"]).read_bytes())
        receipt["state"] = "uninstalling"
        self.write(receipt_path, im.json_bytes(receipt))
        entry = next(e for e in receipt["files"] if e["originalSha256"] is None)
        (self.game / entry["target"]).unlink()
        im.recover(self.game, receipt_path, process_checker=lambda:False)
        self.assert_baseline(installed)
        self.assertEqual(im.load_receipt(self.game, receipt_path)["state"], "installed")

    def test_receipt_cannot_name_foreign_file(self):
        receipt_path = self.install()
        receipt = im.load_receipt(self.game, receipt_path)
        receipt["files"][0]["target"] = "mod/modules/InfMenu.lua"
        self.write(receipt_path, im.json_bytes(receipt))
        installed = self.inventory(self.game)
        with self.assertRaises(im.InstallError): self.uninstall()
        self.assert_baseline(installed)

    def test_older_receipt_cannot_uninstall_newer_install(self):
        first = self.install()
        self.install()
        with self.assertRaises(im.InstallError): self.uninstall(receipt_path=first)

    def test_uninstall_does_not_require_remaining_framework(self):
        self.install()
        (self.game / "dinput8.dll").unlink()
        (self.game / "mod/modules/InfMenu.lua").unlink()
        self.uninstall()
        for target in im.OWNED_TARGETS: self.assertFalse((self.game / target).exists())

    def test_source_symlink_refused(self):
        item = self.manifest["files"][0]
        path = self.package / item["source"]
        data = path.read_bytes()
        outside = self.root / "outside.lua"
        outside.write_bytes(data)
        path.unlink()
        try: path.symlink_to(outside)
        except OSError as exc: self.skipTest("OS does not permit symlink creation: " + str(exc))
        with self.assertRaises(im.InstallError): self.install()
        self.assert_baseline()

    def test_native_process_enumerator_is_read_only(self):
        if os.name != "nt": self.skipTest("Windows process API")
        self.assertIsInstance(im.game_running(), bool)
        self.assert_baseline()

    def test_concurrent_os_transaction_lock_refuses_second_process(self):
        script = self.root / "hold_lock.py"
        ready = self.root / "lock-ready"
        script.write_text('import importlib.util, pathlib, time\n'
            + 's=importlib.util.spec_from_file_location("im", '+repr(str(HERE.parent / "installer/install.py"))+')\n'
            + 'im=importlib.util.module_from_spec(s);s.loader.exec_module(im)\n'
            + 'with im.transaction_lock(pathlib.Path('+repr(str(self.game))+')):\n'
            + ' pathlib.Path('+repr(str(ready))+').write_text("ready")\n time.sleep(20)\n', encoding="utf-8")
        child = subprocess.Popen([sys.executable, "-B", str(script)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            import time
            deadline=time.monotonic()+5
            while not ready.exists() and time.monotonic()<deadline: time.sleep(0.02)
            self.assertTrue(ready.exists())
            with self.assertRaisesRegex(im.InstallError, "Another installer"):
                self.install()
            self.assert_baseline()
        finally:
            child.terminate()
            child.communicate(timeout=5)


    def test_game_junction_refused_with_real_windows_reparse_point(self):
        if os.name != "nt": self.skipTest("Windows junction test")
        original = self.game / "mod/nlab"
        moved = self.root / "real-nlab"
        original.rename(moved)
        result = subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(original), str(moved)], capture_output=True)
        if result.returncode != 0:
            moved.rename(original)
            self.skipTest("Windows junction creation unavailable")
        try:
            with self.assertRaisesRegex(im.InstallError, "reparse points"):
                self.install()
            self.assertEqual((moved / "imb-life-save.lua").read_bytes(), b"private runtime data")
        finally:
            self.assertTrue(original.absolute().is_relative_to(self.root.absolute()))
            original.rmdir()  # Removes only this junction, never its target.
            moved.rename(original)

    def test_install_commit_window_receipt_recovers_previous_install(self):
        first = self.install()
        baseline = self.inventory(self.game)
        self.make_package(version="0.1.1-alpha.1", marker="v2")
        second = self.install()
        journal = im.load_receipt(self.game, second)
        journal["state"] = "installing"
        self.write(second, im.json_bytes(journal))
        im.recover(self.game, second, process_checker=lambda:False)
        self.assert_baseline(baseline)
        active, _, _ = im.active_receipt(self.game)
        self.assertEqual(active, first)

    def test_uninstall_commit_window_with_absent_pointer_recovers(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        receipt = self.install()
        installed = self.inventory(self.game)
        self.uninstall()
        journal = im.load_receipt(self.game, receipt)
        journal["state"] = "uninstalling"
        self.write(receipt, im.json_bytes(journal))
        im.recover(self.game, receipt, process_checker=lambda:False)
        self.assert_baseline(installed)
        active, _, _ = im.active_receipt(self.game)
        self.assertEqual(active, receipt)

    def test_recovery_preserves_external_edits_instead_of_blind_rollback(self):
        edited = []
        def external_change_then_fail(path, data):
            edited.append(path)
            im.atomic_write(path, b"external user modification during install")
            raise OSError("injected external interference")
        with self.assertRaisesRegex(im.InstallError, "Changed files were preserved"):
            self.install(write_file=external_change_then_fail)
        self.assertEqual(edited[0].read_bytes(), b"external user modification during install")
        receipt = next((self.game / im.BACKUP_ROOT).rglob("install-receipt.json"))
        self.assertEqual(im.load_receipt(self.game, receipt)["state"], "recovery_required")
        with self.assertRaises(im.InstallError):
            im.recover(self.game, receipt, process_checker=lambda:False)
        self.assertEqual(edited[0].read_bytes(), b"external user modification during install")

    def test_repeated_install_rejects_corrupted_earliest_original(self):
        self.write(self.game / "mod/modules/NpcLife.lua", b"original user content")
        receipt = self.install()
        installed = self.inventory(self.game)
        self.write(receipt.parent / "original/mod/modules/NpcLife.lua", b"corrupt original")
        with self.assertRaisesRegex(im.InstallError, "Backup is corrupted"):
            self.install()
        self.assert_baseline(installed)


    def test_legacy_private_ih_adapter_refuses_before_any_writes(self):
        legacy = self.game / "mod/modules/NpcIHStaff.lua"
        self.write(legacy, b"-- legacy private adoption provider")
        self.write(self.game / "mod/modules/NpcLife.lua", b"earlier user implementation")
        baseline = self.inventory(self.game)
        with self.assertRaisesRegex(im.InstallError, "private IH staff adoption adapter"):
            self.install()
        self.assertEqual(self.inventory(self.game), baseline)
        self.assertFalse((self.game / im.BACKUP_ROOT).exists())
        self.assertEqual(legacy.read_bytes(), b"-- legacy private adoption provider")

    def test_original_ih_modules_do_not_conflict_with_clean_install(self):
        self.write(self.game / "mod/modules/InfFova.lua", b"-- original IH appearance module")
        self.write(self.game / "mod/modules/InfHostage.lua", b"-- original IH NPC module")
        baseline = self.inventory(self.game)
        self.install()
        self.uninstall()
        self.assertEqual(self.inventory(self.game), baseline)

if __name__ == "__main__":
    unittest.main(verbosity=2)