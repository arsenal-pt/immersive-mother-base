"""Read-only MGSV staff codenames, from the user's installed English language data.
Supported native signatures: day3900. No injection, process writes, or memory scans.
"""
from pathlib import Path
import ctypes
from ctypes import wintypes
import json
import struct
import threading
import time
import xml.etree.ElementTree as ET

GET_QUARK = (0x140BFF050, bytes.fromhex("4883ec28e847ffffff488b40084883c428c3"))
STAFF_NAME_KEY = (0x140F97A70, bytes.fromhex("48896c24104889742418574883ec208bc2410fb6f98bf2c1e807488be9243f3c3f754c4584c9751a48b8989f16bfa0b8"))
FACE_GENDER = (0x1409F2790, bytes.fromhex("4c8bc181fa84030000720332c0c38bc2488d0c80498b80880000008b44c81cc1e81e2401c3"))

def xorshift32(x):
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= x >> 7
    x ^= (x << 5) & 0xFFFFFFFF
    return x & 0xFFFFFFFF

def valid_label(value):
    return isinstance(value, str) and 0 < len(value) <= 160 and not any(ord(c) < 32 for c in value)

def resolve_staff_name(reader, staff, faces, sid, named, hashes):
    """Use native StaffController fields; never guess from faces or roster order."""
    if not 0 < sid < 2**53:
        raise ValueError("invalid 53-bit staff identity")
    head, seed = sid & 0xFFFFFFFF, (sid >> 21) & 0xFFFFF800
    if ((head >> 7) & 63) == 63:
        unique_type = seed >> 24
        key = reader.u64(staff + 0x5788 + (unique_type if unique_type < 254 else 0) * 32)
        result = hashes.get(key & 0xFFFFFFFF)
    else:
        face = (head >> 20) & 1023
        female = (reader.u32(faces + face * 40 + 28) >> 30) & 1 if face < 900 else 0
        first = xorshift32(seed ^ (seed >> 11))
        last = xorshift32(first)
        gender = "f" if female else "m"
        a = named.get(f"staff_1_{gender}_{first % 78:03}")
        b = named.get(f"staff_2_{gender}_{last % 60:03}")
        result = f"{a} {b}" if a and b else None
    return result.strip() if valid_label(result) else None

def validate_native_signatures(reader):
    for address, expected in (GET_QUARK, STAFF_NAME_KEY, FACE_GENDER):
        if reader.read(address, len(expected)) != expected:
            raise ValueError("unsupported native build: staff-name signature differs")

class ProcessEntry(ctypes.Structure):
    _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
                ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD), ("szExeFile", wintypes.WCHAR * 260)]

class ReadOnlyGame:
    def __init__(self, game, resolve_native=True):
        game = Path(game).resolve()
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        k = self.k
        k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k.Process32FirstW.argtypes = k.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
        k.Process32FirstW.restype = k.Process32NextW.restype = wintypes.BOOL
        k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        k.OpenProcess.restype = wintypes.HANDLE
        k.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
        k.ReadProcessMemory.restype = wintypes.BOOL
        k.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        k.QueryFullProcessImageNameW.restype = wintypes.BOOL
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        self.handle = None
        snapshot = k.CreateToolhelp32Snapshot(2, 0)
        if snapshot in (None, ctypes.c_void_p(-1).value):
            raise OSError("cannot enumerate the game process")
        try:
            e = ProcessEntry()
            e.dwSize = ctypes.sizeof(e)
            found = k.Process32FirstW(snapshot, ctypes.byref(e))
            while found:
                if e.szExeFile.casefold() == game.name.casefold():
                    h = k.OpenProcess(0x410, False, e.th32ProcessID)
                    if h:
                        path, size = ctypes.create_unicode_buffer(32768), wintypes.DWORD(32768)
                        if k.QueryFullProcessImageNameW(h, 0, path, ctypes.byref(size)) and Path(path.value).resolve() == game.resolve():
                            self.handle, self.pid = h, e.th32ProcessID
                            break
                        k.CloseHandle(h)
                found = k.Process32NextW(snapshot, ctypes.byref(e))
        finally:
            k.CloseHandle(snapshot)
        if not self.handle:
            raise ProcessLookupError("game closed")
        if not resolve_native:
            return
        try:
            validate_native_signatures(self)
            q = self.u64(0x142C3A8A0)
            systems = self.u64(self.u64(q + 8) + 0x98)
            self.staff = self.u64(self.u64(systems + 0x110) + 0xAC0)
            self.faces = self.u64(self.u64(systems + 0x2D8) + 8 + 0x88)
        except Exception:
            self.close()
            raise

    def read(self, address, length):
        if not 0x10000 <= address < 0x7FFFFFFFFFFF or not 0 < length <= 64:
            raise ValueError("out-of-range native read")
        buf, got = ctypes.create_string_buffer(length), ctypes.c_size_t()
        if not self.k.ReadProcessMemory(self.handle, address, buf, length, ctypes.byref(got)) or got.value != length:
            raise OSError("staff-name memory is not available")
        return buf.raw

    def u64(self, address):
        return struct.unpack("<Q", self.read(address, 8))[0]

    def u32(self, address):
        return struct.unpack("<I", self.read(address, 4))[0]

    def close(self):
        if self.handle:
            self.k.CloseHandle(self.handle)
            self.handle = None

class NameService:
    """Optional verified enrichment; feed labels remain the default."""
    def __init__(self, game=None, resource=None, enabled=False):
        self.game, self.enabled = game, enabled
        self.names, self.named, self.hashes = {}, {}, {}
        self.lock, self.next_check = threading.Lock(), 0
        self.status = "labels supplied by game feed; native name lookup disabled"
        self.pid, self.language_error = None, None
        if enabled:
            try:
                if not game or not resource:
                    raise ValueError("explicit executable and owned name catalogue required")
                resource = Path(resource)
                entries = ET.parse(resource / "lang_default_data_eng_fpk/Assets/tpp/lang/ui/mb_staff_name.eng.lng2.xml").findall(".//Entry")
                self.named = {e.attrib["LangId"]: e.attrib["Value"] for e in entries if "LangId" in e.attrib}
                entries = ET.parse(resource / "mb_staff_name.hashes.xml").findall(".//Entry")
                self.hashes = {int(e.attrib["Key"]): e.attrib["Value"] for e in entries}
            except (OSError, ET.ParseError, KeyError, ValueError) as exc:
                self.language_error = "owned name catalogue unavailable: " + str(exc)

    def enrich(self, status):
        actors = status.get("actors", [])
        with self.lock:
            if self.enabled and time.monotonic() >= self.next_check:
                self.next_check = time.monotonic() + 10
                reader = None
                try:
                    if self.language_error:
                        raise ValueError(self.language_error)
                    reader = ReadOnlyGame(self.game)
                    if self.pid != reader.pid:
                        self.names.clear()
                    self.pid = reader.pid
                    for actor in actors:
                        identity = str(actor.get("name", ""))
                        if identity.startswith("mb_staff_") and identity[9:].isdecimal():
                            value = resolve_staff_name(reader, reader.staff, reader.faces,
                                                       int(identity[9:]), self.named, self.hashes)
                            if value:
                                self.names[identity[9:]] = value
                    self.status = "native codenames verified against day3900 signatures"
                except (OSError, ValueError, AttributeError) as exc:
                    self.pid, self.names = None, {}
                    self.status = "feed labels retained; " + str(exc)
                finally:
                    if reader:
                        reader.close()
            count = 0
            for actor in actors:
                identity = str(actor.get("name", ""))
                value = self.names.get(identity[9:]) if identity.startswith("mb_staff_") else None
                if value:
                    actor["label"] = actor["codeName"] = value
                    actor["nameSource"] = "verified native codename + locally owned language data"
                    person = status.get("hierarchy", {}).get("people", {}).get(identity)
                    if person:
                        person["label"] = value
                    count += 1
            status["nameResolution"] = {"named": count, "registered": len(actors),
                                        "status": self.status, "pid": self.pid, "pollSeconds": 10}
        return status
