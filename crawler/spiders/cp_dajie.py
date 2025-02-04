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
    name = 'dajie'

    def __init__(self, logger=None, *args):
        super(DaJie, self).__init__(logger, *args)
        self.proxy_request_delay = 3

    def query_list_page(self, key, page_to_go):
        # key {'provice': '重庆', 'pid': 500000, 'city': '重庆', 'cid': 500000, 'cate': '计算机软件', 'caid': 3104}
        l =  self.l
        l.info(f"get key: {str(key)}, page: {page_to_go}")

        if isinstance(key, str):
            key = eval(key)

        url = f"https://www.dajie.com/corp/index-pa{page_to_go}-ci{key['cid']}-po{key['caid']}-kw/"
        l.info(f"open list page: {url}")
        retry_time = 15
        # time.sleep(6)

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
