from dataclasses import dataclass
from pathlib import Path

from core.mixins.dataclasses_json import CamelCaseJsonMixin
from core.utilities.path import AppDataFolder

APPLICATION_DIRECTORY = AppDataFolder.get_dir_path()
SETTINGS_FILE_NAME: str = "file-settings.json"
ITEM_STORAGE_NAME: str = "feed-items.json"
OPML_FILE_NAME: str = "feeds.opml"

DEFAULT_SETTINGS_PATH: Path = APPLICATION_DIRECTORY / SETTINGS_FILE_NAME
DEFAULT_ITEM_STORAGE_PATH: Path = APPLICATION_DIRECTORY / ITEM_STORAGE_NAME
DEFAULT_OPML_PATH: Path = APPLICATION_DIRECTORY / OPML_FILE_NAME


@dataclass(slots=True)
class FileStorageSettings(CamelCaseJsonMixin):

    @property
    def storage_file_path(self) -> Path:
        """the path to the opml file"""
        return Path(self.storage_file)

    @storage_file_path.setter
    def storage_file_path(self, storage_file: Path | str):
        self.storage_file = str(storage_file)

    @property
    def file_path(self) -> Path:
        """the path to this file"""
        return Path(self.file)

    @file_path.setter
    def file_path(self, file_path: str | Path) -> None:
        self.file = str(file_path)

    @property
    def opml_file_path(self) -> Path:
        """the path to the opml file"""
        return Path(self.opml_file)

    @opml_file_path.setter
    def opml_file_path(self, opml_file_path: str | Path):
        self.opml_file = str(opml_file_path)

    file: str = str(DEFAULT_SETTINGS_PATH)
    storage_file: str = str(DEFAULT_ITEM_STORAGE_PATH)
    opml_file: str = str(DEFAULT_OPML_PATH)

    def __repr__(self) -> str:
        return f"FileStorageSettings(file_path={self.file_path.as_posix()},storage_file_path={self.storage_file_path.as_posix()},opml_file_path={self.opml_file_path.as_posix()})"
