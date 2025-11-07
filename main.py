from core.config.common import config
from core.config.file import FileStorageSettings, DEFAULT_PICKLE_STORAGE_PATH
import core.config.logging as logging
from core.services.feed.opml import OPMLFeedService
from core.services.rss.pickle import PickleRssStorageService
from core.services.rss.reader import RssFeedReaderService


settings = config.get_config(FileStorageSettings, True)
settings.storage_file_path = DEFAULT_PICKLE_STORAGE_PATH
logging.dev_configuration()
feed_service = OPMLFeedService()
storage_service = PickleRssStorageService()
reader = RssFeedReaderService(storage_service, feed_service)
