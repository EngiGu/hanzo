import json
import re

from core.base import Base

try:
    from .base import *
except:
    from base import *


cookies_tmp = '_user_identify_=c1e888d3-e238-3c92-96a4-b8dd0053d928; uID=467464; sID=3da6663cb824e9e66dce9e36de47f8e6; JSESSIONID=aaaPnSZ9HmYDDhC0yv-Sw; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1559645557,1560135696; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1559645557,1560135697; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1560158375; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1560158375'


class DaJie(SpiderBase, Base):
    name = 'yinguo'

    def __init__(self, logger=None):
        super(DaJie, self).__init__(logger, st_flag=None)
        self.proxy_request_delay = 3
        self.s.cookies = requests.utils.cookiejar_from_dict(
            {i.split('=')[0]: i.split('=')[1] for i in cookies_tmp.split('; ')}
        )
        self.s.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }

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
        time.sleep(6)

        kwargs = {
            'url': url,
            'params': params

        }
        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query detail page failed, try another time...')
                continue
            conn_json = res.json()
            conn_json['index'] = int(page_to_go)
            conn = json.dumps(conn_json, ensure_ascii=False)
            l.info(f'{"*"*5} get list success, len:{len(conn)} {"*"*5}')
            return conn
        return ''

    def __get_product(self, ncid):
        if not ncid:
            return """{"code":0,"msg":"OK","data":[]}"""

        kwargs = {
            'url': 'https://www.innotree.cn/inno/company/ajax/projectlist?compId={}'.format(ncid),
        }
        res = self.send_request(method='get', **kwargs)
        return res.content.decode()


    def query_detail_page(self, url):
        # https://www.innotree.cn/inno/company/10906900663086362370.html
        l = self.l
        retry_time = 15
        time.sleep(6)

        l.info(f"open detail page: {url}")
        ncid = re.findall(r'/company/(\d+)', url)
        if not ncid:
            raise Exception(f'url error, url: {url}')
        ncid = ncid[0]

        kwargs = {
            'url': url,

        }
        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query detail page failed, try another time...')
                continue
            conn = res.content.decode()
            view = self.__get_product(ncid)
            conn = f'{conn}+d8053f3eb827b6bc22006b7200ba2f5e+{view}'
            l.info(f'{"*"*5} get detail success, len:{len(conn)} {"*"*5}')
            return conn
        return ''


if __name__ == '__main__':
    pass
