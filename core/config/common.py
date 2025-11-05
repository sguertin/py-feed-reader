from typing import Any, TypeVar
from core.utilities.singleton import SingletonMeta

T = TypeVar("T")


class Configuration(metaclass=SingletonMeta):
    _configs: dict[type, Any] = {}

    def get_config(self, config_type: type[T]) -> T:
        """Retrieves the registered config for the provided config_type

        Args:
            config_type (type[T]): the type of config requested

        Returns:
            T: the instance of the config
        """
        return self._configs[config_type]

    def set_config(self, config_type: type[T], config: T) -> None:
        """Registers a config of a specific type

        Args:
            config_type (type[T]): the type of the config to register
            config (T): the instance of the config type
        """
        self._configs[config_type] = config

    def clear(self) -> None:
        """Remove all registered configurations"""
        self._configs = {}
