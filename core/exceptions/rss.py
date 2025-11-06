from core.exceptions.common import BaseError


class CategoryDoesNotExistError(BaseError):
    category: str

    def __init__(self, category: str, *args):
        super().__init__(args)
        self.category = category

    @property
    def message(self) -> str:
        return f"'{self.category}' does not exist!"


class RssFeedNotFoundError(BaseError):
    feed_url: str

    def __init__(self, feed_url: str, *args):
        super().__init__(args)
        self.feed_url = feed_url

    @property
    def message(self) -> str:
        return f"'{self.feed_url}' was not found!"
