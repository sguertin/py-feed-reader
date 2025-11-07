from dataclasses import dataclass

from core.mixins.dataclasses_json import CamelCaseJsonMixin
from core.constants.common import EMPTY_STRING
from core.utilities.datetime import DateTime


@dataclass(slots=True)
class Feed(CamelCaseJsonMixin):
    title: str
    url: str
    html_url: str
    category: str
    favicon: str = EMPTY_STRING
    image: str | None = None
    etag: str | None = None
    modified: str | None = None
    last_read: DateTime | None = None
    created: DateTime | None = None

    def __eq__(self, other: Feed) -> bool:
        return self.url == other.url


@dataclass(slots=True)
class FeedItem(CamelCaseJsonMixin):
    id: str
    title: str | None = None
    summary: str | None = None
    images: list[str] | None = None
    link: str | None = None
    published: DateTime | None = None
    feed_url: str = EMPTY_STRING
    read: bool = False
    created: DateTime | None = None

    def __eq__(self, other: FeedItem) -> bool:
        return self.id == other.id

    def update(self, other: FeedItem) -> None:
        self.title = other.title
        self.summary = other.summary
        self.images = other.images
        self.link = other.link
        self.published = other.published
        self.feed_url = other.feed_url
        self.read = other.read
        self.created = other.created
