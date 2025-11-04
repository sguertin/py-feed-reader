from datetime import datetime
import os.path
from pathlib import Path


def file_modification_date(file_path: Path) -> datetime:
    """Get the last modified date for a given file path

    Args:
        file_path (Path): the path to the file

    Returns:
        datetime: a datetime object representing the last modified date
    """    
    timestamp = os.path.getmtime(str(file_path))
    return datetime.fromtimestamp(timestamp)
