import os
from pathlib import Path

WINDOWS: str = "nt"
POSIX: str = "posix"


def get_apps_directory() -> Path:
    if os.name == WINDOWS:
        result = Path(os.getenv("LOCALAPPDATA", ""))
    else:
        result = Path.home()
    return result
