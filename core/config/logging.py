import logging


from rich.logging import RichHandler

DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
MESSAGE_FORMAT: str = (
    '%(name)s [%(levelname)s] "%(message)s" at %(filename)s:%(lineno)d'
)
rich_handler = RichHandler(show_level=False, show_path=False, rich_tracebacks=True)


def default_configuration():
    logging.basicConfig(
        level=logging.ERROR,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[rich_handler],
    )


def dev_configuration():
    logging.basicConfig(
        level=logging.NOTSET,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[rich_handler],
    )
