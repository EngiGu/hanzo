import os
import random

from lxml import etree
from lxml.etree import HTML

try:
    from .base import *
except:
    from base import *


class DaJie(Base):
    name = 'dajie'

    def __init__(self):
        super(DaJie, self).__init__()
        # self.url = 'https://www.brfaka.com/orderquery?order_id={}'

    def query_list_page(self, key, page_to_go):
        pass

    def query_detail_page(self, url):
        pass


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
