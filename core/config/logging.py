import logging


from rich.logging import RichHandler

DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
MESSAGE_FORMAT: str = (
    "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s at %(filename)s:%(lineno)d"
)


def default_configuration():
    logging.basicConfig(
        level=logging.ERROR,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def dev_configuration():
    logging.basicConfig(
        level=logging.NOTSET,
        format=MESSAGE_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)],
    )
