import logging
from logging import getLogger


def make_logger(log_level: int) -> logging.Logger:

    logger = getLogger(__package__)
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
