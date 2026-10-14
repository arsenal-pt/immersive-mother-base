"""Explicit portable configuration; no implicit game paths."""
import argparse
import json
from pathlib import Path

PATHS = ("game_exe", "mod_root", "geometry_catalog", "layout_file", "name_resources")

def parse_config(argv=None):
    parser = argparse.ArgumentParser(description="Immersive Mother Base optional local companion")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--game-exe")
    parser.add_argument("--mod-root")
    parser.add_argument("--port", type=int)
    parser.add_argument("--host", choices=("127.0.0.1", "localhost"))
    parser.add_argument("--geometry-catalog")
    parser.add_argument("--layout-file")
    parser.add_argument("--name-resources")
    parser.add_argument("--native-names", action="store_true", default=None)
    args = parser.parse_args(argv)
    config = {"host": "127.0.0.1", "port": 8785, "native_names": False}
    base = Path.cwd()
    if args.config:
        try:
            config_file = args.config.resolve()
            loaded = json.loads(config_file.read_text(encoding="utf-8"))
            allowed = set(PATHS) | {"host", "port", "native_names"}
            if not isinstance(loaded, dict) or set(loaded) - allowed:
                parser.error("Configuration contains unknown fields")
            config.update(loaded)
            base = config_file.parent
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
    for key, value in vars(args).items():
        if key != "config" and value is not None:
            config[key] = value
            if key in PATHS:
                config[key] = str(Path(value).resolve())
    if config["host"] not in ("127.0.0.1", "localhost"):
        parser.error("Companion listens on loopback only")
    if type(config["port"]) is not int or not 0 <= config["port"] <= 65535:
        parser.error("Port must be an integer from 0 to 65535")
    if type(config["native_names"]) is not bool:
        parser.error("native_names must be true or false")
    for key in PATHS:
        value = config.get(key)
        if value is not None:
            if not isinstance(value, str) or not value:
                parser.error(key + " must be a path or null")
            path = Path(value)
            config[key] = (path if path.is_absolute() else base / path).resolve()
    if not config.get("mod_root") or not config.get("game_exe"):
        parser.error("Explicit --mod-root and --game-exe are required (or set them in --config)")
    if not config["mod_root"].is_dir():
        parser.error("mod_root must be an existing directory; this companion never installs the core")
    return config
