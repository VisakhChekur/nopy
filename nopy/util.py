from logging import getLogger
import logging


def make_logger() -> logging.Logger:

    logger = getLogger(__package__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
