from dataclasses import dataclass

@dataclass
class Feed:
    title: str
    xml_url: str
    html_url: str
    category: str
    e_tag: str
    
    @classmethod
    def from_dict(cls, entry: dict[str,str], e_tag) -> Feed:
        return cls(
            title=entry.get("title", ""),
            xml_url=entry.get("xmlUrl", ""),
            html_url=entry.get("htmlUrl", ""),
            category=entry.get("category", "").replace("/", ""),
            e_tag=e_tag,
        )