from typing import Any, TypeVar
from core.utilities.singleton import SingletonMeta

T = TypeVar("T")


class Configuration(metaclass=SingletonMeta):
    _configs: dict[type, Any] = {}

    def get_config(self, config_type: type[T]) -> T:
        return self._configs[config_type]

    def set_config(self, config_type: type[T], config: T) -> None:
        self._configs[config_type] = config

    def clear(self) -> None:
        self._configs = {}
