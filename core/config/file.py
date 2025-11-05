from abc import ABC, ABCMeta
from dataclasses import dataclass
from pathlib import Path

from core.config.common import Configuration
from core.mixins.dataclasses_json import CamelCaseJsonMixin
from core.interfaces.common import ISave
from core.utilities.path import AppDataFolder

APPLICATION_DIRECTORY = AppDataFolder.get_dir_path()
SETTINGS_FILE_NAME: str = "file-settings.json"
OPML_FILE_NAME: str = "feeds.opml"
ETAGS_FILE_NAME: str = "etags.json"
ITEM_STORAGE_NAME: str = "feed-items.json"

DEFAULT_SETTINGS_PATH: Path = APPLICATION_DIRECTORY / SETTINGS_FILE_NAME
DEFAULT_OPML_PATH: Path = APPLICATION_DIRECTORY / OPML_FILE_NAME
DEFAULT_ETAG_PATH: Path = APPLICATION_DIRECTORY / ETAGS_FILE_NAME
DEFAULT_ITEM_STORAGE_PATH: Path = APPLICATION_DIRECTORY / ITEM_STORAGE_NAME


@dataclass(slots=True)
class FileSettings(CamelCaseJsonMixin, ISave):

    @property
    def opml_file_path(self) -> Path:
        """the path to the opml file"""
        return Path(self.opml_file)

    @opml_file_path.setter
    def opml_file_path(self, opml_file_path: str | Path):
        self.opml_file = str(opml_file_path)

    @property
    def etag_file_path(self) -> Path:
        """the path to the etags file"""
        return Path(self.etag_file)

    @etag_file_path.setter
    def etag_file_path(self, e_tag_file_path: str | Path) -> None:
        self.etag_file = str(e_tag_file_path)

    @property
    def storage_file_path(self) -> Path:
        """the path to the opml file"""
        return Path(self.storage_file)

    @storage_file_path.setter
    def storage_file_path(self, storage_file: str | Path):
        self.storage_file = str(storage_file)

    @property
    def file_path(self) -> Path:
        """the path to this file"""
        return Path(self.file)

    @file_path.setter
    def file_path(self, file_path: str | Path) -> None:
        self.file = str(file_path)

    file: str = str(DEFAULT_SETTINGS_PATH)
    opml_file: str = str(DEFAULT_OPML_PATH)
    etag_file: str = str(DEFAULT_ETAG_PATH)
    storage_file: str = str(DEFAULT_ITEM_STORAGE_PATH)

    @classmethod
    def load(cls, path: Path = DEFAULT_SETTINGS_PATH) -> FileSettings:  # type: ignore
        if not path.exists():
            result = cls(
                str(path),
            )
            result.save()
        else:
            result = FileSettings.from_json(path.read_text())
        return result

    def save(self) -> None:
        self.file_path.write_text(self.to_json())


class FileConfiguration(ABC, metaclass=ABCMeta):

    @staticmethod
    def set_default_file_config():
        config = Configuration()
        config.set_config(
            FileSettings,
            FileSettings(),
        )
