from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Optional
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from core.exceptions.opml import DuplicateFeedError, FeedNotFoundError
from core.models.opml import Feed
from core.models.settings import Settings
from core.utilities.file import file_modification_date
from core.utilities.json import read_json_file, write_json_file

STR_EMPTY: str = ""
OUTLINE_TAG: str = "outline"
CATEGORY: str = "category"
DISABLED: str = "isComment"
HTML_URL: str = "htmlUrl"
RSS: str = "rss"
TEXT: str = "text"
TITLE: str = "title"
TYPE: str = "type"
XML_URL: str = "xmlUrl"

TRUE: str = "true"
FALSE: str = "false"


def disabled(outline: Element) -> bool:
    """
    Checks if the element has been "commented out", i.e. disabled
    Args:
        outline (Element): outline xml element

    Returns:
        bool: True if the element is disabled
    """
    return outline.attrib.get(DISABLED, FALSE).lower() == TRUE


class OPMLService:
    _opml_file: Path
    _e_tag_file: Path
    _opml: ElementTree[Element[str]]
    _body: Element
    _e_tags: dict[str, str]

    e_tags_modified: datetime
    
    # HOLY VIOLATION OF SEPARATION OF CONCERNS BATMAN
    @property
    def e_tags(self) -> dict[str, str]:
        last_modified = file_modification_date(self._e_tag_file)
        if last_modified > self.e_tags_modified:
            self.e_tags_modified = last_modified
            self._e_tags = read_json_file(self._e_tag_file)
        return self._e_tags

    @property
    def disabled_feeds(self) -> list[Feed]:
        return [
            Feed.from_dict(
                outline.attrib, self.e_tags.get(outline.attrib[XML_URL], STR_EMPTY)
            )
            for outline in self._body
            if disabled(outline)
        ]

    @property
    def feeds(self) -> list[Feed]:
        return [
            Feed.from_dict(
                outline.attrib, self.e_tags.get(outline.attrib[XML_URL], STR_EMPTY)
            )
            for outline in self._body
            if not disabled(outline)
        ]

    # TODO: Create e-tag service, there's too many details and this is a separate concern from OPML or RSS Feed reading
    def __init__(self, settings: Settings):
        self._opml_file = Path(settings.opml_file_path)
        self._e_tag_file = Path(settings.e_tag_file_path)
        if not self._e_tag_file.exists():
            write_json_file(self._e_tag_file, {})
        self.load_opml_file(self._opml_file)

    def load_opml_file(self, opml_file: Optional[Path] = None) -> None:
        if opml_file is None:
            opml_file = self._opml_file
        else:
            self._opml_file = opml_file
        if opml_file.exists():
            self._opml = ET.parse(opml_file)
        else:
            self._opml = ET.parse(StringIO(EMPTY_OPML))
        self._body = self._opml.getroot()[1]

    def save_opml_file(self, opml_file_path: Optional[Path] = None) -> None:
        if opml_file_path is None:
            opml_file_path = self._opml_file
        else:
            self._opml_file = opml_file_path
        self._opml.write(opml_file_path)

    def add_feed(self, feed: Feed) -> None:
        if self.feed_exists(feed):
            raise DuplicateFeedError(feed.xml_url)
        elif self.disabled_feed_exists(feed):
            self.update_feed(feed)
            self.enable_feed(feed)
        else:
            self._body.append(self.create_element_from_feed(feed))

    def get_feed_element(self, xml_url: str) -> Element:
        try:
            return [
                outline for outline in self._body if outline.attrib[XML_URL] == xml_url
            ][0]
        except IndexError:
            raise FeedNotFoundError(xml_url)

    def disable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.xml_url).set(DISABLED, TRUE)

    def enable_feed(self, feed: Feed) -> None:
        self.get_feed_element(feed.xml_url).set(DISABLED, FALSE)

    def feed_exists(self, feed: Feed) -> bool:
        return any(
            [
                existing_feed
                for existing_feed in self.feeds
                if existing_feed.xml_url == feed.xml_url
            ]
        )

    def disabled_feed_exists(self, feed: Feed) -> bool:
        return any(
            [
                existing_feed
                for existing_feed in self.disabled_feeds
                if existing_feed.xml_url == feed.xml_url
            ]
        )

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
                CATEGORY: f"/{feed.category}",
                XML_URL: feed.xml_url,
                HTML_URL: feed.html_url,
                DISABLED: FALSE,
            },
        )


EMPTY_OPML = """
    <?xml version="1.0" encoding="UTF-8"?>
    <opml version="1.0">
    <head>
        <title>My RSS Feeds</title>
        <description></description>
    </head>
    <body>

    </body>
    </opml>
"""
