from io import StringIO
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from core.constants.common import SLASH, STR_EMPTY
from core.constants.opml import (
    OUTLINE_TAG,
    CATEGORY,
    DISABLED,
    HTML_URL,
    RSS,
    TEXT,
    TITLE,
    TYPE,
    XML_URL,
    TRUE,
    FALSE,
    DATE_CREATED,
    DATE_MODIFIED,
)
from core.exceptions.feed import DuplicateFeedError, FeedNotFoundError
from core.interfaces.common import ISave
from core.interfaces.e_tag import IETagService
from core.interfaces.feed import IFeedService
from core.models.feed import Feed
from core.models.settings import Settings
from core.utilities.datetime import utc_timestamp
from core.utilities.decorators import autosave
from core.utilities.xml import get_first_element_or_default


class OPMLFeedService(IFeedService, ISave):
    file_path: Path
    tree: ElementTree[Element[str]]
    head: Element
    body: Element
    e_tag_service: IETagService

    def __init__(self, settings: Settings, e_tag_service: IETagService):
        self.file_path = settings.opml_file_path
        self.e_tag_service = e_tag_service
        self.load(self.file_path)

    @property
    def disabled_feeds(self) -> list[Feed]:
        return [
            self.create_feed_from_outline(
                outline, self.e_tag_service.get_e_tag(outline.attrib[XML_URL])
            )
            for outline in self.body
            if disabled(outline)
        ]

    @property
    def feeds(self) -> list[Feed]:
        return [
            self.create_feed_from_outline(
                outline, self.e_tag_service.get_e_tag(outline.attrib[XML_URL])
            )
            for outline in self.body
            if not disabled(outline)
        ]

    def load(self, opml_file: Optional[Path] = None) -> None:
        if opml_file is None:
            opml_file = self.file_path
        else:
            self.file_path = opml_file
        timestamp = utc_timestamp()
        if opml_file.exists():
            self.tree = ET.parse(opml_file)
        else:
            self.tree = ET.parse(StringIO(get_empty_opml(timestamp)))
        self.head = self.tree.getroot()[0]
        self.body = self.tree.getroot()[1]
        get_first_element_or_default(
            self.head, DATE_MODIFIED, timestamp
        )  # Don't need the element, just adding them if they're not there
        get_first_element_or_default(self.head, DATE_CREATED, timestamp)

    def save(self, opml_file_path: Optional[Path] = None) -> None:
        if opml_file_path is None:
            opml_file_path = self.file_path
        else:
            self.file_path = opml_file_path
        timestamp = utc_timestamp()
        last_modified = get_first_element_or_default(self.head, DATE_MODIFIED)
        last_modified.text = timestamp
        self.tree.write(opml_file_path, encoding="UTF-8", xml_declaration=True)

    @autosave
    def add_feed(self, feed: Feed) -> None:
        if self.feed_exists(feed):
            raise DuplicateFeedError(feed.xml_url)
        elif self.disabled_feed_exists(feed):
            self.update_feed(feed)
            self.enable_feed(feed)
        else:
            self.body.append(self.create_element_from_feed(feed))

    def get_feed(self, xml_url: str) -> Feed:
        try:
            return [feed for feed in self.feeds if feed.xml_url == xml_url][0]
        except IndexError:
            raise FeedNotFoundError(xml_url)

    def get_feed_element(self, xml_url: str) -> Element:
        try:
            return [
                outline for outline in self.body if outline.attrib[XML_URL] == xml_url
            ][0]
        except IndexError:
            raise FeedNotFoundError(xml_url)

    @autosave
    def disable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.xml_url).set(DISABLED, TRUE)

    @autosave
    def enable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.xml_url).set(DISABLED, FALSE)

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
        feed_element = self.get_feed_element(feed_info.xml_url)
        feed_element.set(TEXT, feed_info.title)
        feed_element.set(TITLE, feed_info.title)
        feed_element.set(CATEGORY, f"/{feed_info.category}")
        feed_element.set(XML_URL, feed_info.xml_url)
        feed_element.set(HTML_URL, feed_info.html_url)

    @staticmethod
    def create_element_from_feed(feed: Feed) -> Element:
        return Element(
            OUTLINE_TAG,
            attrib={
                TEXT: feed.title,
                TITLE: feed.title,
                TYPE: RSS,
                CATEGORY: f"{SLASH}{feed.category}",
                XML_URL: feed.xml_url,
                HTML_URL: feed.html_url,
                DISABLED: FALSE,
            },
        )

    @staticmethod
    def create_feed_from_outline(outline: Element, e_tag: str | None = None) -> Feed:
        entry = outline.attrib
        return Feed(
            title=entry.get(TITLE, STR_EMPTY),
            xml_url=entry.get(XML_URL, STR_EMPTY),
            html_url=entry.get(HTML_URL, STR_EMPTY),
            category=entry.get(CATEGORY, STR_EMPTY).replace(SLASH, STR_EMPTY),
            e_tag=e_tag,
        )


# def get_first_element_or_default(
#     parent: Element, tag: str, text: str= STR_EMPTY, attrib: dict[str, str] | None = None
# ):
#     if attrib is None:
#         attrib = {}
#     elements = [e for e in parent if e.tag == tag]
#     if not any(elements):
#         default_element = SubElement(parent, tag=tag, attrib=attrib, text=text)
#         return default_element
#     else:
#         return elements[0]


def get_empty_opml(timestamp: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>RSS Feeds</title>
        <dateCreated>{timestamp}</dateCreated>
        <dateModified>{timestamp}</dateModified>
        <ownerName></ownerName>
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
    return outline.attrib.get(DISABLED, FALSE).lower() == TRUE
