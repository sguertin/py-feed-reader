from abc import ABC, ABCMeta, abstractmethod


class BaseError(Exception, ABC, metaclass=ABCMeta):

    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__name__}('{self.message}')"


class ApplicationError(BaseError):
    _message: str

    @property
    def message(self):
        return self._message

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(args, kwargs)
        self._message = message
