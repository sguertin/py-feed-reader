from abc import ABC, ABCMeta, abstractmethod

from core.models.feed import Feed, FeedItem


class IRssReaderService(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_items(
        self,
        category: str | None = None,
        exclude_read: bool = True,
    ) -> list[FeedItem]:
        """Retrieves feed items optionally filtered by read status and/or category

        Args:
            category (str | None, optional): category retrieve items from. Defaults to None.
            exclude_read (bool, optional): set to False to include previously read items. Defaults to True.

        Raises:
            CategoryDoesNotExistError: raised if the specified category could not be found

        Returns:
            list[FeedItem]: the list of feed items
        """
        pass

    @abstractmethod
    def get_feed_items(self, feed: Feed, exclude_read: bool = True) -> list[FeedItem]:
        """Retrieves items from the specified feed

        Args:
            feed (Feed): the feed to retrieve items for
            exclude_read (bool, optional): set to False to include previously read items. Defaults to True.

        Raises:
            RssFeedNotFoundError: raised if the Rss Feed could not be retrieved

        Returns:
            FeedItem:
        """
        pass
