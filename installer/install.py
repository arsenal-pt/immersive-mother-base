#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Implementation contributor: OpenAI Codex (AI assistant).
"""Reversible loose-Lua installer. Never patches game archives or launches MGSV."""
from __future__ import annotations
import argparse
import ctypes
from contextlib import contextmanager
from functools import wraps
import threading
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import tempfile
import uuid

OWNED_TARGETS = frozenset(
    ["mod/modules/" + name + ".lua" for name in (
        "ImmersiveMotherBase", "NpcTraining", "NlabActionRecorder", "NpcLife", "NpcSoldiers", "NpcBaseMap")]
    + ["mod/nlab/" + name + ".lua" for name in (
        "NpcRegistry", "NativeHierarchy", "NativeServiceBindings", "CqcRosterPolicy", "CqcPairPlan",
        "CqcTrainingPlan", "CqcDrillSession", "NativeMotionObserver", "StaffConfig", "NpcLifeCore",
        "LifeLayout", "NativeCqcTraining", "CqcTrainingProof", "ActionRecorderCore")])
KNOWN_LEGACY_ADAPTER_MODULES = ("mod/modules/NpcIHStaff.lua",)
BACKUP_ROOT = "mod/imb-install-backups"
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9][a-zA-Z0-9.-]*)?\Z")
RECEIPT_ID_RE = re.compile(r"[0-9]{8}T[0-9]{12}Z-[0-9a-f]{12}\Z")

class InstallError(RuntimeError):
    """Check failure or safely restored transaction failure."""

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

def plain_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise InstallError("Invalid relative path in package or receipt.")
    parts = value.split("/")
    reserved = re.compile(r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z", re.I)
    if PurePosixPath(value).is_absolute() or any(
        p in ("", ".", "..") or p[-1:] in (" ", ".") or reserved.fullmatch(p)
        or any(c in p for c in '<>"|?*') for p in parts):
        raise InstallError("Unsafe relative path in package or receipt.")
    return value

def no_links(path: Path) -> None:
    for node in (path, *path.parents):
        try:
            s = node.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(s.st_mode) or getattr(s, "st_file_attributes", 0) & 0x400:
            raise InstallError("Symbolic links and Windows reparse points are not allowed: " + str(node))

def absolute_root(path: str | Path) -> Path:
    root = Path(os.path.abspath(path))
    no_links(root)
    if not root.is_dir():
        raise InstallError("Folder does not exist: " + str(root))
    return root

def within(root: Path, relative: str) -> Path:
    path = root.joinpath(*plain_path(relative).split("/"))
    no_links(path)
    if not path.is_relative_to(root):
        raise InstallError("Path escapes its expected folder.")
    return path

def read_regular(path: Path, limit: int = 32 * 1024 * 1024) -> bytes:
    no_links(path)
    try:
        s = path.stat()
        if not stat.S_ISREG(s.st_mode) or s.st_size > limit:
            raise InstallError("Expected a bounded regular file: " + str(path))
        return path.read_bytes()
    except OSError as exc:
        raise InstallError("Cannot read required file: " + str(path)) from exc

def current_hash(path: Path) -> str | None:
    no_links(path)
    return digest(read_regular(path)) if path.exists() else None

def mkdir_tracked(path: Path, created: list[Path]) -> None:
    no_links(path)
    missing = []
    node = path
    while not node.exists():
        missing.append(node)
        node = node.parent
    if not node.is_dir():
        raise InstallError("A required parent is a file: " + str(node))
    for node in reversed(missing):
        no_links(node)
        node.mkdir()
        created.append(node)

def atomic_write(path: Path, data: bytes) -> None:
    no_links(path)
    fd, temporary = tempfile.mkstemp(prefix=".imb-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        no_links(path)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def read_json(path: Path) -> dict:
    try:
        value = json.loads(read_regular(path).decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise InstallError("Invalid JSON file: " + str(path)) from exc
    if not isinstance(value, dict):
        raise InstallError("Expected a JSON object: " + str(path))
    return value

def is_pe(path: Path) -> bool:
    no_links(path)
    try:
        with path.open("rb") as stream:
            header = stream.read(64)
            if len(header) != 64 or header[:2] != b"MZ":
                return False
            offset = struct.unpack_from("<I", header, 60)[0]
            if offset < 64 or offset > 1024 * 1024:
                return False
            stream.seek(offset)
            return stream.read(4) == b"PE\0\0"
    except OSError:
        return False

def game_running() -> bool:
    """Windows Toolhelp process enumeration; no termination or shell command."""
    if os.name != "nt":
        raise InstallError("The installer runs on Windows; process detection is unavailable here.")
    from ctypes import wintypes
    class ProcessEntry(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    api.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    api.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    api.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
    api.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
    api.Process32FirstW.restype = api.Process32NextW.restype = wintypes.BOOL
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = api.CreateToolhelp32Snapshot(2, 0)
    if handle == ctypes.c_void_p(-1).value:
        raise InstallError("Could not inspect running processes; no files were changed.")
    try:
        entry = ProcessEntry()
        entry.dwSize = ctypes.sizeof(entry)
        if not api.Process32FirstW(handle, ctypes.byref(entry)):
            raise InstallError("Could not enumerate running processes; no files were changed.")
        while True:
            if entry.szExeFile.casefold() == "mgsvtpp.exe":
                return True
            if not api.Process32NextW(handle, ctypes.byref(entry)):
                if ctypes.get_last_error() != 18:
                    raise InstallError("Process inspection failed; no files were changed.")
                return False
    finally:
        api.CloseHandle(handle)

def ensure_stopped(process_checker) -> None:
    if process_checker():
        raise InstallError("Close MGSV (mgsvtpp.exe) before installing or restoring files.")

def validate_game(game_dir: str | Path, require_framework: bool = True) -> tuple[Path, list[str]]:
    game = absolute_root(game_dir)
    if not is_pe(within(game, "mgsvtpp.exe")):
        raise InstallError("Select the existing MGS_TPP folder containing mgsvtpp.exe (a Windows PE file).")
    findings = ["MGSV executable present; ownership, DRM and native compatibility are not verified by this check."]
    if require_framework:
        conflicts = [relative for relative in KNOWN_LEGACY_ADAPTER_MODULES if within(game, relative).exists()]
        if conflicts:
            raise InstallError("This alpha excludes the private IH staff adoption adapter: " + ", ".join(conflicts)
                + ". Use a separate clean test game/mod setup or manually review backups before migrating the old private adapter. "
                + "Keep the original IH/IHHook framework installed. No files were changed.")
        for relative in ("mod/modules/InfMenu.lua", "mod/modules/InfMenuDefs.lua"):
            if not read_regular(within(game, relative), 4 * 1024 * 1024):
                raise InstallError("Install external Infinite Heaven first: missing " + relative)
        hook = None
        for relative in ("dinput8.dll", "plugins/IHHook.dll", "plugins/IHHook.asi", "IHHook.dll", "IHHook.asi"):
            path = within(game, relative)
            if path.exists() and is_pe(path):
                raw = read_regular(path).lower()
                if b"ihhook" in raw or "ihhook".encode("utf-16le") in raw:
                    hook = relative
                    break
        if hook is None:
            raise InstallError("Install external IHHook first. No recognized PE hook containing its IHHook identity was found.")
        findings += ["Infinite Heaven menu files present.", "IHHook identity present in " + hook + ".",
            "Structural dependency checks do not verify executable-version, VC++ runtime or native gameplay acceptance."]
    return game, findings

def load_package(package_root: str | Path) -> tuple[Path, dict, dict[str, bytes]]:
    root = absolute_root(package_root)
    manifest = read_json(within(root, "installer/package-manifest.json"))
    if manifest.get("schemaVersion") != 1 or manifest.get("product") != "Immersive Mother Base":
        raise InstallError("Unrecognized package manifest.")
    version = manifest.get("version", "")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise InstallError("Invalid package version.")
    if read_regular(within(root, "VERSION"), 200).decode("utf-8").strip() != version:
        raise InstallError("VERSION and installer manifest disagree.")
    if manifest.get("license") != "GPL-3.0-only" or manifest.get("nativeAcceptance") is not False:
        raise InstallError("This alpha installer requires its GPL-3.0-only/nativeAcceptance=false scope.")
    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != len(OWNED_TARGETS):
        raise InstallError("Manifest must contain exactly the 20 owned core Lua files.")
    payload = {}
    for entry in files:
        if not isinstance(entry, dict):
            raise InstallError("Invalid manifest entry.")
        target, source, sha = entry.get("target"), entry.get("source"), entry.get("sha256")
        plain_path(target)
        plain_path(source)
        if target not in OWNED_TARGETS or target in payload or source != "core/GameDir/" + target:
            raise InstallError("Manifest target/source is outside the owned allowlist or duplicated.")
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            raise InstallError("Invalid source SHA-256.")
        data = read_regular(within(root, source), 4 * 1024 * 1024)
        if len(data) != entry.get("size") or digest(data) != sha:
            raise InstallError("Package file is corrupted: " + source)
        payload[target] = data
    if set(payload) != OWNED_TARGETS:
        raise InstallError("Incomplete core allowlist.")
    return root, manifest, payload

def load_receipt(game: Path, path: Path) -> dict:
    path = Path(os.path.abspath(path))
    if not path.is_relative_to(within(game, BACKUP_ROOT)) or path.name != "install-receipt.json":
        raise InstallError("Receipt must be inside this game's imb-install-backups folder.")
    receipt = read_json(path)
    version, receipt_id = receipt.get("version", ""), receipt.get("id", "")
    if receipt.get("schemaVersion") != 1 or receipt.get("product") != "Immersive Mother Base":
        raise InstallError("Invalid install receipt.")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version) or not isinstance(receipt_id, str) or not RECEIPT_ID_RE.fullmatch(receipt_id):
        raise InstallError("Invalid receipt version or ID.")
    expected = within(game, BACKUP_ROOT + "/" + version + "/" + receipt_id + "/install-receipt.json")
    if path != expected or not isinstance(receipt.get("gameDir"), str) or os.path.normcase(os.path.abspath(receipt["gameDir"])) != os.path.normcase(str(game)):
        raise InstallError("Receipt does not belong to this game/path.")
    entries = receipt.get("files")
    if not isinstance(entries, list) or len(entries) != len(OWNED_TARGETS):
        raise InstallError("Invalid receipt file list.")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("target") not in OWNED_TARGETS or entry["target"] in seen:
            raise InstallError("Receipt contains a duplicate/unowned target.")
        seen.add(entry["target"])
        for key in ("installedSha256", "originalSha256", "beforeSha256"):
            value = entry.get(key)
            if value is not None and (not isinstance(value, str) or not SHA_RE.fullmatch(value)):
                raise InstallError("Invalid receipt hash.")
        if not entry.get("installedSha256") or not isinstance(entry.get("originalOrigin"), str):
            raise InstallError("Receipt lacks installed-file provenance.")
    prior = receipt.get("priorActive")
    if prior is not None:
        if not isinstance(prior, dict) or not isinstance(prior.get("receipt"), str) or not prior["receipt"].startswith(BACKUP_ROOT + "/"):
            raise InstallError("Invalid prior-install pointer.")
        within(game, prior["receipt"])
    return receipt

def active_receipt(game: Path) -> tuple[Path | None, dict | None, bytes | None]:
    pointer = within(game, BACKUP_ROOT + "/active.json")
    if not pointer.exists():
        return None, None, None
    raw, value = read_regular(pointer), read_json(pointer)
    relative = value.get("receipt", "")
    if not isinstance(relative, str) or not relative.startswith(BACKUP_ROOT + "/"):
        raise InstallError("Invalid active-install pointer.")
    path = within(game, relative)
    receipt = load_receipt(game, path)
    if receipt.get("state") != "installed":
        raise InstallError("An interrupted install/restore needs recovery: " + str(path))
    return path, receipt, raw

def guard_hash(game: Path, target: str, expected: str | None) -> None:
    if current_hash(within(game, target)) != expected:
        raise InstallError("File changed; preserving it without modification: " + target)

def backup_data(receipt_dir: Path, folder: str, target: str, expected: str | None) -> bytes | None:
    if expected is None:
        return None
    data = read_regular(within(receipt_dir, folder + "/" + target))
    if digest(data) != expected:
        raise InstallError("Backup is corrupted; restoration refused: " + target)
    return data

def cleanup_empty(created: list[Path]) -> None:
    for path in reversed(created):
        try:
            no_links(path)
            path.rmdir()
        except OSError:
            pass

def restore_before(game: Path, receipt_dir: Path, receipt: dict, restoring_uninstall: bool = False) -> None:
    key = "installedSha256" if restoring_uninstall else "beforeSha256"
    folder = "uninstall-before" if restoring_uninstall else "before"
    actions = []
    for entry in receipt["files"]:
        target, expected = entry["target"], entry[key]
        current = current_hash(within(game, target))
        possible = {entry["installedSha256"], expected}
        if restoring_uninstall:
            possible.add(entry["originalSha256"])
        if current not in possible:
            raise InstallError("Recovery stopped to preserve a changed file: " + target)
        actions.append((target, backup_data(receipt_dir, folder, target, expected)))
    pointer = within(game, BACKUP_ROOT + "/active.json")
    old_active = receipt.get("priorActive")
    ours = str((receipt_dir / "install-receipt.json").relative_to(game)).replace("\\", "/")
    if pointer.exists() and read_json(pointer).get("receipt") not in (ours, (old_active or {}).get("receipt")):
        raise InstallError("A newer active installation exists; recovery refused.")
    for target, data in actions:
        path = within(game, target)
        if data is None:
            if path.exists():
                path.unlink()
        else:
            atomic_write(path, data)
        if current_hash(path) != (digest(data) if data is not None else None):
            raise InstallError("Restoration hash failed: " + target)
    if restoring_uninstall:
        atomic_write(pointer, json_bytes({"receipt": ours}))
        receipt["state"] = "installed"
    else:
        if old_active is None:
            if pointer.exists():
                pointer.unlink()
        else:
            atomic_write(pointer, json_bytes(old_active))
        receipt["state"] = "rolled_back"
    atomic_write(receipt_dir / "install-receipt.json", json_bytes(receipt))


_LOCK_LOCAL = threading.local()

@contextmanager
def transaction_lock(game: Path):
    """OS lock is released even if the installer process crashes."""
    active = getattr(_LOCK_LOCAL, "active", set())
    if str(game) in active:
        yield
        return
    path = within(game, BACKUP_ROOT + "/transaction.lock")
    mkdir_tracked(path.parent, [])
    no_links(path)
    if path.exists() and (not path.is_file() or path.stat().st_size > 1024):
        raise InstallError("Invalid installer transaction lock.")
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    locked = False
    try:
        if os.fstat(fd).st_size == 0:
            os.write(fd, b"0")
        os.lseek(fd, 0, os.SEEK_SET)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise InstallError("Another installer transaction is active; no core files changed.") from exc
        locked = True
        active = set(active)
        active.add(str(game))
        _LOCK_LOCAL.active = active
        yield
    finally:
        if locked:
            active.discard(str(game))
            _LOCK_LOCAL.active = active
            os.lseek(fd, 0, os.SEEK_SET)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)

def serialized(func):
    @wraps(func)
    def wrapper(game_dir, *args, **kwargs):
        if func.__name__ == "install":
            load_package(args[0] if args else kwargs["package_root"])
        game, _ = validate_game(game_dir, require_framework=func.__name__ == "install")
        ensure_stopped(kwargs.get("process_checker", game_running))
        with transaction_lock(game):
            return func(game, *args, **kwargs)
    return wrapper

@serialized
def install(game_dir: str | Path, package_root: str | Path, *, process_checker=game_running, write_file=atomic_write) -> Path:
    _, manifest, payload = load_package(package_root)
    game, _ = validate_game(game_dir)
    ensure_stopped(process_checker)
    previous_path, previous, active_raw = active_receipt(game)
    if previous:
        for entry in previous["files"]:
            guard_hash(game, entry["target"], entry["installedSha256"])
    targets = sorted(payload)
    before = {target: current_hash(within(game, target)) for target in targets}
    previous_entries = {e["target"]: e for e in previous["files"]} if previous else {}
    original, original_origin = {}, {}
    for target in targets:
        if target in previous_entries:
            entry = previous_entries[target]
            original[target] = backup_data(previous_path.parent, "original", target, entry["originalSha256"])
            original_origin[target] = entry["originalOrigin"]
        else:
            original[target] = read_regular(within(game, target)) if before[target] else None
            original_origin[target] = "pre-existing user file" if before[target] else "absent before first installation"
    receipt_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:12]
    receipt_dir = within(game, BACKUP_ROOT + "/" + manifest["version"] + "/" + receipt_id)
    mkdir_tracked(receipt_dir, [])
    receipt = {"schemaVersion": 1, "product": "Immersive Mother Base", "version": manifest["version"],
        "id": receipt_id, "gameDir": str(game), "state": "preparing", "nativeAcceptance": False,
        "packageManifestSha256": digest(json_bytes(manifest)), "createdUTC": datetime.now(timezone.utc).isoformat(),
        "priorActive": json.loads(active_raw) if active_raw else None, "files": [],
        "sourceTag": manifest.get("sourceTag"), "sourceCommit": manifest.get("sourceCommit"),
        "sourceTreeSha256": manifest.get("sourceTreeSha256")}
    for target in targets:
        for folder, data in (("original", original[target]), ("before", read_regular(within(game, target)) if before[target] else None)):
            if data is not None:
                backup = within(receipt_dir, folder + "/" + target)
                mkdir_tracked(backup.parent, [])
                atomic_write(backup, data)
        receipt["files"].append({"target": target, "beforeSha256": before[target],
            "originalSha256": digest(original[target]) if original[target] is not None else None,
            "originalOrigin": original_origin[target],
            "originalReceiptId": previous_entries.get(target, {}).get("originalReceiptId", receipt_id),
            "installedSha256": digest(payload[target])})
    receipt_path = receipt_dir / "install-receipt.json"
    receipt["state"] = "installing"
    atomic_write(receipt_path, json_bytes(receipt))
    target_dirs = []
    try:
        for target in targets:
            ensure_stopped(process_checker)
            guard_hash(game, target, before[target])
            path = within(game, target)
            mkdir_tracked(path.parent, target_dirs)
            write_file(path, payload[target])
            guard_hash(game, target, digest(payload[target]))
        pointer = within(game, BACKUP_ROOT + "/active.json")
        if (read_regular(pointer) if pointer.exists() else None) != active_raw:
            raise InstallError("Active installation changed during the transaction.")
        atomic_write(pointer, json_bytes({"receipt": str(receipt_path.relative_to(game)).replace("\\", "/")}))
        receipt["state"] = "installed"
        atomic_write(receipt_path, json_bytes(receipt))
        return receipt_path
    except BaseException as exc:
        try:
            ensure_stopped(process_checker)
            restore_before(game, receipt_dir, receipt)
            cleanup_empty(target_dirs)
        except BaseException as recovery_error:
            receipt["state"] = "recovery_required"
            receipt["failure"] = str(exc)
            receipt["recoveryFailure"] = str(recovery_error)
            atomic_write(receipt_path, json_bytes(receipt))
            raise InstallError("Installation stopped. Close MGSV and use restore --receipt " + str(receipt_path)
                + ". Changed files were preserved: " + str(recovery_error)) from exc
        raise InstallError("Installation failed; planned targets restored. Receipt: " + str(receipt_path)) from exc

@serialized
def uninstall(game_dir: str | Path, *, receipt_path: str | Path | None = None, process_checker=game_running, write_file=atomic_write) -> Path:
    game, _ = validate_game(game_dir, require_framework=False)
    ensure_stopped(process_checker)
    active_path, receipt, _ = active_receipt(game)
    if active_path is None:
        raise InstallError("No active Immersive Mother Base installation was recorded.")
    if receipt_path and Path(os.path.abspath(receipt_path)) != active_path:
        raise InstallError("Uninstall accepts only the active receipt; older versions are historical backups.")
    actions = []
    for entry in receipt["files"]:
        guard_hash(game, entry["target"], entry["installedSha256"])
        data = backup_data(active_path.parent, "original", entry["target"], entry["originalSha256"])
        actions.append((entry, data))
    for entry, _ in actions:
        path = within(active_path.parent, "uninstall-before/" + entry["target"])
        mkdir_tracked(path.parent, [])
        atomic_write(path, read_regular(within(game, entry["target"])))
    receipt["state"] = "uninstalling"
    atomic_write(active_path, json_bytes(receipt))
    try:
        for entry, data in actions:
            ensure_stopped(process_checker)
            guard_hash(game, entry["target"], entry["installedSha256"])
            path = within(game, entry["target"])
            if data is None:
                path.unlink()
            else:
                write_file(path, data)
            guard_hash(game, entry["target"], entry["originalSha256"])
        within(game, BACKUP_ROOT + "/active.json").unlink()
        receipt["state"] = "uninstalled"
        atomic_write(active_path, json_bytes(receipt))
        return active_path
    except BaseException as exc:
        try:
            ensure_stopped(process_checker)
            restore_before(game, active_path.parent, receipt, restoring_uninstall=True)
        except BaseException as recovery_error:
            receipt["state"] = "uninstall_recovery_required"
            receipt["recoveryFailure"] = str(recovery_error)
            atomic_write(active_path, json_bytes(receipt))
            raise InstallError("Restore interrupted; use restore --receipt " + str(active_path)) from exc
        raise InstallError("Uninstall failed; installed files restored. Receipt: " + str(active_path)) from exc

@serialized
def recover(game_dir: str | Path, receipt_path: str | Path, *, process_checker=game_running) -> Path:
    game, _ = validate_game(game_dir, require_framework=False)
    ensure_stopped(process_checker)
    path = Path(os.path.abspath(receipt_path))
    receipt = load_receipt(game, path)
    state = receipt.get("state")
    if state == "installed":
        return uninstall(game, receipt_path=path, process_checker=process_checker)
    if state not in ("installing", "recovery_required", "uninstalling", "uninstall_recovery_required"):
        raise InstallError("Receipt does not describe an active or interrupted transaction.")
    restore_before(game, path.parent, receipt, restoring_uninstall=state in ("uninstalling", "uninstall_recovery_required"))
    return path

def choose_game() -> str:
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        chosen = filedialog.askdirectory(title="Select your existing MGS_TPP folder (contains mgsvtpp.exe)", mustexist=True)
        root.destroy()
    except Exception as exc:
        raise InstallError("Folder picker unavailable. Run with --game-dir followed by the game folder.") from exc
    if not chosen:
        raise InstallError("Cancelled; no files changed.")
    return chosen

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "install", "uninstall", "restore"))
    parser.add_argument("--game-dir", help="Existing MGS_TPP folder; otherwise opens a folder picker")
    parser.add_argument("--receipt", help="Active or interrupted install-receipt.json for restore")
    parser.add_argument("--package-root", default=str(Path(__file__).absolute().parent.parent))
    args = parser.parse_args(argv)
    try:
        if sys.version_info < (3, 10):
            raise InstallError("Install Python 3.10 or later first.")
        game_dir = args.game_dir or choose_game()
        if args.mode in ("check", "install"):
            _, manifest, payload = load_package(args.package_root)
            game, findings = validate_game(game_dir)
            print("Immersive Mother Base " + manifest["version"] + " - installable alpha; native gameplay acceptance pending.")
            print("Supported source scope: " + "; ".join(manifest.get("supportedFeatures", [])))
            print("Unavailable/unaccepted: " + "; ".join(manifest.get("unavailableFeatures", [])))
            print("\n".join(findings))
            if args.mode == "check":
                print("Verified " + str(len(payload)) + " core files. MGSV running: " + str(game_running()))
            else:
                print("Installed; keep this restore receipt: " + str(install(game, args.package_root)))
        elif args.mode == "uninstall":
            print("Original owned files restored; private data and backups retained: " + str(uninstall(game_dir, receipt_path=args.receipt)))
        else:
            if not args.receipt:
                raise InstallError("restore requires --receipt pointing to this game's install-receipt.json.")
            print("Restoration/recovery completed: " + str(recover(game_dir, args.receipt)))
        print("Game not launched. Archives, third-party settings and game saves not changed.")
        return 0
    except (InstallError, OSError, UnicodeError) as exc:
        print("Could not complete: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())