"""Compatibility import/CLI for the canonical Command Platform1 v9.1 helper.
Original source GPL-3.0-only. No game assets included.
"""
from pathlib import Path
import importlib.util
import runpy
CANONICAL = Path(__file__).resolve().parent.parent / "command/platform-1/versions/v9.1/rebuild.py"
_spec = importlib.util.spec_from_file_location("_imb_command_platform1_v91_rebuild", CANONICAL)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
HERE = _module.HERE
sha = _module.sha
child = _module.child
originals = _module.originals
reconstruct = _module.reconstruct
rebuild = _module.rebuild
if __name__ == "__main__":
    runpy.run_path(str(CANONICAL), run_name="__main__")
