from core.config.common import config
from core.config.file import FileStorageSettings
from core.config.logging import dev_configuration  # , default_configuration
from core.services.feed.opml import OPMLFeedService


config.get_config(FileStorageSettings, True)
dev_configuration()
feed_service = OPMLFeedService()
