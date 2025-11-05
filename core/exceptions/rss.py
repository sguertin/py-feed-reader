class CategoryDoesNotExistError(Exception):
    category: str

    def __init__(self, category: str, *args):
        super().__init__(args)
        self.category = category

    @property
    def message(self) -> str:
        return f"'{self.category}' does not exist!"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"CategoryDoesNotExist({self.message})"


class RssFeedNotFoundError(Exception):
    xml_url: str

    def __init__(self, xml_url: str, *args):
        super().__init__(args)
        self.xml_url = xml_url

    @property
    def message(self) -> str:
        return f"'{self.xml_url}' was not found!"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"RssFeedNotFoundError({self.message})"
