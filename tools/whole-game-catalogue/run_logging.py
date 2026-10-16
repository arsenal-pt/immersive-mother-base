"""Bounded private console transcripts and run summaries; no environment/payload dump."""
from datetime import datetime, timezone
import contextlib
import json
import os
from pathlib import Path
import time
import uuid

MAX_LOG_BYTES = 8 * 1024 * 1024
MAX_REASONS = 50

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

def compact_counts(status):
    counts = dict.fromkeys(("outer_indexed","outer_members","nested_indexed","nested_pending","nested_review","nested_running","nested_cancelled"),0)
    for row in status.get("container_coverage",[]):
        if row["layer"]=="outer" and row["state"]=="indexed":
            counts["outer_indexed"]+=row["containers"]
            counts["outer_members"]+=row["members"] or 0
        elif row["layer"]=="nested":
            key={"indexed":"nested_indexed","pending":"nested_pending","cancelled":"nested_cancelled","running":"nested_running","failed":"nested_review","deferred":"nested_review"}.get(row["state"])
            if key: counts[key]+=row["containers"]
    counts.update(remaining=counts["nested_pending"]+counts["nested_cancelled"],
                  occurrences=sum(status.get("types",{}).values()),models_found=status.get("types",{}).get("fmdl",0),
                  dependency_resolved=status.get("dependency_resolved",0),previews=status.get("previews",0))
    return counts

class Tee:
    def __init__(self,original,journal):
        self.original,self.journal=original,journal
    def write(self,text):
        value=self.original.write(text)
        self.journal.write_text(text)
        return value
    def flush(self):
        self.original.flush()
        self.journal.transcript.flush()
    def __getattr__(self,name):
        return getattr(self.original,name)

class RunJournal:
    def __init__(self,runtime,command,inputs):
        self.root=Path(runtime)/"logs"
        self.root.mkdir(parents=True,exist_ok=True)
        self.run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")+"-"+uuid.uuid4().hex[:8]
        self.directory=self.root/"runs"/self.run_id
        self.directory.mkdir(parents=True)
        self.paths={key:"runs/"+self.run_id+"/"+file for key,file in (("summary","summary.json"),("transcript","transcript.txt"),("events","events.jsonl"))}
        self.summary_path=self.root/self.paths["summary"]
        self.transcript=(self.root/self.paths["transcript"]).open("w",encoding="utf-8",newline="")
        self.events=(self.root/self.paths["events"]).open("w",encoding="utf-8",newline="")
        self.started=time.monotonic()
        self.text_bytes=self.event_bytes=0
        self.summary={"schema_version":1,"run_id":self.run_id,"pid":os.getpid(),"command":command,"inputs":inputs,
            "entered_inputs":[],"started_at":utc_now(),"ended_at":None,"status":"running","exit_code":None,
            "before":{},"after":{},"attempted":0,"succeeded":0,"skipped":0,"errors":0,"reasons":[],
            "attempt_scope":"outer_archives" if command=="index" else "nested_containers",
            "phases":{name:{"attempted":0,"succeeded":0,"skipped":0,"errors":0} for name in ("index","expand")},
            "phase_results":{},
            "export_path":None,"paths":self.paths,"event_count":0,"transcript_truncated":False,"events_truncated":False}
        self.save()
        self.atomic(self.root/"latest-run.json",{"run_id":self.run_id,"pid":os.getpid(),**self.paths})
        self.emit("run_started",{"command":command})
    @staticmethod
    def atomic(path,value):
        temp=path.with_name(path.name+"."+uuid.uuid4().hex[:8]+".tmp")
        with temp.open("w",encoding="utf-8") as stream:
            json.dump(value,stream,ensure_ascii=False,indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp,path)
    def save(self):
        self.summary.update(transcript_bytes=self.text_bytes,events_bytes=self.event_bytes)
        self.atomic(self.summary_path,self.summary)
    def write_text(self,text):
        data=text.encode("utf-8",errors="replace")
        if self.text_bytes+len(data)<=MAX_LOG_BYTES:
            self.transcript.write(text)
            self.text_bytes+=len(data)
        elif not self.summary["transcript_truncated"]:
            self.summary["transcript_truncated"]=True
            note="\n[Transcript limit reached; machine summary remains available.]\n"
            room=max(0,MAX_LOG_BYTES-self.text_bytes-len(note.encode()))
            clipped=(data[:room].decode("utf-8",errors="ignore")+note).encode("utf-8")[:max(0,MAX_LOG_BYTES-self.text_bytes)].decode("utf-8",errors="ignore")
            self.transcript.write(clipped)
            self.text_bytes+=len(clipped.encode("utf-8"))
        self.transcript.flush()
    def emit(self,event,detail=None):
        text=json.dumps({"at":utc_now(),"event":event,"detail":detail or {}},ensure_ascii=False,separators=(",",":"))+"\n"
        size=len(text.encode("utf-8"))
        self.summary["event_count"]+=1
        if self.event_bytes+size<=MAX_LOG_BYTES:
            self.events.write(text)
            self.events.flush()
            self.event_bytes+=size
        else:self.summary["events_truncated"]=True
        self.save()
    def set_before(self,status):
        self.summary["before"]=compact_counts(status)
        self.emit("coverage_before",self.summary["before"])
    def entered(self,name,value):
        item={"name":name,"value":str(value)[:128]}
        self.summary["entered_inputs"].append(item)
        self.emit("input",item)
    def error(self,reason):
        self.summary["errors"]=max(1,self.summary["errors"])
        if len(self.summary["reasons"])<MAX_REASONS:self.summary["reasons"].append(str(reason)[:2000])
        self.emit("error",{"reason":str(reason)[:2000]})
    def progress(self,event,detail):
        detail={key:(value[:2000] if isinstance(value,str) else value) for key,value in detail.items()}
        phase=detail.get("phase")
        counts=self.summary["phases"].get(phase)
        if counts is not None:
            if event=="container_started":counts["attempted"]+=1
            elif event=="container_completed":counts["succeeded"]+=1
            elif event=="container_skipped":counts["skipped"]+=1
            elif event=="container_error":
                counts["errors"]+=1
                if len(self.summary["reasons"])<MAX_REASONS:self.summary["reasons"].append(detail.get("reason","unknown"))
            if phase=="expand" or self.summary["command"]=="index":
                for key in ("attempted","succeeded","skipped","errors"):self.summary[key]=counts[key]
        self.emit(event,detail)
        if getattr(self,"human",False):
            name=detail.get("name","") or detail.get("container_id","")
            if len(name)>120:name="..."+name[-117:]
            if event=="container_started":
                total=detail.get("total")
                allowance=str(total) if total is not None else "all within limits"
                print("Starting "+("outer" if phase=="index" else "nested")+" "+str(detail.get("number",1))+"/"+allowance+": "+name,flush=True)
            elif event=="container_completed":print("Indexed: "+name,flush=True)
            elif event=="container_skipped":print("Skipped completed container: "+name,flush=True)
            elif event=="container_error":
                import sys
                print("Needs attention: "+name+" - "+detail.get("reason","unknown"),file=sys.stderr,flush=True)
    def phase_result(self,phase,result):
        allowed=("files","attempts","indexed","needs_attention","payload_decodes","helper_processes","read_bytes","indexed_this_run","cache_hit","cancel_requested")
        self.summary["phase_results"][phase]={key:result[key] for key in allowed if key in result}
        self.emit("phase_completed",{"phase":phase,**self.summary["phase_results"][phase]})
    def finish(self,exit_code,status,result=None,work=None):
        result,work=result or {},work or {}
        self.summary["after"]=compact_counts(status)
        for target,key in (("attempted","attempts"),("succeeded","indexed"),("errors","needs_attention")):
            self.summary[target]=max(self.summary[target],work.get(key,0))
        self.summary["skipped"]=max(self.summary["skipped"],int(bool(work.get("cache_hit"))))
        self.summary.update(export_path=result.get("export",self.summary["export_path"]),exit_code=exit_code,
            status="cancelled" if exit_code==130 else "needs_attention" if exit_code==1 else "succeeded" if exit_code==0 else "failed",
            ended_at=utc_now(),duration_seconds=round(time.monotonic()-self.started,3))
        allowed=("attempts","indexed","needs_attention","payload_decodes","helper_processes","read_bytes","indexed_this_run","cache_hit","cancel_requested")
        self.summary["result"]={key:work[key] for key in allowed if key in work}
        self.emit("run_finished",{"status":self.summary["status"],"exit_code":exit_code})
    @contextlib.contextmanager
    def capture(self):
        import sys
        with contextlib.redirect_stdout(Tee(sys.stdout,self)),contextlib.redirect_stderr(Tee(sys.stderr,self)):
            yield
    def close(self):
        self.transcript.close()
        self.events.close()


def print_coverage(label,status):
    counts=compact_counts(status)
    print(label+": outer "+format(counts["outer_indexed"],",")+" archives / "+format(counts["outer_members"],",")+
          " members; nested "+format(counts["nested_indexed"],",")+" indexed, "+format(counts["remaining"],",")+
          " remaining, "+format(counts["nested_review"],",")+" need review.",flush=True)
    pending=status.get("next_nested",[])
    if pending:
        name=pending[0].get("name") or pending[0]["id"]
        print("Next: "+str(name),flush=True)

def print_log_paths(journal):
    print("Transcript: "+str(journal.root/journal.paths["transcript"]),flush=True)
    print("Run summary: "+str(journal.summary_path),flush=True)
    print("Latest run: "+str(journal.root/"latest-run.json"),flush=True)

def print_footer(journal,status):
    s=journal.summary
    print("Result: "+s["status"]+" (exit "+str(s["exit_code"])+").",flush=True)
    label="Outer: " if s["attempt_scope"]=="outer_archives" else "Nested: "
    print(label+"Attempted "+str(s["attempted"])+", indexed "+str(s["succeeded"])+", skipped "+str(s["skipped"])+
          ", errors "+str(s["errors"])+". Remaining "+format(s["after"].get("remaining",0),",")+".",flush=True)
    outer=s["phase_results"].get("index")
    if outer is not None:print("Outer indexed this run: "+str(outer.get("indexed_this_run",0))+".",flush=True)
    print("Metadata only; no model previews generated.",flush=True)
    if s["export_path"]:print("Export: "+s["export_path"],flush=True)
    print("Transcript: "+str(journal.root/journal.paths["transcript"]),flush=True)
    print("Run summary: "+str(journal.summary_path),flush=True)
