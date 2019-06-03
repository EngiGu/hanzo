import os
import random

from lxml import etree
from lxml.etree import HTML
import logging

try:
    from .base import *
except:
    from base import *


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')


class DaJie(SpiderBase):
    name = 'dajie'

    def __init__(self, logger=None):
        super(DaJie, self).__init__(logger)


        # self.url = 'https://www.brfaka.com/orderquery?order_id={}'

    def query_list_page(self, key, page_to_go):
        pass

    def query_detail_page(self, url):
        pass


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
