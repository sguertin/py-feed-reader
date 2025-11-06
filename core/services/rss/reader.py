from typing import Any
import feedparser as fp
from http import HTTPStatus as http
from core.constants.common import EMPTY_STRING
from core.exceptions.feed import FeedNotFoundError
from core.interfaces.feed import IFeedService
from core.interfaces.rss import IRssStorageService
from core.models.feed import Feed, FeedItem
from core.utilities.datetime import DateTime


ID = "id"
ENTRIES = "entries"
ETAG = "etag"
LINK = "link"
MODIFIED = "modified"
PUBLISHED = "published"
TITLE = "title"
STATUS = "status"
SUMMARY = "summary"


def create_feed_item_from_entry(entry: dict, feed_url: str) -> FeedItem:
    return FeedItem(
        id=entry[ID],
        title=entry.get(TITLE),
        summary=entry.get(SUMMARY),
        link=entry.get(LINK),
        published=DateTime.parse_timestamp(entry.get(PUBLISHED)),
        feed_url=feed_url,
        created=DateTime.now(),
    )


def create_feed_from_rss(feed: dict, feed_url: str) -> Feed:
    return Feed(
        title=feed.get(TITLE, EMPTY_STRING),
        url=feed_url,
        html_url=feed.get(LINK, EMPTY_STRING),
        category=EMPTY_STRING,
        created=DateTime.now(),
    )


class RssFeedReaderService:
    storage_service: IRssStorageService
    feed_service: IFeedService

    def __init__(self, storage_service: IRssStorageService, feed_service: IFeedService):
        self.storage_service = storage_service
        self.feed_service = feed_service

    def get_feed(self, feed_url: str) -> Feed:
        rss = fp.parse(feed_url)
        if rss.get(STATUS) == http.NOT_FOUND:
            raise FeedNotFoundError(feed_url)
        return create_feed_from_rss(rss.feed, feed_url)  # type: ignore

    def get_items(self, include_read: bool = False) -> list[FeedItem]:
        stored_items = [item for item in self.storage_service.get_stored_items()]
        stored_ids = [item.id for item in stored_items]
        for feed in self.feed_service.feeds:
            stored_items += [
                item
                for item in self._get_feed_items(feed)
                if item.id not in stored_ids and (item.read == False or include_read)
            ]
        return []

    def get_feed_items(self, feed: Feed, include_read: bool = False) -> list[FeedItem]:
        stored_items = [
            item
            for item in self.storage_service.get_stored_items()
            if item.feed_url == feed.url
        ]
        new_feed_items = self._get_feed_items(feed)
        return stored_items + [
            item
            for item in new_feed_items
            if item.id not in [existing.id for existing in stored_items]
            and (item.read == False or include_read)
        ]

    def read(self, feed: Feed) -> dict[str, Any] | None:
        rss = fp.parse(feed.url, etag=feed.etag, modified=feed.modified)
        if rss.get(STATUS) == http.NOT_FOUND:
            raise FeedNotFoundError(feed.url)
        if rss.get(STATUS) == http.NOT_MODIFIED:
            return None
        return rss

    def _get_feed_items(self, feed: Feed):
        rss = self.read(feed)
        if rss is None:
            return []
        feed.etag = rss.get(ETAG, None)  # type: ignore
        feed.modified = rss.get(MODIFIED, None)  # type: ignore
        feed.last_read = DateTime.now()
        entries: list[dict] = rss.get(ENTRIES, [])  # type: ignore
        return [create_feed_item_from_entry(entry, feed.url) for entry in entries]
