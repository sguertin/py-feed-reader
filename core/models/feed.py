from dataclasses import dataclass

from core.config.dataclasses_json import CamelCaseJsonMixin


@dataclass
class Feed(CamelCaseJsonMixin):
    title: str
    xml_url: str
    html_url: str
    category: str
    e_tag: str | None

    def __eq__(self, other: Feed) -> bool:
        return self.xml_url == other.xml_url


@dataclass
class FeedItem(CamelCaseJsonMixin):
    title: str
    link: str
    description: str
    enclosure: str
    pub_date: str
    guid: str
