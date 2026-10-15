from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class PlatformVersion(str, Enum):
    V8_3_20 = "8.3.20"
    V8_3_21 = "8.3.21"
    V8_3_22 = "8.3.22"
    V8_3_23 = "8.3.23"
    V8_3_24 = "8.3.24"
    V8_3_25 = "8.3.25"

@dataclass
class PlatformCheck:
    current: str
    target: str

def version_tuple(v):
    return tuple(int(x) for x in v.split("."))

def is_upgrade_possible(current, target):
    return version_tuple(target) >= version_tuple(current)

def find_platform_binary(version):
    for c in Path("C:/Program Files/1cv8").glob(f"{version}*"):
        exe = c / "bin" / "1cv8.exe"
        if exe.exists():
            return str(exe)
    return None

def list_installed_platforms():
    result = []
    base = Path("C:/Program Files/1cv8")
    if not base.exists():
        return result
    for d in base.iterdir():
        if d.is_dir() and (d / "bin" / "1cv8.exe").exists():
            result.append(d.name)
    return sorted(result)
