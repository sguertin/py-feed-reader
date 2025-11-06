from pathlib import Path

from core.config.common import ConfigurationRoot
from core.config.file import FileStorageSettings
from core.interfaces.common import ISave
from core.interfaces.rss import IRssStorageService
from core.models.feed import FeedItem
from core.utilities.decorators import autosave
from core.utilities.file import file_modification_date
from core.utilities.path import AppDataFolder
from core.utilities.datetime import DateTime

STORAGE_FILE_NAME: str = "rss-storage.json"
STORAGE_FILE = AppDataFolder.get_dir_path() / STORAGE_FILE_NAME

config = ConfigurationRoot()


class RssReaderStorage(ISave, IRssStorageService):
    last_read: DateTime
    cache: list[FeedItem]

    @property
    def settings(self) -> FileStorageSettings:
        return config.get_config(FileStorageSettings)

    @property
    def file_path(self) -> Path:
        return self.settings.storage_file_path

    def __init__(self):
        self.load()

    def get_last_modified(self) -> DateTime:
        return file_modification_date(STORAGE_FILE)

    def load(self) -> None:
        if not self.file_path.exists():
            self.cache = []
            self.save()
            self.last_read = DateTime.now()
        else:
            self.last_read = self.get_last_modified()
            self.cache = FeedItem.schema().loads(self.file_path.read_text())

    def get_stored_items(self) -> list[FeedItem]:
        if not self.file_path.exists():
            self.cache = []
            return self.cache
        if self.get_last_modified() > self.last_read:
            return FeedItem.schema().loads(self.file_path.read_text())
        else:
            return self.cache

    @autosave
    def store_feed_item(self, item: FeedItem) -> None:
        self.store_feed_items([item])

    @autosave
    def store_feed_items(self, items: list[FeedItem]) -> None:
        stored_items = self.get_stored_items()
        self.cache = stored_items + [
            item
            for item in items
            if item.id not in [stored_item.id for stored_item in stored_items]
        ]

    def save(self) -> None:
        self.file_path.write_text(FeedItem.schema().dumps(self.cache))
