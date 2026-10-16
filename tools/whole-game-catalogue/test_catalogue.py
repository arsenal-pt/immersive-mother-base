"""Tiny authored format fixtures; never reads game payloads."""
import json
import os
from pathlib import Path
import sqlite3
import struct
import subprocess
import tempfile
import unittest
import threading
import time
from unittest.mock import patch
import hashlib
import catalogue as m

TOOL = os.environ.get("MGSV_CATALOGUE_TEST_TOOL")
ROOT = os.environ.get("MGSV_CATALOGUE_TEST_ROOT")
BUILDER = r"""
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using GzsTool.Core.Qar;
using GzsTool.Core.Common;
class Fixtures {
 static void Main(string[] args) {
   if(args.Length>2){Thread.Sleep(30000);return;}
   string root=args[0];var q=new QarFile {Flags=0x3000e0U,Entries=new List<QarEntry>()};
   foreach(string n in new[]{"model.fpk","model-copy.fpk","audio.sbp","texture.pftxs","unknown.zzunknown"})
     q.Entries.Add(new QarEntry {FilePath="/Assets/catalogue/"+n});
   using(var output=File.Create(Path.Combine(root,"master","test.dat")))
     q.Write(output,new FileSystemDirectory(args[1]));
   File.WriteAllBytes(Path.Combine(args[1],"Assets","catalogue","final.txt"),new byte[131072]);
   var compressed=new QarFile {Flags=0x3000e0U,Entries=new List<QarEntry>{new QarEntry{FilePath="/Assets/catalogue/final.txt",Compressed=true}}};
   using(var output=File.Create(Path.Combine(root,"master","z-final.dat")))
     compressed.Write(output,new FileSystemDirectory(args[1]));
 }
}
"""

def fpk(payload=b"authored-model", bad=False):
    name = b"/Assets/catalogue/model.fmdl"
    ref = b"/Assets/catalogue/dependency.fpk"
    name_offset = 48 + 48 + 16
    ref_offset = name_offset + len(name) + 1
    data_offset = (ref_offset + len(ref) + 1 + 15) // 16 * 16
    size = data_offset + len(payload)
    header = b"foxfpk win" + struct.pack("<I", size) + bytes(18) + struct.pack("<IIII",2,1,1,0)
    entry = struct.pack("<IIIIIIII",size+1 if bad else data_offset,0,len(payload),0,name_offset,0,len(name),0) + hashlib.md5(name).digest()
    reference = struct.pack("<IIII",ref_offset,0,len(ref),0)
    table = header + entry + reference + name + b"\0" + ref + b"\0"
    return table + bytes(data_offset-len(table)) + payload

def sbp():
    return b"SBPL" + struct.pack("<BHB",1,20,0) + b"bnk\0" + struct.pack("<Ii",32,4) + bytes(12) + b"TEST"

def pftxs(bad=False):
    block = struct.pack("<IIQIIII",0x58455446,52,0,1,0,0,0) + struct.pack("<Qii",0,999 if bad else 48,4) + b"TEST"
    return struct.pack("<IIIIIIII",0x58544650,0x40000000,16,1,0x4c584554,16+len(block),1,0) + block

@unittest.skipUnless(TOOL and ROOT, "set MGSV_CATALOGUE_TEST_TOOL and MGSV_CATALOGUE_TEST_ROOT")
class Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="fixtures-",dir=ROOT)
        cls.base = Path(cls.temp.name)
        cls.game = cls.base / "game"
        (cls.game / "master").mkdir(parents=True)
        inp = cls.base / "input/Assets/catalogue"
        inp.mkdir(parents=True)
        (inp / "model.fpk").write_bytes(fpk())
        (inp / "model-copy.fpk").write_bytes(fpk())
        (inp / "audio.sbp").write_bytes(sbp())
        (inp / "texture.pftxs").write_bytes(pftxs())
        (inp / "unknown.zzunknown").write_bytes(b"authored")
        cls.config = {"gameRoot": str(cls.game), "toolRoot": TOOL, "runtimeRoot": str(cls.base / "runtime"),
                      "exportRoot": str(cls.base / "exports"), "reserveBytes":m.MIB,
                      "maxContainerBytes":m.MIB, "cacheBytes":4*m.MIB,"ioBytesPerRun":128*m.MIB}
        cls.cat=m.Catalogue(cls.config)
        cls.cat.ensure_bridge()
        build=cls.cat.exe.parent
        src=cls.base/"builder.cs"
        src.write_text(BUILDER)
        compiler=Path(os.environ.get("WINDIR","C:/Windows"))/"Microsoft.NET/Framework64/v4.0.30319/csc.exe"
        exe=build/"fixture_builder.exe"
        subprocess.run([str(compiler),"/nologo","/out:"+str(exe),"/reference:"+str(Path(TOOL)/"GzsTool.Core.dll"),str(src)],check=True,capture_output=True)
        subprocess.run([str(exe),str(cls.game),str(cls.base/"input")],check=True,capture_output=True)
        cls.census=cls.cat.census()
        cls.index=cls.cat.index()
    @classmethod
    def tearDownClass(cls):
        cls.cat.close()
        assert cls.base.resolve().is_relative_to(Path(ROOT).resolve())
        cls.temp.cleanup()
    def test_01_outer_api_zero_decode_and_null_content_hashes(self):
        self.assertEqual(self.index["payload_decodes"],0)
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM occurrences").fetchone()[0],6)
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM occurrences WHERE content_sha256 IS NOT NULL").fetchone()[0],0)
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM containers WHERE depth=1").fetchone()[0],4)
    def test_01b_compressed_final_member_uses_stored_extent(self):
        row=self.cat.db.execute("SELECT o.*,s.bytes FROM occurrences o JOIN containers c ON c.id=o.container_id JOIN sources s ON s.id=c.source_id WHERE s.relative_path='master/z-final.dat'").fetchone()
        self.assertLess(row["declared_size"],row["bytes"])
        self.assertGreater(row["compressed_size"],row["bytes"])
        sizes=self.cat.db.execute("SELECT * FROM member_sizes WHERE id=?",(row["id"],)).fetchone()
        self.assertEqual(sizes["stored_size"],row["declared_size"])
        self.assertEqual(sizes["declared_decoded_size"],131072)
    def test_02_bounded_nested_and_restart_cache(self):
        child=self.cat.db.execute("SELECT * FROM containers WHERE kind='fpk' AND depth=1 ORDER BY name").fetchone()
        result=self.cat.expand(1,child["id"])
        self.assertEqual(result["indexed"],1)
        self.assertEqual(result["payload_decodes"],1)
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM refs").fetchone()[0],1)
        current=self.cat.db.execute("SELECT * FROM containers WHERE id=?",(child["id"],)).fetchone()
        occurrence=self.cat.db.execute("SELECT * FROM occurrences WHERE id=?",(current["parent_occurrence"],)).fetchone()
        self.assertEqual(occurrence["content_sha256"],current["content_sha256"])
        self.assertEqual(occurrence["actual_size"],Path(current["input_path"]).stat().st_size)
        member=self.cat.db.execute("SELECT * FROM occurrences WHERE container_id=?",(child["id"],)).fetchone()
        self.assertEqual(member["name_origin"],"embedded")
        self.assertTrue(member["resolved"])
        other=m.Catalogue(self.config)
        try:
            repeated=other.expand(1,child["id"])
            self.assertEqual(repeated["attempts"],0)
            self.assertEqual(repeated["payload_decodes"],0)
            self.assertTrue(repeated["cache_hit"])
        finally: other.close()
    def test_02b_identical_content_preserves_occurrence_chains(self):
        first=self.cat.db.execute("SELECT * FROM containers WHERE kind='fpk' AND depth=1 AND state='indexed'").fetchone()
        second=self.cat.db.execute("SELECT * FROM containers WHERE kind='fpk' AND depth=1 AND state='pending'").fetchone()
        before=self.cat.processes
        result=self.cat.expand(1,second["id"])
        self.assertEqual(result["indexed"],1)
        # Only the outer selected member is decoded. Its identical FPK table is reused.
        self.assertEqual(self.cat.processes-before,1)
        current=self.cat.db.execute("SELECT * FROM containers WHERE id=?",(second["id"],)).fetchone()
        self.assertEqual(first["content_sha256"],current["content_sha256"])
        self.assertNotEqual(first["parent_occurrence"],current["parent_occurrence"])
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM occurrences WHERE container_id IN (?,?)",(first["id"],second["id"])).fetchone()[0],2)
    def test_02c_source_checked_before_cached_content_acceptance(self):
        row=self.cat.db.execute("SELECT * FROM containers WHERE kind='fpk' AND depth=1 AND state='indexed' ORDER BY name").fetchone()
        source=self.cat.db.execute("SELECT * FROM sources WHERE id=?",(row["source_id"],)).fetchone()
        path=self.game/source["relative_path"]
        stamp=path.stat()
        os.utime(path,ns=(stamp.st_atime_ns,stamp.st_mtime_ns+1000000000))
        try:
            with self.assertRaisesRegex(m.CatalogueError,"source_snapshot_changed"):
                self.cat.prepare_container(row)
            with self.assertRaisesRegex(m.CatalogueError,"source_snapshot_changed"):
                self.cat.index_one(row)
        finally:os.utime(path,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
    def test_02d_stale_root_index_preserves_verified_child_hashes(self):
        root=self.cat.db.execute("SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id WHERE s.relative_path='master/test.dat' AND c.depth=0").fetchone()
        before=[tuple(x) for x in self.cat.db.execute("SELECT id,content_sha256,actual_size FROM occurrences WHERE container_id=? AND content_sha256 IS NOT NULL ORDER BY id",(root["id"],))]
        self.assertEqual(len(before),2)
        Path(root["index_path"]).write_text("broken index",encoding="utf-8")
        decodes=self.cat.decoded
        self.cat.index()
        after=[tuple(x) for x in self.cat.db.execute("SELECT id,content_sha256,actual_size FROM occurrences WHERE container_id=? AND content_sha256 IS NOT NULL ORDER BY id",(root["id"],))]
        self.assertEqual(before,after)
        self.assertEqual(decodes,self.cat.decoded)
    def test_03_sbp_pftxs_metadata(self):
        for kind in ("sbp","pftxs"):
            child=self.cat.db.execute("SELECT * FROM containers WHERE kind=? AND depth=1",(kind,)).fetchone()
            self.assertEqual(self.cat.expand(1,child["id"])["indexed"],1)
            self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM occurrences WHERE container_id=?",(child["id"],)).fetchone()[0],1)
    def test_04_malformed_pftxs_and_member_bounds(self):
        for kind,data in (("pftxs",pftxs(True)),("fpk",fpk(bad=True))):
            src=self.base/("bad-"+kind);src.write_bytes(data)
            output=self.base/("bad-"+kind+".jsonl")
            with self.assertRaises(m.CatalogueError): self.cat.bridge("index",kind,src,output)
    def test_04b_partial_jsonl_never_imported(self):
        names=[b"/Assets/catalogue/first.bin",b"/Assets/catalogue/second.bin"]
        start=48+96
        offsets=[start,start+len(names[0])+1]
        data_offset=(offsets[1]+len(names[1])+1+15)//16*16
        total=data_offset+4
        header=b"foxfpk win"+struct.pack("<I",total)+bytes(18)+struct.pack("<IIII",2,2,0,0)
        entries=b"".join(struct.pack("<IIIIIIII",data_offset if i==0 else total+1,0,4,0,offsets[i],0,len(n),0)+hashlib.md5(n).digest() for i,n in enumerate(names))
        data=header+entries+names[0]+b"\0"+names[1]+b"\0"
        data+=bytes(data_offset-len(data))+b"TEST"
        path=self.game/"master/partial.fpk"
        path.write_bytes(data)
        self.cat.census()
        row=self.cat.db.execute("SELECT c.* FROM containers c JOIN sources s ON s.id=c.source_id WHERE s.relative_path='master/partial.fpk'").fetchone()
        with self.assertRaises(m.CatalogueError):self.cat.index_one(row)
        self.assertEqual(self.cat.db.execute("SELECT COUNT(*) FROM occurrences WHERE container_id=?",(row["id"],)).fetchone()[0],0)
        self.assertEqual(self.cat.db.execute("SELECT state FROM containers WHERE id=?",(row["id"],)).fetchone()[0],"failed")
        outputs=list((self.cat.runtime/"indexes").glob(row["id"][:16]+"-*.jsonl"))
        self.assertEqual(len(outputs),1)
        self.assertEqual(len(outputs[0].read_text().splitlines()),1)
    def test_05_cancel_and_read_budget(self):
        self.cat.setmeta("cancel","1")
        with self.assertRaises(KeyboardInterrupt): self.cat.cancelled()
        self.cat.setmeta("cancel","0")
        b=m.Budget(10)
        b.charge(10)
        with self.assertRaises(m.CatalogueError): b.charge(1)
    def test_05b_actual_owned_child_cancel_and_timeout(self):
        original_exe, original_timeout = self.cat.exe, self.cat.timeout
        self.cat.exe = self.cat.exe.parent / "fixture_builder.exe"
        source = self.game / "master/test.dat"
        def cancel():
            time.sleep(0.3)
            db=sqlite3.connect(self.cat.runtime/"catalogue.sqlite")
            db.execute("INSERT OR REPLACE INTO meta VALUES('cancel','1')")
            db.commit()
            db.close()
        worker=threading.Thread(target=cancel)
        worker.start()
        try:
            with self.assertRaises(KeyboardInterrupt):
                self.cat.bridge("index","qar",source,self.base/"cancelled.jsonl")
            worker.join()
            self.assertIsNone(self.cat.process)
            self.cat.setmeta("cancel","0")
            self.cat.budget=m.Budget(128*m.MIB)
            self.cat.timeout=0.3
            with self.assertRaisesRegex(m.CatalogueError,"child_timeout"):
                self.cat.bridge("index","qar",source,self.base/"timeout.jsonl")
            self.assertIsNone(self.cat.process)
        finally:
            self.cat.exe,self.cat.timeout=original_exe,original_timeout
            self.cat.setmeta("cancel","0")
            self.cat.budget=m.Budget(128*m.MIB)
    def test_06_snapshot_change_and_export_seam(self):
        result=self.cat.export()
        export=Path(result["export"])
        con=sqlite3.connect(export/"catalogue.sqlite")
        self.assertNotIn("events",[r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")])
        con.close()
        for file in export.glob("*"):
            if file.suffix in (".csv",".json",".md"):
                self.assertNotIn(str(self.base),file.read_text(encoding="utf-8"))
        source=self.cat.db.execute("SELECT * FROM sources WHERE kind='qar'").fetchone()
        archive=self.game/source["relative_path"]
        archive.touch()
        with self.assertRaises(m.CatalogueError): self.cat.validate_source(source["id"])

class Pure(unittest.TestCase):
    def test_classification_and_unsigned_hash_storage(self):
        self.assertEqual(m.classify("master/e2.dat",bytes.fromhex("3026b2758e66cf11a6d900aa0062ce6c")),("asf","loose_media"))
        self.assertEqual(m.classify("master/a.dat.original",b"SQAR"),("excluded","backup"))
        self.assertEqual(m.classify("save/private.dat",b"SQAR"),("excluded","protected_private"))
        self.assertEqual(m.count_arg("all"),None)
        with self.assertRaises(Exception): m.count_arg("0")
    def test_budget_and_path_guards(self):
        b=m.Budget(3);b.charge(2)
        with self.assertRaises(m.CatalogueError):b.charge(2)
        with self.assertRaises(m.CatalogueError):m.Catalogue({"gameRoot":str(m.HERE),"toolRoot":str(m.HERE),"runtimeRoot":str(m.HERE/"runtime")})

if __name__=="__main__":unittest.main(verbosity=2)
