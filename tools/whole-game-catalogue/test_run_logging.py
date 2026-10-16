"""CLI logging/usability tests; use tiny authored fixtures, never installed game data."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import time
import catalogue as m
import test_catalogue as fixtures

HERE = Path(__file__).resolve().parent
ROOT = os.environ.get("MGSV_CATALOGUE_TEST_ROOT")

class RunLoggingCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="run-log-", dir=ROOT)
        self.base = Path(self.temp.name)
        (self.base / "game").mkdir()
        self.runtime = self.base / "runtime"
        self.config = self.base / "config.json"
        self.config.write_text(json.dumps({"gameRoot": str(self.base / "game"),
            "toolRoot": str(self.base / "unused-tool"), "runtimeRoot": str(self.runtime),
            "exportRoot": str(self.base / "exports"), "reserveBytes": 1048576}),encoding="utf-8")
    def tearDown(self):
        if ROOT:
            assert self.base.resolve().is_relative_to(Path(ROOT).resolve())
        self.temp.cleanup()
    def cli(self,*args,input_text=None):
        return subprocess.run([sys.executable,str(HERE / "catalogue.py"),"--config",str(self.config),*args],
            input=input_text,text=True,capture_output=True,timeout=30)
    def latest(self):
        pointer=self.runtime / "logs/latest-run.json"
        self.assertTrue(pointer.is_file(),"Every CLI invocation must automatically persist a latest-run pointer.")
        value=json.loads(pointer.read_text(encoding="utf-8"))
        summary=self.runtime / "logs" / value["summary"]
        transcript=self.runtime / "logs" / value["transcript"]
        return json.loads(summary.read_text(encoding="utf-8")),transcript.read_text(encoding="utf-8"),value
    def prepare_archives(self,bad=False):
        tool=os.environ.get("MGSV_CATALOGUE_TEST_TOOL")
        if not tool:self.skipTest("set MGSV_CATALOGUE_TEST_TOOL for authored archive fixtures")
        config=json.loads(self.config.read_text())
        config.update(toolRoot=tool,maxContainerBytes=1048576,cacheBytes=4194304,ioBytesPerRun=134217728)
        self.config.write_text(json.dumps(config),encoding="utf-8")
        (self.base/"game/master").mkdir()
        inputs=self.base/"input/Assets/catalogue"
        inputs.mkdir(parents=True)
        for name,data in (("model.fpk",fixtures.fpk(bad=bad)),("model-copy.fpk",fixtures.fpk(bad=bad)),("audio.sbp",fixtures.sbp()),
                          ("texture.pftxs",fixtures.pftxs()),("unknown.zzunknown",b"authored")):
            (inputs/name).write_bytes(data)
        cat=m.Catalogue(config)
        try:
            cat.ensure_bridge()
            compiler=Path(os.environ.get("WINDIR","C:/Windows"))/"Microsoft.NET/Framework64/v4.0.30319/csc.exe"
            source=self.base/"fixtures.cs"
            source.write_text(fixtures.BUILDER,encoding="utf-8")
            writer=cat.exe.parent/"fixtures.exe"
            subprocess.run([str(compiler),"/nologo","/out:"+str(writer),"/reference:"+str(Path(tool)/"GzsTool.Core.dll"),str(source)],check=True,capture_output=True)
            subprocess.run([str(writer),str(self.base/"game"),str(self.base/"input")],check=True,capture_output=True)
        finally:cat.close()
    def test_menu_records_entered_count_and_compact_progress(self):
        self.prepare_archives()
        run=self.cli("menu",input_text="1\n")
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertNotIn('"container_coverage"',run.stdout,"Default menu must not dump detailed status JSON.")
        self.assertIn("Metadata only; no model previews generated",run.stdout)
        self.assertIn("Attempted 1",run.stdout)
        summary,transcript,pointer=self.latest()
        self.assertEqual(summary["entered_inputs"],[{"name":"nested_count","value":"1"}])
        self.assertIn("Selected nested count: 1",transcript)
        self.assertEqual(summary["attempted"],1)
        self.assertEqual(summary["succeeded"],1)
        self.assertEqual(summary["errors"],0)
        events=[json.loads(line) for line in (self.runtime/"logs"/pointer["events"]).read_text().splitlines()]
        self.assertIn("container_started",[x["event"] for x in events])
        self.assertIn("container_completed",[x["event"] for x in events])
        self.assertIsNotNone(summary["export_path"])

    def test_menu_needs_attention_remains_exit1_after_successful_export(self):
        self.prepare_archives(bad=True)
        run=self.cli("menu",input_text="1\n")
        self.assertEqual(run.returncode,1,"A successful export must not erase a container failure: "+run.stdout+run.stderr)
        summary,transcript,pointer=self.latest()
        self.assertEqual(summary["status"],"needs_attention")
        self.assertEqual(summary["attempted"],1)
        self.assertEqual(summary["succeeded"],0)
        self.assertEqual(summary["errors"],1)
        self.assertTrue(summary["reasons"])
        self.assertTrue(Path(summary["export_path"]).is_dir())
        self.assertIn("Needs attention:",run.stderr)
        self.assertIn("member_outside_container",transcript)

    def test_cancelled_menu_flushes_running_progress_and_never_claims_success(self):
        self.prepare_archives()
        process=subprocess.Popen([sys.executable,str(HERE/"catalogue.py"),"--config",str(self.config),"menu"],
                                 stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        pointer=None
        try:
            deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                latest=self.runtime/"logs/latest-run.json"
                if latest.exists():
                    pointer=json.loads(latest.read_text())
                    summary=json.loads((self.runtime/"logs"/pointer["summary"]).read_text())
                    events_file=self.runtime/"logs"/pointer["events"]
                    events=[json.loads(x) for x in events_file.read_text().splitlines()] if events_file.exists() else []
                    completed=[x for x in events if x["event"]=="container_completed" and x["detail"].get("phase")=="index"]
                    if len(completed)==2:
                        self.assertEqual(summary["status"],"running")
                        self.assertIsNone(summary["exit_code"])
                        self.assertTrue(summary["pid"])
                        break
                time.sleep(.05)
            else:self.fail("Menu did not flush running progress before waiting for input.")
            cancelled=self.cli("cancel")
            self.assertEqual(cancelled.returncode,0,cancelled.stderr)
            stdout,stderr=process.communicate("1\n",timeout=20)
            self.assertEqual(process.returncode,130,stdout+stderr)
            final=json.loads((self.runtime/"logs"/pointer["summary"]).read_text())
            self.assertEqual(final["status"],"cancelled")
            self.assertEqual(final["exit_code"],130)
            self.assertEqual(final["attempted"],0)
            self.assertIsNotNone(final["ended_at"])
            self.assertIn("Cancelled",(self.runtime/"logs"/pointer["transcript"]).read_text())
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
    def test_cli_failure_is_logged_and_invalid_protected_runtime_creates_no_logs(self):
        run=self.cli("index")
        self.assertEqual(run.returncode,2)
        summary,transcript,pointer=self.latest()
        self.assertEqual(summary["status"],"failed")
        self.assertEqual(summary["exit_code"],2)
        self.assertTrue(summary["reasons"])
        self.assertIn("FileNotFoundError",transcript)
        bad=json.loads(self.config.read_text())
        bad["runtimeRoot"]=str(self.base/"game/protected-runtime")
        self.config.write_text(json.dumps(bad))
        rejected=self.cli("status")
        self.assertEqual(rejected.returncode,2)
        self.assertFalse((self.base/"game/protected-runtime").exists())
    def test_exports_exclude_all_private_run_logs(self):
        self.prepare_archives()
        run=self.cli("menu",input_text="0\n")
        self.assertEqual(run.returncode,0,run.stderr)
        summary,transcript,pointer=self.latest()
        export=Path(summary["export_path"])
        self.assertEqual({p.name for p in export.iterdir()},
                         {"catalogue.sqlite","sources.csv","containers.csv","occurrences.csv","refs.csv","provenance.json","status.json","README.md"})
        for path in export.iterdir():
            if path.suffix in (".json",".md",".csv"):
                text=path.read_text(encoding="utf-8")
                self.assertNotIn(str(self.runtime),text)
                self.assertNotIn(pointer["run_id"],text)
        previous=pointer["run_id"]
        checked=self.cli("status")
        self.assertEqual(checked.returncode,0)
        latest,_,new_pointer=self.latest()
        self.assertNotEqual(previous,new_pointer["run_id"])
        self.assertTrue((self.runtime/"logs"/pointer["summary"]).exists())

    def test_menu_exposes_logs_at_start_and_records_outer_work_separately(self):
        self.prepare_archives()
        run=self.cli("menu",input_text="0\n")
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertLess(run.stdout.index("Transcript:"),run.stdout.index("Checking filesystem"))
        summary,transcript,pointer=self.latest()
        self.assertEqual(summary["phases"]["index"]["attempted"],2)
        self.assertEqual(summary["phases"]["index"]["succeeded"],2)
        self.assertEqual(summary["phase_results"]["index"]["indexed_this_run"],2)
        self.assertEqual(summary["attempt_scope"],"nested_containers")
        self.assertEqual(summary["attempted"],0)
        self.assertEqual(summary["succeeded"],0)
        self.assertEqual(summary["after"]["outer_indexed"],2)
        self.assertIn("Latest run:",run.stdout)

    def test_reporting_failure_cannot_relabel_committed_indexed_container(self):
        self.prepare_archives()
        cat=m.Catalogue(json.loads(self.config.read_text()))
        try:
            cat.census()
            cat.index()
            def report(event,detail):
                if event=="container_completed":raise RuntimeError("authored_log_write_failure")
            cat.progress_callback=report
            with self.assertRaisesRegex(RuntimeError,"authored_log_write_failure"):
                cat.expand(1)
            nested={row["state"]:row["containers"] for row in cat.status()["container_coverage"] if row["layer"]=="nested"}
            self.assertEqual(nested.get("indexed"),1)
            self.assertEqual(nested.get("deferred",0),0)
        finally:cat.close()

    def test_status_cli_saves_transcript_and_latest_summary_without_polluting_stdout(self):
        run=self.cli("status")
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(json.loads(run.stdout)["previews"],0)
        summary,transcript,pointer=self.latest()
        self.assertEqual(summary["command"],"status")
        self.assertEqual(summary["status"],"succeeded")
        self.assertEqual(summary["exit_code"],0)
        self.assertIn('"previews": 0',transcript)
        self.assertIsNotNone(summary["ended_at"])
        self.assertEqual(summary["before"]["nested_indexed"],0)
        self.assertEqual(summary["after"]["nested_indexed"],0)

if __name__=="__main__":unittest.main(verbosity=2)
