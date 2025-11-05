from datetime import datetime
from pathlib import Path

from core.models.settings import Settings
import core.utilities.file as file
import core.utilities.json as json
from core.interfaces.e_tag import IETagService


class ETagJsonFileService(IETagService):
    file_path: Path
    _e_tags: dict[str, str]
    last_modified: datetime | None = None

    @property
    def e_tags(self) -> dict[str, str]:
        self.reload_e_tags()
        return self._e_tags

    def __init__(self, settings: Settings):
        self.file_path = Path(settings.e_tag_file_path)
        self.reload_e_tags()

    def get_e_tag(self, xml_url: str) -> str | None:
        return self.e_tags.get(xml_url)

    def set_e_tag(self, xml_url: str, e_tag: str) -> None:
        self.reload_e_tags()
        self._e_tags[xml_url] = e_tag
        json.write_json_file(self.file_path, self._e_tags)
        self.last_modified = datetime.now()

    def reload_e_tags(self) -> None:
        last_modified = file.file_modification_date(self.file_path)
        if self.last_modified is None or last_modified > self.last_modified:
            self.last_modified = last_modified
            self._e_tags = json.read_json_file(self.file_path)
