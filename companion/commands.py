"""Original game mailbox protocol, independent of optional staff adapters."""
import threading
import uuid
from StaffControlService import StaffCommandError

ALLOWED = {"muster", "gather", "roam", "toilet", "shower", "mess", "water", "bunk",
           "autonomy", "morning_test", "evening_test", "duty", "guard",
           "cqc", "cqc_four", "cqc_stop", "cqc_auto"}

class LifeCommands:
    def __init__(self, mod, runtime):
        self.mod, self.runtime = mod, runtime
        self.lock = threading.Lock()

    def submit(self, payload):
        if not isinstance(payload, dict) or set(payload) != {"command"} or payload["command"] not in ALLOWED:
            raise StaffCommandError("Unsupported routine command")
        command = payload["command"]
        with self.lock:
            life = self.runtime.life.read()
            if not self.runtime.readiness(life)["ready"]:
                raise StaffCommandError("Game closed, paused or status feed stale; command was not queued", 409)
            if command in {"muster", "gather", "cqc", "cqc_four", "cqc_auto"} and life.get("assemblyReservation"):
                raise StaffCommandError("Assembly pad is reserved by another active activity", 409)
            if command in {"cqc", "cqc_four", "cqc_auto"} and not (life.get("cqcTraining") or {}).get("ready"):
                raise StaffCommandError("CQC training is waiting for native verification", 409)
            if command == "cqc_auto" and not (life.get("cqcTraining") or {}).get("scheduleReady"):
                raise StaffCommandError("Scheduled CQC training still requires session and rumble verification", 409)
            path = self.mod / "nlab_life_command.txt"
            try:
                words = path.read_text(encoding="utf-8").split()
            except OSError:
                words = []
            if words and words[0] != life.get("lastCommand"):
                raise StaffCommandError("The previous routine command is still waiting for the game", 409)
            uid = "dashboard_" + uuid.uuid4().hex[:12]
            temporary = path.with_name(path.name + "." + uid + ".tmp")
            try:
                temporary.write_text(uid + " " + command + "\n", encoding="utf-8", newline="\n")
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
            return {"id": uid}
