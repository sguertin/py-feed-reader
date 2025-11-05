from datetime import datetime
from pathlib import Path

from core.config.file import FileSettings
import core.utilities.file as file
import core.utilities.json as json
from core.interfaces.e_tag import IETagService


class ETagJsonFileService(IETagService):
    file_path: Path
    _etags: dict[str, str]
    last_modified: datetime | None = None

    @property
    def etags(self) -> dict[str, str]:
        self.reload_etags()
        return self._etags

    def __init__(self, settings: FileSettings):
        self.file_path = Path(settings.etag_file_path)
        self.reload_etags()

    def get_etag(self, xml_url: str) -> str | None:
        return self.etags.get(xml_url)

    def set_etag(self, xml_url: str, etag: str) -> None:
        self.reload_etags()
        self._etags[xml_url] = etag
        json.write_json_file(self.file_path, self._etags)
        self.last_modified = datetime.now()

    def reload_etags(self) -> None:
        last_modified = file.file_modification_date(self.file_path)
        if self.last_modified is None or last_modified > self.last_modified:
            self.last_modified = last_modified
            self._etags = json.read_json_file(self.file_path)
