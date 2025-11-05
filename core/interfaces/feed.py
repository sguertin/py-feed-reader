from abc import ABC, ABCMeta, abstractmethod

from core.models.feed import Feed


class IFeedService(ABC, metaclass=ABCMeta):

    @property
    @abstractmethod
    def feeds(self) -> list[Feed]:
        """The list of currently active feeds
        """
        pass
    
    @property
    @abstractmethod
    def disabled_feeds(self) -> list[Feed]:
        """The list of currently disabled feeds
        """
        pass

    @abstractmethod
    def get_feed(self, xml_url: str) -> Feed:
        """Returns the feed for a given xml_url

        Args:
            xml_url (str): the xml_url of the feed

        Raises:
            FeedNotFoundError: thrown if the feed is not found

        Returns:
            Feed: the feed with the xml_url
        """
        pass
    
    @abstractmethod
    def add_feed(self, feed: Feed) -> None:
        """Add a feed to the OPML file

        Args:
            feed (Feed): the feed to be added

        Raises:
            DuplicateFeedError: raised if the feed already exists, based on xml_url
        """
        pass
    
    @abstractmethod
    def update_feed(self, feed_info: Feed) -> None:
        """Update the information for a given feed

        Args:
            feed_info (Feed): the feed information
        """
        pass

    @abstractmethod
    def disable_feed(self, feed: Feed) -> None:
        """Disable a feed

        Args:
            feed (Feed): the feed to be disabled
        """
        pass

    @abstractmethod
    def enable_feed(self, feed: Feed) -> None:
        """Enable a feed

        Args:
            feed (Feed): the feed to be enabled
        """
        pass

    @abstractmethod
    def feed_exists(self, feed: Feed) -> bool:
        """Returns True if the given feed exists

        Args:
            feed (Feed): _description_

        Returns:
            bool: _description_
        """
        pass

    @abstractmethod
    def disabled_feed_exists(self, feed: Feed) -> bool:
        pass
