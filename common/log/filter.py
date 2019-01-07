from .cid import get_cid
import logging


class CidContextFilter(logging.Filter):

    def filter(self, record):
        record.cid = get_cid()
        return True
