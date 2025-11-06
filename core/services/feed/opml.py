from io import StringIO
import logging
from logging import Logger
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from core.config.common import config
from core.config.file import FileStorageSettings
import core.constants.common as Constants
import core.constants.opml as OPML
from core.exceptions.feed import DuplicateFeedError, FeedNotFoundError
from core.interfaces.common import ISave
from core.interfaces.feed import IFeedService
from core.models.feed import Feed
from core.utilities.datetime import DateTime
from core.utilities.decorators import autosave
from core.utilities.xml import get_first_element_or_default


class OPMLFeedService(IFeedService, ISave):
    tree: ElementTree[Element[str]]
    head: Element
    body: Element
    log: Logger

    def __init__(self, settings: FileStorageSettings | None = None):
        self.log = logging.getLogger(OPMLFeedService.__name__)
        if settings is not None:
            self.settings = settings
        self.load(self.file_path)

    @property
    def settings(self) -> FileStorageSettings:
        return config.get_config(FileStorageSettings)

    @settings.setter
    def settings(self, settings: FileStorageSettings) -> None:
        config.set_config(FileStorageSettings, settings)

    @property
    def file_path(self) -> Path:
        return self.settings.opml_file_path

    @file_path.setter
    def file_path(self, file_path: Path):
        self.settings.opml_file_path = file_path

    @property
    def disabled_feeds(self) -> list[Feed]:
        return [
            self.create_feed_from_outline(outline)
            for outline in self.body
            if disabled(outline)
        ]

    @property
    def feeds(self) -> list[Feed]:
        return [
            self.create_feed_from_outline(outline)
            for outline in self.body
            if not disabled(outline)
        ]

    def load_from_string(self, opml_text: str) -> None:
        self.tree = ET.parse(StringIO(opml_text))
        self.extract_elements(DateTime.utcnow_timestamp())

    def load(self, opml_file: Optional[Path] = None) -> None:
        timestamp = DateTime.utcnow_timestamp()
        if opml_file is None:
            opml_file = self.file_path
        else:
            self.file_path = opml_file
        file_path_repr = opml_file.as_posix()
        if opml_file.exists():
            self.log.debug(f"'%s' exists", file_path_repr)
            self.tree = ET.parse(opml_file)
            self.extract_elements(timestamp)
        else:
            self.log.warning(
                f"'%s' does not exist, creating empty file", file_path_repr
            )
            empty_opml = get_empty_opml(timestamp)
            self.load_from_string(empty_opml)

    def save(self, opml_file: Optional[Path] = None) -> None:
        if opml_file is None:
            opml_file = self.file_path
        else:
            self.file_path = opml_file
        timestamp = DateTime.utcnow_timestamp()
        last_modified = get_first_element_or_default(self.head, OPML.DATE_MODIFIED)
        last_modified.text = timestamp
        self.tree.write(opml_file, encoding="UTF-8", xml_declaration=True)

    def extract_elements(self, timestamp) -> None:
        self.head = self.tree.getroot()[0]
        self.body = self.tree.getroot()[1]
        # Don't need the elements, just adding them if they're not there
        get_first_element_or_default(self.head, OPML.DATE_MODIFIED, timestamp)
        get_first_element_or_default(self.head, OPML.DATE_CREATED, timestamp)

    @autosave
    def add_feed(self, feed: Feed) -> None:
        if self.feed_exists(feed):
            raise DuplicateFeedError(feed.url)
        elif self.disabled_feed_exists(feed):
            self.update_feed(feed)
            self.enable_feed(feed)
        else:
            self.body.append(self.create_element_from_feed(feed))

    def get_feed(self, feed_url: str) -> Feed:
        try:
            return [feed for feed in self.feeds if feed.url == feed_url][0]
        except IndexError as e:
            raise FeedNotFoundError(feed_url).with_traceback(e.__traceback__)

    def get_feed_element(self, xml_url: str) -> Element:
        try:
            return [
                outline
                for outline in self.body
                if outline.attrib[OPML.XML_URL] == xml_url
            ][0]
        except IndexError as e:
            self.log.warning(str(e), exc_info=e)
            raise FeedNotFoundError(xml_url).with_traceback(e.__traceback__)

    @autosave
    def disable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.url).set(OPML.DISABLED, OPML.TRUE)

    @autosave
    def enable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.url).set(OPML.DISABLED, OPML.FALSE)

    def feed_exists(self, feed: Feed) -> bool:
        return any(
            [existing_feed for existing_feed in self.feeds if existing_feed == feed]
        )

    def disabled_feed_exists(self, feed: Feed) -> bool:
        return any(
            [
                existing_feed
                for existing_feed in self.disabled_feeds
                if existing_feed == feed
            ]
        )

    @autosave
    def update_feed(self, feed_info: Feed) -> None:
        feed_element = self.get_feed_element(feed_info.url)
        feed_element.set(OPML.TEXT, feed_info.title)
        feed_element.set(OPML.TITLE, feed_info.title)
        feed_element.set(OPML.CATEGORY, f"/{feed_info.category}")
        feed_element.set(OPML.XML_URL, feed_info.url)
        feed_element.set(OPML.HTML_URL, feed_info.html_url)

    @staticmethod
    def create_element_from_feed(feed: Feed) -> Element:
        return Element(
            OPML.OUTLINE_TAG,
            attrib={
                OPML.TEXT: feed.title,
                OPML.TITLE: feed.title,
                OPML.TYPE: OPML.RSS,
                OPML.CATEGORY: f"{Constants.SLASH}{feed.category}",
                OPML.XML_URL: feed.url,
                OPML.HTML_URL: feed.html_url,
                OPML.DISABLED: OPML.FALSE,
            },
        )

    @staticmethod
    def create_feed_from_outline(outline: Element) -> Feed:
        entry = outline.attrib
        return Feed(
            title=entry.get(OPML.TITLE, Constants.EMPTY_STRING),
            url=entry.get(OPML.XML_URL, Constants.EMPTY_STRING),
            html_url=entry.get(OPML.HTML_URL, Constants.EMPTY_STRING),
            category=entry.get(OPML.CATEGORY, Constants.EMPTY_STRING).replace(
                Constants.SLASH, Constants.EMPTY_STRING
            ),
        )


def get_empty_opml(
    timestamp: str, title: str = "RSS Feeds", owner_name: str = Constants.EMPTY_STRING
) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>{title}</title>
        <dateCreated>{timestamp}</dateCreated>
        <dateModified>{timestamp}</dateModified>
        <ownerName>{owner_name}</ownerName>
        <docs>http://opml.org/spec2.opml</docs>
    </head>
    <body>

    </body>
</opml>
"""


def disabled(outline: Element) -> bool:
    """
    Checks if the element has been "commented out", i.e. disabled
    Args:
        outline (Element): outline xml element

    Returns:
        bool: True if the element is disabled
    """
    return outline.attrib.get(OPML.DISABLED, OPML.FALSE).lower() == OPML.TRUE
