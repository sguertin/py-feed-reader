from abc import ABC, ABCMeta, abstractmethod

class IETagService(ABC, metaclass=ABCMeta):
    @property
    @abstractmethod
    def e_tags(self) -> dict[str, str]:
        """The current e_tags stored by the xml url for each feed

        Returns:
            dict[str, str]: a dictionary of xml url keys with e-tag values
        """
        pass
    
    @abstractmethod
    def get_e_tag(self, xml_url: str) -> str | None:
        """Retrieve the e_tag for a given xml url

        Args:
            xml_url (str): the feed's xml url

        Returns:
            str|None : the e-tag or None if none are found
        """
        pass
    
    @abstractmethod
    def set_e_tag(self, xml_url: str, e_tag: str) -> None:
        """Set the e_tag for a feed

        Args:
            xml_url (str): the feed's xml url
            e_tag (str): the e-tag from the last reading of the rss feed
        """
        pass