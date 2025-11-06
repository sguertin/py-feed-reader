from typing import Any, TypeVar
from core.exceptions.config import ConfigurationNotFoundError
from core.utilities.singleton import SingletonMeta

T = TypeVar("T")


class ConfigurationRoot(metaclass=SingletonMeta):
    _configs: dict[type, Any] = {}

    def get_config(self, config_type: type[T]) -> T:
        """Retrieves the registered config for the provided config_type

        Args:
            config_type (type[T]): the type of config requested

        Returns:
            T: the instance of the config
        """
        config = self._configs.get(config_type)
        if config is None:
            raise ConfigurationNotFoundError(config_type.__name__)
        return config

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
