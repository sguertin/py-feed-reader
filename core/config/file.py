from dataclasses import dataclass

import logging
from pathlib import Path
import tempfile as temp


from core.config.dataclasses_json import CamelCaseJsonMixin
from core.interfaces.common import ISave
import core.utilities.path as path

temp_directory = temp.gettempdir()
TEMP_DIRECTORY = Path(temp_directory) / "settings.json"
APP_DIRECTORY_NAME: str = ".py-feed-reader"
SETTINGS_FILE_NAME: str = "settings.json"
OPML_FILE_NAME: str = "feeds.opml"
ETAGS_FILE_NAME: str = "etags.json"
ITEM_STORAGE_NAME: str = "feed-items.json"
APPLICATION_DIRECTORY: Path = path.get_apps_directory() / APP_DIRECTORY_NAME
SETTINGS_FILE_PATH: Path = APPLICATION_DIRECTORY / SETTINGS_FILE_NAME
DEFAULT_OPML_PATH: Path = APPLICATION_DIRECTORY / OPML_FILE_NAME
DEFAULT_ETAG_PATH: Path = APPLICATION_DIRECTORY / ETAGS_FILE_NAME
DEFAULT_ITEM_STORAGE_PATH: Path = APPLICATION_DIRECTORY / ITEM_STORAGE_NAME


@dataclass
class FileSettings(CamelCaseJsonMixin, ISave):

    @property
    def opml_file_path(self) -> Path:
        """the path to the opml file"""
        return Path(self._opml_file_path)

    @opml_file_path.setter
    def opml_file_path(self, opml_file_path: str | Path):
        self._opml_file_path = str(opml_file_path)

    @property
    def e_tag_file_path(self) -> Path:
        """the path to the e-tags file"""
        return Path(self._e_tag_file_path)

    @e_tag_file_path.setter
    def e_tag_file_path(self, e_tag_file_path: str | Path) -> None:
        self._e_tag_file_path = str(e_tag_file_path)

    @property
    def file_path(self) -> Path:
        return Path(self._file_path)

    @file_path.setter
    def file_path(self, file_path: str | Path) -> None:
        self._file_path = str(file_path)

    _opml_file_path: str
    _e_tag_file_path: str
    _file_path: str

    def __init__(
        self,
        opml_file_path: str = str(DEFAULT_OPML_PATH),
        e_tag_file_path: str = str(DEFAULT_ETAG_PATH),
        file_path: str = str(SETTINGS_FILE_PATH),
    ):
        self._opml_file_path = opml_file_path
        self._e_tag_file_path = e_tag_file_path
        self._file_path = file_path
        self.log = logging.getLogger(__name__)

    @classmethod
    def load(cls) -> FileSettings:  # type: ignore
        if not SETTINGS_FILE_PATH.exists():
            return cls()
        return FileSettings.from_json(SETTINGS_FILE_PATH.read_text())

    def save(self) -> None:
        """Save the settings to a json file located file_path, if that fails, it will write to temp directory"""
        try:
            self.file_path.write_text(self.to_json())
        except Exception as e:
            message = f"Failed to create {APPLICATION_DIRECTORY}, creating temp files in {temp_directory}!"
            e.add_note(message)
            self.log.error(message, exc_info=e)
            TEMP_DIRECTORY.write_text(self.to_json())
