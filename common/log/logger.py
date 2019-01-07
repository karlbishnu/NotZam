import logging

from .filter import CidContextFilter

default_format = '[cid: %(cid)s] %(levelname)s %(asctime)s %(module)s %(message)s'


def get_logger(name=None, level='INFO', logging_format=default_format):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(logging_format))

    logger.addFilter(CidContextFilter())
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
