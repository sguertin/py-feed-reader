class ConfigurationNotFoundError(Exception):
    config_name: str

    @property
    def message(self) -> str:
        return f"{self.config_name} is not registered a configuration"

    def __init__(self, config_name: str, *args, **kwargs):
        super().__init__(args, kwargs)
        self.config_name = config_name
