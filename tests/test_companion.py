"""Offline HTTP/IPC regression; only a temporary mod root and ephemeral ports."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
COMPANION = ROOT / "companion"

class Routes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="imb-companion-test-")
        cls.mod = Path(cls.temp.name) / "mod"
        cls.mod.mkdir()
        cls.child = None
        cls.start(sys.executable)

    @classmethod
    def start(cls, game):
        if cls.child:
            cls.child.terminate()
            cls.child.wait(timeout=10)
            cls.child.stdout.close()
            cls.child.stderr.close()
        cls.child = subprocess.Popen(
            [sys.executable, "-B", str(COMPANION / "server.py"), "--mod-root", str(cls.mod),
             "--game-exe", str(game), "--port", "0"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        line = cls.child.stdout.readline()
        try:
            cls.url = json.loads(line)["url"]
            cls.port = int(cls.url.rsplit(":", 1)[1])
            assert cls.port != 8785
        except Exception:
            cls.child.terminate()
            cls.child.wait(timeout=10)
            raise AssertionError("Child server startup failed: " + line + cls.child.stderr.read())

    @classmethod
    def tearDownClass(cls):
        if cls.child:
            cls.child.terminate()
            cls.child.wait(timeout=10)
            cls.child.stdout.close()
            cls.child.stderr.close()
        cls.temp.cleanup()

    def setUp(self):
        self.life = {"realTime": time.time(), "nativeProfile": True, "mission": 30050,
                     "actors": [{"id": 1, "name": "fixture_actor", "label": "Fixture label", "needs": {}}],
                     "lastCommand": None, "cqcTraining": {"ready": True, "scheduleReady": False}}
        self.staff = {"schema": 1, "ready": True, "mission": 30050, "managedCount": 0,
                      "free": 10, "loaded": 10, "activeCount": 0, "lastCommand": None}
        self.publish()
        (self.mod / "nlab_staff_control_status.json").write_text(json.dumps(self.staff), encoding="utf-8")
        for name in ("nlab_life_command.txt", "nlab_staff_command.txt", "nlab_base_map.json"):
            (self.mod / name).unlink(missing_ok=True)

    def publish(self):
        self.life["realTime"] = time.time()
        (self.mod / "nlab_life_status.json").write_text(json.dumps(self.life), encoding="utf-8")

    def request(self, path, payload=None, origin=None, raw=None):
        headers = {"Content-Type": "application/json"}
        if origin is not None:
            headers["Origin"] = origin
        data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
        req = urllib.request.Request(self.url + path, data=data, headers=headers)
        try:
            response = urllib.request.urlopen(req, timeout=3)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            content = response.read()
            try:
                value = json.loads(content)
            except ValueError:
                value = content.decode()
            return response.status, value

    def test_01_portable_feed_and_no_catalogues(self):
        code, status = self.request("/status")
        self.assertEqual(code, 200)
        self.assertTrue(status["runtime"]["ready"])
        self.assertEqual(status["actors"][0]["label"], "Fixture label")
        self.assertIn("lookup disabled", status["nameResolution"]["status"])
        self.assertEqual(self.request("/layout")[0], 503)
        self.assertEqual(self.request("/base-map-geometry")[0], 503)
        self.assertEqual(self.request("/base-map-state")[0], 503)
        self.assertFalse((self.mod / "nlab/native-staff-names.lua").exists())
        self.assertFalse((COMPANION / "native-staff-name-cache.json").exists())

    def test_02_extra_adapter_routes_and_controls_absent(self):
        for path in ("/ih-staff-panel.js", "/ih-staff-status", "/animations", "/native-animations", "/base-layout"):
            self.assertEqual(self.request(path)[0], 404)
        self.assertEqual(self.request("/ih-staff-command", {"action": "enable", "role": ""})[0], 403)
        html = self.request("/")[1]
        for text in ("IHStaff", "ihstaff", "inspection", "/animations"):
            self.assertNotIn(text, html)
        self.assertNotIn("ih_staff", (COMPANION / "commands.py").read_text())

    def test_03_atomic_life_command_and_pending_ack(self):
        code, value = self.request("/command", {"command": "muster"}, origin=self.url)
        self.assertEqual(code, 202)
        words = (self.mod / "nlab_life_command.txt").read_text().split()
        self.assertEqual(words, [value["id"], "muster"])
        self.assertEqual(self.request("/command", {"command": "gather"})[0], 409)
        self.life["lastCommand"] = value["id"]
        self.publish()
        self.assertEqual(self.request("/command", {"command": "gather"}, origin="http://localhost:" + str(self.port))[0], 202)
        self.assertEqual(list(self.mod.glob("*.tmp")), [])

    def test_04_origin_and_validation_never_write(self):
        self.assertEqual(self.request("/command", {"command": "muster"}, origin="https://example.invalid")[0], 403)
        self.assertEqual(self.request("/command", {"command": "muster"}, origin="http://127.0.0.1:8785")[0], 403)
        self.assertEqual(self.request("/command", {"command": "ih_staff_enable"})[0], 400)
        self.assertEqual(self.request("/command", {"command": "muster", "extra": True})[0], 400)
        self.assertEqual(self.request("/command", raw=b"x" * 512)[0], 400)
        self.assertFalse((self.mod / "nlab_life_command.txt").exists())

    def test_05_stale_feed_and_partial_replacement(self):
        self.assertEqual(self.request("/status")[0], 200)
        path = self.mod / "nlab_life_status.json"
        old = time.time() - 30
        os.utime(path, (old, old))
        self.assertEqual(self.request("/command", {"command": "muster"})[0], 409)
        path.write_text("{", encoding="utf-8")
        code, status = self.request("/status")
        self.assertEqual(code, 200)
        self.assertGreater(status["feedAgeSeconds"], 25)
        self.assertFalse(status["runtime"]["ready"])
        self.assertFalse((self.mod / "nlab_life_command.txt").exists())

    def test_06_staff_mailbox_and_limits(self):
        code, value = self.request("/staff-command", {"action": "add", "count": 1})
        self.assertEqual(code, 202)
        self.assertEqual((self.mod / "nlab_staff_command.txt").read_text().split(), [value["id"], "add", "1"])
        self.assertEqual(self.request("/staff-command", {"action": "clear", "count": 0})[0], 409)
        for action, count in (("add", 0), ("count", 11), ("clear", 1), ("remove", True)):
            self.assertEqual(self.request("/staff-command", {"action": action, "count": count})[0], 400)
        self.assertEqual(list(self.mod.glob("*.tmp")), [])

    def test_07_training_native_gates(self):
        self.assertEqual(self.request("/command", {"command": "cqc_auto"})[0], 409)
        self.life["cqcTraining"]["ready"] = False
        self.publish()
        self.assertEqual(self.request("/command", {"command": "cqc"})[0], 409)
        self.assertFalse((self.mod / "nlab_life_command.txt").exists())

    def test_08_wrong_mission_and_paused(self):
        self.life["mission"] = 40050
        self.publish()
        self.assertEqual(self.request("/command", {"command": "muster"})[0], 409)
        self.life["mission"], self.life["paused"] = 30050, True
        self.publish()
        self.assertEqual(self.request("/staff-command", {"action": "add", "count": 1})[0], 409)

    def test_09_closed_exact_configured_process(self):
        self.start(self.mod.parent / "closed-game.exe")
        try:
            self.assertFalse(self.request("/status")[1]["runtime"]["ready"])
            self.assertEqual(self.request("/command", {"command": "muster"})[0], 409)
            self.assertEqual(self.request("/staff-command", {"action": "add", "count": 1})[0], 409)
            self.assertFalse((self.mod / "nlab_life_command.txt").exists())
            self.assertFalse((self.mod / "nlab_staff_command.txt").exists())
        finally:
            self.start(sys.executable)

    def test_10_legacy_adapter_filter_and_reservation(self):
        self.life["actors"].append({"id": 2, "label": "Excluded fixture", "staffSource": "Infinite Heaven dependency"})
        self.life["actors"].append({"id": 3, "label": "Excluded fixture", "presenceSource": "existing IH actor; no duplicate spawned"})
        self.life["ihStaff"] = {"ready": True}
        self.life["assemblyReservation"] = {"owner": "temporary fixture"}
        self.publish()
        code, value = self.request("/status")
        self.assertEqual(code, 200)
        self.assertEqual(len(value["actors"]), 1)
        self.assertNotIn("ihStaff", value)
        self.assertEqual(self.request("/command", {"command": "muster"})[0], 409)
        self.assertFalse((self.mod / "nlab_life_command.txt").exists())

    def test_11_nonadvancing_fresh_file(self):
        self.assertTrue(self.request("/status")[1]["runtime"]["ready"])
        time.sleep(5.1)
        path = self.mod / "nlab_life_status.json"
        os.utime(path, None)
        self.assertEqual(self.request("/command", {"command": "muster"})[0], 409)
        self.assertFalse((self.mod / "nlab_life_command.txt").exists())

    def test_12_optional_names_missing_owned_data(self):
        sys.path.insert(0, str(COMPANION))
        from NativeNameResolver import NameService, validate_native_signatures
        service = NameService(sys.executable, self.mod / "absent", enabled=True)
        value = service.enrich({"actors": [{"name": "mb_staff_1234", "label": "Feed label"}]})
        self.assertEqual(value["actors"][0]["label"], "Feed label")
        self.assertIn("catalogue unavailable", value["nameResolution"]["status"])
        class UnsupportedReader:
            def read(self, address, size):
                return b"unsupported"
        with self.assertRaises(ValueError):
            validate_native_signatures(UnsupportedReader())
        self.assertFalse((self.mod / "nlab/native-staff-names.lua").exists())

    def test_13_config_loopback_and_explicit_paths(self):
        command = [sys.executable, "-B", str(COMPANION / "server.py")]
        missing = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        config = self.mod.parent / "test-config.json"
        config.write_text(json.dumps({"host": "0.0.0.0", "mod_root": "mod", "game_exe": sys.executable}), encoding="utf-8")
        rejected = subprocess.run(command + ["--config", str(config)], capture_output=True, text=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("loopback", rejected.stderr)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Routes)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"schema": 1, "date": "2026-10-14", "scope": "actual child-server HTTP and atomic IPC with temporary fixtures",
              "testsRun": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "passed": result.wasSuccessful(), "liveGameAccess": False, "liveModAccess": False,
              "port8785Used": False, "nativeGameplayProved": False,
              "childCleanup": "exact Popen children terminated and waited; temporary directory removed"}
    (Path(__file__).parent / "OFFLINE-TEST-REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    sys.exit(not result.wasSuccessful())
