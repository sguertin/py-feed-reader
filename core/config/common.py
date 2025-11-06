from typing import Any, TypeVar
from core.exceptions.config import ConfigurationNotFoundError
from core.utilities.singleton import SingletonMeta

T = TypeVar("T")


class ConfigurationRoot(metaclass=SingletonMeta):
    _configs: dict[type, Any] = {}

    @property
    def count(self) -> int:
        return len(self._configs.keys())

    def get_config(self, config_type: type[T], use_default: bool = False) -> T:
        """Retrieves the registered config for the provided config_type

        Args:
            config_type (type[T]): the type of config requested

        Returns:
            T: the instance of the config
        """
        config = self._configs.get(config_type, None)
        if config is not None:
            return config
        if use_default:
            default = config_type()
            self._configs[config_type] = default
            return default
        config_type_name = config_type.__name__
        raise ConfigurationNotFoundError(config_type_name)

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

    def __repr__(self) -> str:
        configs_text = ",".join([cfg.__name__ for cfg in self._configs.keys()])
        return (
            f"ConfigurationRoot(total_configs={self.count}, configs=[{configs_text}])"
        )


config = ConfigurationRoot()
