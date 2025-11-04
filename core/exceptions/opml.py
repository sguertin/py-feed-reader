
class FeedNotFoundError(Exception):
    xml_url: str
    def __init__(self, xml_url: str, *args):
        super().__init__(args)
        self.xml_url = xml_url
    
    @property
    def message(self)->str:
        return f"'{self.xml_url}' was not found!"
        
    def __str__(self)->str:
        return self.message

    def __repr__(self)->str:
        return f'FeedNotFoundError({self.message})'

class DuplicateFeedError(Exception):
    xml_url: str
    def __init__(self, xml_url: str, *args):
        super().__init__(args)
        self.xml_url = xml_url
    
    @property
    def message(self)->str:
        return f"'{self.xml_url}' already exists!"
        
    def __str__(self)->str:
        return self.message

    def __repr__(self)->str:
        return f'DuplicateFeedError({self.message})'