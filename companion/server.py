"""Optional local dashboard; simulation remains in the installed game Lua."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from config import parse_config
from runtime import Runtime
from NativeNameResolver import NameService
from StaffControlService import StaffControlService, StaffCommandError
from commands import LifeCommands

ROOT = Path(__file__).resolve().parent

class CompanionServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, config):
        self.config = config
        self.runtime = Runtime(config)
        self.names = NameService(config["game_exe"], config.get("name_resources"), config["native_names"])
        self.staff = StaffControlService(config["mod_root"])
        self.commands = LifeCommands(config["mod_root"], self.runtime)
        super().__init__((config["host"], config["port"]), Handler)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, status, value, mime="application/json; charset=utf-8"):
        data = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        name = self.path.split("?")[0]
        server = self.server
        try:
            if name == "/status":
                status = server.runtime.life.read()
                status.pop("ihStaff", None)
                # Extra-adapter actors are excluded from this standalone view.
                status["actors"] = [a for a in status["actors"] if a.get("staffSource") != "Infinite Heaven dependency"
                                    and not str(a.get("presenceSource", "")).startswith("existing IH actor")]
                status["runtime"] = server.runtime.readiness(status)
                status = server.names.enrich(status)
                status["baseMap"] = server.runtime.map_status()
                status["staffControl"] = server.staff.snapshot()
                return self.respond(200, status)
            if name == "/staff-status":
                return self.respond(200, server.staff.snapshot())
            if name == "/base-map-state":
                value = server.runtime.map_status()
                if value is None:
                    raise ValueError("Base map feed unavailable")
                return self.respond(200, value)
            routes = {
                "/": (ROOT / "index.html", "text/html; charset=utf-8"),
                "/base-map.js": (ROOT / "base-map.js", "text/javascript; charset=utf-8"),
                "/base-map-geometry": (server.config.get("geometry_catalog"), "application/json"),
                "/layout": (server.config.get("layout_file"), "application/json")}
            if name not in routes:
                return self.respond(404, {"error": "Unknown route"})
            path, mime = routes[name]
            if path is None:
                raise ValueError("Optional local data is unavailable")
            return self.respond(200, Path(path).read_bytes(), mime)
        except (OSError, ValueError) as exc:
            return self.respond(503, {"error": str(exc)})

    def do_POST(self):
        server = self.server
        origins = {None, "http://127.0.0.1:" + str(server.server_port),
                   "http://localhost:" + str(server.server_port)}
        if self.path not in ("/command", "/staff-command") or self.headers.get("Origin") not in origins:
            return self.respond(403, {"error": "Route or Origin is not allowed"})
        try:
            if self.headers.get("Transfer-Encoding"):
                raise StaffCommandError("Unsupported request framing")
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size < 512:
                raise StaffCommandError("Request body must be smaller than 512 bytes")
            payload = json.loads(self.rfile.read(size))
            if self.path == "/command":
                response = server.commands.submit(payload)
            else:
                response = server.staff.submit(payload, server.runtime.readiness()["ready"])
            return self.respond(202, response)
        except StaffCommandError as exc:
            return self.respond(exc.status, {"error": str(exc)})
        except (KeyError, TypeError, OSError, ValueError):
            return self.respond(400, {"error": "Invalid request or unavailable IPC"})

def main():
    config = parse_config()
    with CompanionServer(config) as server:
        print(json.dumps({"url": "http://127.0.0.1:" + str(server.server_port),
                          "status": "pre-alpha companion; game is not launched"}), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
