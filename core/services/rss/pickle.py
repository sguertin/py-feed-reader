from pathlib import Path
import pickle

from core.config.common import ConfigurationRoot
from core.config.file import FileStorageSettings
from core.interfaces.common import ISave
from core.interfaces.rss import IRssStorageService
from core.models.feed import FeedItem
from core.utilities.decorators import autosave
from core.utilities.list import first

config = ConfigurationRoot()


class PickleRssStorageService(IRssStorageService, ISave):
    cache: list[FeedItem]

    @property
    def settings(self) -> FileStorageSettings:
        return config.get_config(FileStorageSettings)

    @property
    def file_path(self) -> Path:
        return self.settings.storage_file_path

    def __init__(self):
        self.load()

    def get_stored_items(self) -> list[FeedItem]:
        if not self.file_path.exists():
            self.cache = []
        else:
            self.cache = pickle.loads(self.file_path.read_bytes(), encoding="UTF-8")
        return self.cache

    @autosave
    def update_feed_item(self, item: FeedItem) -> None:
        cached_item = first([i for i in self.cache if i.id == item.id])
        if cached_item is None:
            self.store_feed_item(item)
        else:
            cached_item.update(item)

    @autosave
    def store_feed_item(self, item: FeedItem) -> None:
        self.store_feed_items([item])

    @autosave
    def store_feed_items(self, items: list[FeedItem]) -> None:
        self.cache = self.cache + [
            item
            for item in items
            if item.id not in [stored_item.id for stored_item in self.cache]
        ]

    def save(self) -> None:
        self.file_path.write_bytes(pickle.dumps(self.cache))

    def load(self) -> list[FeedItem]:
        self.cache = pickle.loads(self.file_path.read_bytes(), encoding="UTF-8")
        return self.cache
