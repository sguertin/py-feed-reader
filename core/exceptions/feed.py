from core.exceptions.common import BaseError


class FeedNotFoundError(BaseError):
    xml_url: str

    def __init__(self, xml_url: str, *args):
        super().__init__(args)
        self.xml_url = xml_url
        self.add_note(self.message)

    @property
    def message(self) -> str:
        return f"'{self.xml_url}' was not found!"

    def __repr__(self) -> str:
        return f"FeedNotFoundError(xml_url='{self.xml_url}')"


class DuplicateFeedError(BaseError):
    feed_url: str

    def __init__(self, feed_url: str, *args):
        super().__init__(args)
        self.feed_url = feed_url

    @property
    def message(self) -> str:
        return f"'{self.feed_url}' already exists!"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"DuplicateFeedError(feed_url='{self.feed_url}')"
