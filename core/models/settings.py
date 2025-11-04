from dataclasses import dataclass
from pathlib import Path
import core.utilities.json as json

HOME = Path.home()
SETTINGS_DIRECTORY = HOME / "py-feed-reader"
SETTINGS_FILE_PATH = SETTINGS_DIRECTORY / "settings.json"
DEFAULT_OPML_PATH = SETTINGS_DIRECTORY / "feeds.opml"
DEFAULT_ETAG_PATH = SETTINGS_DIRECTORY / "etags.json"


@dataclass
class Settings:
    opml_file_path: str = str(DEFAULT_OPML_PATH)
    e_tag_file_path: str = str(DEFAULT_ETAG_PATH)

    @classmethod
    def load(cls) -> Settings:
        settings_dict = json.read_json_file(SETTINGS_FILE_PATH)
        return cls(
            settings_dict.get("opml_file_path", str(DEFAULT_OPML_PATH)),
            settings_dict.get("e_tag_file_path", str(DEFAULT_ETAG_PATH)),
        )

    def save(self):
        json.write_json_file(SETTINGS_FILE_PATH, self.__dict__)
