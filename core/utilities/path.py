import logging
import os
from pathlib import Path
import tempfile as temp
from constants.common import EMPTY_STRING, APPLICATION_NAME

WINDOWS: str = "nt"
POSIX: str = "posix"

TEMP_DIRECTORY = Path(temp.gettempdir())
APPDATA_ENV = "APPDATA"
LOCAL_APPDATA_ENV = "LOCALAPPDATA"

log = logging.getLogger(__name__)


class AppDataFolder:

    @staticmethod
    def get_dir_path() -> Path:
        if os.name == WINDOWS:
            dir_name = APPLICATION_NAME
            apps_dir = Path(
                os.getenv(LOCAL_APPDATA_ENV, os.getenv(APPDATA_ENV, EMPTY_STRING))
            )
        else:
            dir_name = f".{APPLICATION_NAME}"
            apps_dir = Path.home()
        app_data_dir = apps_dir / dir_name
        try:
            if not app_data_dir.exists():
                app_data_dir.mkdir()
            return app_data_dir
        except PermissionError as e:
            temp_data_dir = TEMP_DIRECTORY / dir_name
            log.warning(
                f"Failed to create app folder '{app_data_dir}', creating temp folder '{temp_data_dir}'",
                exc_info=e,
            )
            if not temp_data_dir.exists():
                temp_data_dir.mkdir()
            return temp_data_dir
