import base64
import hashlib
import io
import json, sys
import os, time
import random
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# from lxml import etree
# from lxml.etree import HTML
# import logging
import re

from fontTools.ttLib import TTFont

from core.base import Base
from core.func import send_ftqq_msg, get_local_ip
from config import ROOT_PATH

try:
    from .base import *
    from .yima_api import Yima
except:
    from base import *
    from yima_api import Yima


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

def lock_single_selenium(func):
    def wrapper(*args, **kwargs):
        lock_path = './login.lock'
        l = args[0].l
        while True:
            if os.path.exists(lock_path):
                l.info('other spiders is logining, wait....')
                time.sleep(3)
                continue
            with open(lock_path, 'w', encoding='utf-8') as f:
                f.write('')  # 加锁
            res = func(*args, **kwargs)
            os.remove(lock_path)  # 移除锁文件
            return res
    return wrapper


class Job58(SpiderBase, Base):
    name = 'job58'
    selenium = True

    def __init__(self, logger=None, st_flag=None):
        super(Job58, self).__init__(logger, st_flag)
        self.proxy_request_delay = 3
        self.yima = Yima(username="fbfbfbfb", password="jianxun1302", project_id=159, project_name=u"58同城")
        self.raw = {'届': 'e04fd81cb8c88283509d5341a5239d27', '陈': 'a7cce2d2e218b52730631d09ec7e2ed9',
                    'B': 'd8053f3eb827b6bc22006b7200ba2f5e', '验': '7a33cce93a04b4524c945fdd4863c692',
                    '张': 'e44ea76315a9181253f7e39021a11901', '9': '88513b3b880318b2aefe1c35baaa7317',
                    '黄': '4228c2b7c3c4edb4b069e96d908a8f15', 'M': 'b3ef7aacedb46a51123ba44ffc6e93f2',
                    '大': 'c4c708edd777514f181bbc23cbc251c0', '5': '7b30bfaa410b31b8f622689785fec6ea',
                    '经': '3567a87741d0cb1883dfd69cfd1e0f46', '硕': 'cb88eed2daeb561016eefe02ec301b08',
                    '1': '00d61ac0c9b97bd51ce0def77708151d', '男': 'c5332bc0e32cf526c35d675000b86a1c',
                    '李': 'a690e49089b65b3870e9f0323a2c9a0b', '本': '5e28508bb8c28f71b869a3bfbb7480a8',
                    '无': '2919e0c17e85f2bfe86b5ce9b65c3eae', '以': 'd22a15a2f90ee09a6c0bf0823d079be5',
                    '中': '44fc8a68e6c9df82bf852d3c66eaeb05', '应': '0cce8876190362b436b578dbed3f9246',
                    '刘': '959c3f40e416c0781c76de0e107a5d87', '高': 'f191b64b86ebc5e83be80157e08837f7',
                    '科': '78098b93944a5d4f80be0ae3ddde7cb3', '下': '78547b10ad2bed3d059999b8a96dd1b8',
                    '士': 'd135638806955c0ee9d255c64a952705', '2': 'b3c4c3c3910b00cadde436b80f6a8f6b',
                    'A': '74b827b8303f2ea048a46dbc9af94bb1', '杨': '92a3b6fce1f494c341e108a80663092e',
                    '技': 'eaeeb3a7d33100f7111086ddc809f347', '3': 'b18fc63ce51133a669550d84582cb419',
                    '王': '3f68d21b92136ffc805b4447ff36a51c', 'E': '91977ada50e982cee1ee1bc77af4ec14',
                    '博': '0d93906202dbf2ef2f1ea3e62b8da9c7', '专': '838da47c476a8bd67657de21a39eb6c1',
                    '女': 'b9112f6e0b8cfea98108fcd418258219', '赵': 'adf2316c9216071fc6fde848f30b29b2',
                    '8': 'f37cd5eddb6767c4af2522dfe31bb9af', '4': '14e811bd38883308e8acd8b1c93626a9',
                    '吴': '0b8c37528ba6265f4b2fbd6ae13da1bc', '0': '11017a39e2ec6133814e3b78fd9b65a5',
                    '7': '8b704365dbeda76db5b5ccb61f6da11e', '6': '6e91626a6e9bdbedcb288e72022c512a',
                    '校': 'b3fe35de81075be87c90995ffb1a0ba6', '生': '9376dbdbb9f3cb9e17094bc1384e6d3c',
                    '周': 'd9a3ae3942f61fcf567a682c766076e0', 'x': '23629ab2fe153b1ef9ca6b2c935eec3a'}

        cookies = 'commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; xxzl_deviceid=JEeqR%2FlvZb3nkMnYIyXnOu6jyZR7P5DCgLq7pAeTAPCQwlHFbAOuR2G1yHqWb5%2FV; PPU="UID=64419503664392&UN=s3ghmh70x&TT=8e91f95d03be12825195460da19adf76&PBODY=Z0Eu5T2DSidVsd_xfi2AdIXPcbqMygPCEsGkcHJdZ1FQYP3jVy9nkiy3UZIKYwPwXDtzZS_JvRMF4rcflohhYAoF2NyIFSCeBYDTxfcFD165wlH3vaEXdF3aa9TyLzEYZ7hx8RrqD3IAgRHxHzJu2jhpu7yZL02Tt_WpLin9Xss&VER=1"; www58com="UserID=64419503664392&UserName=s3ghmh70x"; 58cooper="userid=64419503664392&username=s3ghmh70x"; 58uname=s3ghmh70x; id58=c5/nn10MUR40y9dYOYYPAg==; 58tj_uuid=bfb34ef7-1022-4fa0-9e11-7909b2a86882; new_uv=1; utm_source=; spm=; init_refer=; new_session=0; als=0; showOrder=1; xxzl_smartid=91d3942d198af425fe14cc84ece4df2f; showPTTip=1; ljrzfc=1; wmda_uuid=0ea1bb90b58fb575349a29fb0f3717a3; wmda_new_uuid=1; wmda_session_id_1731916484865=1561088740962-50154453-d145-fcd3; wmda_visited_projects=%3B1731916484865; isShowYdPaychat=1'
        self.s.headers = {
            # 'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,it;q=0.8',
            'cache-control': 'no-cache',
            'cookie': cookies,
            'pragma': 'no-cache',
            'referer': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-0f7d-5880-bbccd08216eb&ClickID=104',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
            # 'x-requested-with': 'XMLHttpRequest',
        }
        # cookies_ = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('; ')}
        # self.s.cookies = requests.utils.cookiejar_from_dict(cookies_)
        self.driver = None
        self.cookies = None
        self.call_login_times = 0
        self.uid = st_flag
        self.first = True
        self.need_login_times = 0
        self.fr_times = 0
        # time.sleep(3 * 60)
        # self.login()

    def gene_jq_name(self):
        _1 = (str(random.random()) + str(random.random())).replace('0.', '')[3:24]
        _2 = str(int(time.time() * 1000))
        'jQuery180024326300832150838_1557039752063'
        return 'jQuery' + _1 + '_' + _2

    def query_list_page(self, keyword, page_to_go):
        l = self.l
        l.info(str([keyword, page_to_go]))
        # keyword 人力|行政|管理 人事/行政/后勤 renli
        keyword = keyword.strip()

        tmp = keyword.split('+')

        if len(tmp) == 1:  # 旧版只有分类
            url_key = tmp[0]
            search_url = 'https://wh.58.com/{}/pn{}'.format(url_key, page_to_go)
        elif len(tmp) == 2:  # 新版加入地区
            url_key, area = tmp
            search_url = 'https://wh.58.com/{}/{}/pn{}'.format(area, url_key, page_to_go)
        else:
            raise Exception(f'58job search job key: {keyword} error!!')

        self.current_url = search_url
        retry_time = 15

        time.sleep(6)
        # https://wh.58.com/caiwujingli/pn2
        kwargs = {
            'url': search_url
        }

        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query list page failed, try another time...')
                continue
            conn = res.content.decode()
            if '频繁' in conn:
                l.info(f'crawl too frequent, sleep 10~15s and change proxy...')
                time.sleep(random.uniform(10, 15))
                self.proxy = {}  # 换ip
                continue
            l.info(f'get job detail success, len:{len(conn)}')
            return conn
        return ''

    def __get_view(self, info_id, url):
        if not info_id:
            return 0, 0

        kwargs = {
            'url': 'https://jst1.58.com/counter?infoid={}&userid=&uname=&sid=0&lid=0&px=0&cfpath='.format(info_id),
            'headers': {'Referer': url}
        }
        res = self.send_request(method='get', **kwargs)
        view = res.content.decode().split('Counter58.total=')[-1]
        view = int(view) if view else 0
        return view

    def __get_apply(self, info_id, html):
        # html =  html.replce(' ', '')
        user_id = re.findall(r"'userid':'(\d+)'", html.replace(' ', ''), re.S)

        if not user_id:
            return 0

        kwargs = {
            'url': 'https://statisticszp.58.com/position/totalcount/?infoId={}&userId={}'.format(info_id, user_id[0])
            # 'headers': {'Referer': url}
        }
        res = self.send_request(method='get', **kwargs)
        apply = re.findall(r'"deliveryCount":(\d+),', res.content.decode())
        apply = int(apply[0]) if apply else 0
        return apply

    def query_detail_page(self, url):
        '''
           打开58job详情页面
           '''
        l = self.l
        # self.session.headers['User-Agent'] = random_ua()
        # l.debug(f'Open a resume: request_url: {url}')
        retry_time = 15
        key_info = json.loads(key_info)
        # print('+'*66, key_info['type'])
        key_type = key_info['type']
        # sys.exit(6666)
        # time.sleep(6)
        # https://wh.58.com/renli/34103568126897x.shtml?psid=127631613204014944925734117&entinfo=34103568126897_j&ytdzwdetaildj=0&finalCp=000001250000000000080000000000000000_127631613204014944925734117&tjfrom=pc_list_left_jp__127631613204014944925734117__21562518912925696__jp

        info_id = re.findall('(\d+)x.shtml', url)
        if not info_id:
            info_id = re.findall('entinfo=(\d+)_', url)
        if not info_id:
            raise Exception('invalid url...')
        info_id = info_id[0]

        kwargs = {
            'url': url
        }
        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query detail page failed, try another time...')
                continue
            conn = res.content.decode()
            if '频繁' in conn:
                l.info(f'crawl too frequent, sleep 10~15s and change proxy...')
                time.sleep(random.uniform(10, 15))
                self.proxy = {}
                continue

            l.info(f'get job detail success, len:{len(conn)}')
            view = self.__get_view(info_id, url)
            apply = self.__get_apply(info_id, conn)
            l.info(f'get view:{view}, apply: {apply}')
            conn = f'{conn}+++{view}+++{apply}+++{key_type}'
            return conn
        return ''


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
