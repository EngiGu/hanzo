import json
import os
import random

# from lxml import etree
# from lxml.etree import HTML
# import logging
from core.base import Base

try:
    from .base import *
except:
    from base import *


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')


class DaJie(SpiderBase, Base):
    name = 'yinguo'

    def __init__(self, logger=None):
        super(DaJie, self).__init__(logger)
        self.proxy_request_delay = 3

    def query_list_page(self, key, page_to_go):
        # key 新疆+60+2010及以前+2015及以前
        l = self.l
        l.info(f"get key: {str(key)}, page: {page_to_go}")

        area, rounds, edate, idate = key.split('+')

        params = {
            'query': '',
            'tagquery': '',
            'st': str(page_to_go),
            'ps': '10',
            'areaName': area,
            'rounds': rounds,
            'show': '0',
            'idate': idate,
            'edate': edate,
            'cSEdate': '-1',
            'cSRound': '-1',
            'cSFdate': '1',
            'cSInum': '-1',
            'iSNInum': '1',
            'iSInum': '-1',
            'iSEnum': '-1',
            'iSEdate': '-1',
            'fchain': '',
        }

        url = 'https://www.innotree.cn/inno/search/ajax/getAllSearchResult'
        l.info(f"open list page: {url}")
        retry_time = 15
        # time.sleep(6)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }

        kwargs = {
            'url': url,
            'headers': headers,
            'params': params

        }
        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query detail page failed, try another time...')
                continue
            conn = res.content.decode()
            l.info(f'{"*"*5} get list success, len:{len(conn)} {"*"*5}')
            return conn
        return ''

    def query_detail_page(self, url):
        l = self.l
        retry_time = 15
        # time.sleep(6)
        l.info(f"open detail page: {url}")

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }

        kwargs = {
            'url': url,
            'headers': headers,

        }
        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query detail page failed, try another time...')
                continue
            conn = res.content.decode()
            l.info(f'{"*"*5} get detail success, len:{len(conn)} {"*"*5}')
            return conn
        return ''


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
