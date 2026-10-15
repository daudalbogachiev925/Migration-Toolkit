import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def backup_ib(ib_path, backup_folder="backups"):
    Path(backup_folder).mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    target = Path(backup_folder) / f"ib_{ts}.dt"

    platform = find_platform()
    cmd = [
        platform, "DESIGNER",
        "/F", ib_path,
        "/DumpIB", str(target),
        "/Out", str(Path(backup_folder) / f"dump_{ts}.log"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Backup failed: {result.stderr}")
    return target

def restore_ib(ib_path, backup_file):
    platform = find_platform()
    cmd = [
        platform, "DESIGNER",
        "/F", ib_path,
        "/RestoreIB", backup_file,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Restore failed: {result.stderr}")
    return True

def find_platform(version="8.3"):
    for c in Path("C:/Program Files/1cv8").glob(f"{version}*"):
        exe = c / "bin" / "1cv8.exe"
        if exe.exists():
            return str(exe)
    raise FileNotFoundError("1cv8.exe not found")
