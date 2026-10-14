"""Read complete snapshots and fail closed when the game feed stops."""
import copy
import json
import math
from pathlib import Path
import threading
import time
from NativeNameResolver import ReadOnlyGame

class Snapshot:
    def __init__(self, path, validate):
        self.path, self.validate = Path(path), validate
        self.cache, self.updated = None, None
        self.lock = threading.Lock()

    def read(self):
        with self.lock:
            try:
                before = self.path.stat()
                value = json.loads(self.path.read_bytes())
                after = self.path.stat()
                if (self.validate(value) and before.st_mtime_ns == after.st_mtime_ns
                        and before.st_size == after.st_size):
                    self.cache, self.updated = value, after.st_mtime
            except (OSError, ValueError):
                pass
            if self.cache is None:
                raise ValueError("No complete game snapshot is available")
            return {**copy.deepcopy(self.cache),
                    "feedAgeSeconds": max(0, time.time() - self.updated)}

def life_valid(value):
    return (isinstance(value, dict) and type(value.get("realTime")) in (int, float)
            and math.isfinite(value["realTime"]) and isinstance(value.get("actors"), list))

class Runtime:
    def __init__(self, config):
        self.config = config
        self.life = Snapshot(config["mod_root"] / "nlab_life_status.json", life_valid)
        self.map = Snapshot(config["mod_root"] / "nlab_base_map.json",
                            lambda v: isinstance(v, dict) and v.get("schema") == 1)
        self.last_time, self.last_changed = None, 0
        self.lock = threading.Lock()

    def readiness(self, life=None):
        life = life if life is not None else self.life.read()
        with self.lock:
            # First observation can be current, but a cached/nonadvancing feed
            # loses action permission after five real seconds.
            if life["realTime"] != self.last_time:
                self.last_time, self.last_changed = life["realTime"], time.monotonic()
            ready = life["feedAgeSeconds"] <= 10 and time.monotonic() - self.last_changed < 5
        # Core snapshots historically use both nativeProfile and mission fields.
        ready = ready and life.get("nativeProfile") is True
        if life.get("mission") is not None:
            ready = ready and life["mission"] == 30050
        if life.get("ready") is False or life.get("paused") is True:
            ready = False
        if not ready:
            return {"ready": False, "reason": "Game feed stale, paused or outside normal Mother Base"}
        reader = None
        try:
            # Process identity only: name enrichment signatures never authorize actions.
            reader = ReadOnlyGame(self.config["game_exe"], resolve_native=False)
            return {"ready": True, "reason": "Fresh normal Mother Base feed and configured process", "pid": reader.pid}
        except (OSError, ValueError, AttributeError):
            return {"ready": False, "reason": "Configured game process is closed or unavailable"}
        finally:
            if reader:
                reader.close()

    def map_status(self):
        try:
            return self.map.read()
        except ValueError:
            return None
