from dataclasses import dataclass


@dataclass
class Feed:
    title: str
    xml_url: str
    html_url: str
    category: str
    e_tag: str | None

    def __eq__(self, other: Feed) -> bool:
        return self.xml_url == other.xml_url
