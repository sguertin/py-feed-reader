from abc import ABC, ABCMeta, abstractmethod


class IETagService(ABC, metaclass=ABCMeta):
    @property
    @abstractmethod
    def etags(self) -> dict[str, str]:
        """The current etags stored by the xml url for each feed

        Returns:
            dict[str, str]: a dictionary of xml url keys with etag values
        """
        pass

    @abstractmethod
    def get_etag(self, xml_url: str) -> str | None:
        """Retrieve the etag for a given xml url

        Args:
            xml_url (str): the feed's xml url

        Returns:
            str|None : the etag or None if none are found
        """
        pass

    @abstractmethod
    def set_etag(self, xml_url: str, etag: str) -> None:
        """Set the etag for a feed

        Args:
            xml_url (str): the feed's xml url
            etag (str): the etag from the last reading of the rss feed
        """
        pass
