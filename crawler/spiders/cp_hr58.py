import base64
import hashlib
import io
import json, sys
import os, time
import random
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from core.mysql import session_scope
from core.schema import CookieStore

# from lxml import etree
# from lxml.etree import HTML
# import logging
import re

from fontTools.ttLib import TTFont

from core.base import Base
from config import ROOT_PATH, NUM_PRE_COOKIES

try:
    from .base import *
    from .yima_api import Yima
except:
    from base import *
    from yima_api import Yima

from core.func import get_local_ip, send_ftqq_msg


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')


class COOKIES_STATUS:
    ok = 0  # 可以用
    broken = 1  # 被封需要更换
    updating = 2  # 正在更换


class HR58(SpiderBase, Base):
    name = 'hr58'
    selenium = True

    def __init__(self, logger=None, st_flag=None):
        super(HR58, self).__init__(logger, st_flag)
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
        self.s.headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,it;q=0.8',
            'cache-control': 'no-cache',
            'cookie': 'commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; sessionid=8a9675fa-4e41-423c-bf28-96eeecbb70d3; param8616=1; param8716kop=1; id58=e87rZl0EuzCoPyC3CISqAg==; 58tj_uuid=a22f6c49-35ff-4270-bb98-d2019ec09be9; new_uv=1; utm_source=; spm=; init_refer=; jl_list_left_banner=1; als=0; wmda_uuid=b6470035d30409766e3ee91a34134b88; wmda_new_uuid=1; wmda_session_id_1731916484865=1560591154559-d9fea39d-51e4-d60a; wmda_visited_projects=%3B1731916484865; xxzl_deviceid=OaoMjiA0nALhIk8zQgyEqqC3l8WbqPO7tnnsBGKfNsq48JuDusI4uvBUV2tTaT1r; PPU="UID=63814192696597&UN=xvhjzdghyhlg&TT=7de63ccc32a8e06f75c3e53d361f507b&PBODY=RBW5dnfz1XND4QF10hm9wBOmrFc22q_0pTJ1YZOLJlFocLYgeC5QLQuPr05KE7ZzWeo58JMSzD030OzjTl62MjUvFARQi0ucSQ-Gibgnl7lWVYYSqQHG60I4BCIceOkdUZFtwP1c-hziWZ_4iJ3BqPYfu2I-T9KrpKDTC7d6qRo&VER=1"; www58com="UserID=63814192696597&UserName=xvhjzdghyhlg"; 58cooper="userid=63814192696597&username=xvhjzdghyhlg"; 58uname=xvhjzdghyhlg; new_session=0; showPTTip=1; ljrzfc=1',
            'pragma': 'no-cache',
            'referer': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-0f7d-5880-bbccd08216eb&ClickID=104',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            # 'x-requested-with': 'XMLHttpRequest',
        }
        self.driver = None
        self.cookies = None
        self.call_login_times = 0
        self.uid = st_flag
        self.first = True
        self.need_login_times = 0
        self.tag = 'cookies_{}'.format(int(self.uid['user_id']) % NUM_PRE_COOKIES)
        self.query_cookies_change_cookies()
        # self.login()

    def check_is_login(self):
        url = 'https://employer.58.com/resumesearch'
        kwargs = {
            'url': url
        }
        res = self.send_request(method='get', **kwargs)
        if '<title>用户登录-58同城</title>' in res.content.decode():
            return False
        return True

    def login(self):
        l = self.l
        self.call_login_times += 1
        if self.call_login_times > 10:
            l.info(f"login be called: {self.call_login_times}, exit...")
            sys.exit()

        cookies_path = os.path.join(ROOT_PATH, 'cookies')
        if not os.path.exists(cookies_path):
            os.makedirs(cookies_path)

        cookies_name = f'cookies_{self.uid}'
        # if not os.path.exists(cookies_name):

        if self.first:
            if os.path.exists(cookies_name):
                self.first = False
                with open(os.path.join(cookies_path, cookies_name), 'r') as f:
                    cookies = f.read().strip()
                    l.info(f'loaded local cookies: {cookies}')
                    self.s.headers['cookie'] = cookies
                if self.check_is_login():
                    l.info(f'local cookies useful, login success...')
                    return True

        # login with selenium
        for _ in range(10):
            l.info(f"no cookies, starting {_ + 1}/10 login...")
            cookie_str = self._login()
            if cookie_str:
                self.s.headers['cookie'] = cookie_str
                # self.cookies = cookies
                # self.s.cookies = requests.utils.cookiejar_from_dict(cookies)
                with open(os.path.join(cookies_path, cookies_name), 'w') as f:
                    f.write(str(cookie_str))
                return
            try:
                self.driver.quit()
            except:
                pass
        l.error(f"after 10 retry, failed to login, exit....")
        sys.exit()

    def _login(self):
        l = self.l
        option = ChromeOptions()
        option.add_argument('-headless')
        option.add_argument('--no-sandbox')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = Chrome(options=option, executable_path='/home/hr58/chromedriver')
        self.driver = driver

        driver.get('https://passport.58.com/login')
        driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/img')[0].click()
        driver.find_elements_by_xpath('//*[@id="phonenum"]')[0].click()

        ele = driver.find_elements_by_xpath('//*[@id="phone"]')[0]

        phonenum = self.yima.generate_phone()
        # print('phone:', phonenum)
        l.info(f"get phone: {phonenum}")

        for character in phonenum:
            ele.send_keys(character)
            time.sleep(0.1)
        driver.save_screenshot('./c_phone.png')

        # 点击发送验证码
        # driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/span')[0].click()
        driver.find_element_by_class_name('getcode').click()
        time.sleep(1.1)
        driver.save_screenshot('./send_sms.png')

        code = self.yima.get_message(phone=phonenum)
        l.info(f"get code: {code}")
        if not code:
            l.error(f"get code timeout.")
            return False

        ele = driver.find_elements_by_xpath('//*[@id="mobilecode"]')[0]
        for character in code:
            ele.send_keys(character)
            time.sleep(0.1)

        time.sleep(1.1)
        driver.find_elements_by_xpath('//*[@id="btn_phonenum"]')[0].click()
        l.info('has clicked login button.')
        time.sleep(5)
        driver.get('https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29')
        time.sleep(10)
        driver.save_screenshot('./login.png')

        self.yima.release_num(phonenum)

        if 'employer.58.com/resumesearch' not in driver.current_url:
            l.error(f"login failed, current url: {driver.current_url}")
            return False

        # driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div[2]')[0].click()
        # time.sleep(5)
        # driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[2]/ul/li[1]/div[1]/div[3]/p[1]/span[1]')[
        #     0].click()
        cookie_str = driver.execute_script('return document.cookie')
        # cookies = {i['name']: i['value'] for i in driver.get_cookies()}
        self.l.info(f"get cookies: {cookie_str}")
        driver.quit()
        # return cookies
        return cookie_str

    def gene_jq_name(self):
        _1 = (str(random.random()) + str(random.random())).replace('0.', '')[3:24]
        _2 = str(int(time.time() * 1000))
        'jQuery180024326300832150838_1557039752063'
        return 'jQuery' + _1 + '_' + _2

    def query_list_page(self, keyword, page_to_go):
        '''58job HTML'''
        # # keyword:  159+3084
        # l = self.l
        # l.info(str([keyword, page_to_go]))
        #
        # cid = 158  # 158是武汉，暂时只是抓取武汉
        # aid, nid = keyword.strip().split('+')
        # nid = '-1'
        #
        # jq = self.gene_jq_name()
        # search_url = f'https://employer.58.com/resume/searchresume'
        # params = {
        #     'cid': cid,
        #     'aid': aid,
        #     'nid': nid,
        #     'eduabove': '0',
        #     'workabove': '0',
        #     'pc': '0',
        #     'mc': '0',
        #     'pageindex': page_to_go,
        #     'resumeSort': 'time',
        #     'update24Hours': '1',
        #     'keyword': '',
        #     'pageSize': '70',
        #     'callback': jq,
        #     '_': str(int(time.time() * 1000)),
        # }
        #
        # self.current_url = search_url
        # retry_time = 15
        # time.sleep(6)
        # kwargs = {
        #     'url': search_url,
        #     'params': params
        # }
        #
        # for _ in range(retry_time):
        #     res = self.send_request(method='get', **kwargs)
        #     if res == '':
        #         l.info(f'current query list page failed, try another time...')
        #         continue
        #     conn = res.content.decode()
        #     conn = conn.replace(jq + '(', '')[:-1]
        #     if '频繁' in conn:
        #         l.info(f'crawl too frequent, sleep 10~15s and change proxy...')
        #         time.sleep(random.uniform(10, 15))
        #         self.proxy = {}  # 换ip
        #         continue
        #     tmp = json.loads(conn)
        #     tmp['index'] = int(page_to_go)
        #     conn = json.dumps(tmp, ensure_ascii=False)
        #     l.info(f'{"*" * 5}  get job detail success, len:{len(conn)} {"*" * 5}')
        #     # print(conn)
        #     # sys.exit()
        #     return conn
        # return ''
        pass

    def __get_view(self, resumeId):
        if not resumeId:
            return """{"returnMessage":"success","entity":"{\"b\":0,\"c\":0,\"d\":0,\"dw\":0,\"f\":0,\"r\":0,\"re\":0}"}"""

        kwargs = {
            'url': 'https://statisticszp.58.com/resume/statics/{}'.format(resumeId),
        }
        res = self.send_request(method='get', **kwargs)
        return res.content.decode()

    def xml_to_unimap(self, xml_path):
        with open(xml_path, 'r') as f:
            xml = f.read()
        xml = xml.replace('<TTGlyph name="glyph00000"/>', '')
        res = re.findall(r'<TTGlyph name="(.*?)" (.*?)</TTGlyph>', xml, re.S)
        return {i[0]: hashlib.md5(''.join(i[1].split()).encode()).hexdigest() for i in res[:]}

    def resource_page(self, json_str, raw):
        l = self.l
        res = """@font-face{font-family:"customfont"; src:url(data:application/font-woff;charset=utf-8;base64,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)  format("woff");}"""
        xml_path = f'/tmp/font_{os.getpid()}.xml'
        to_replace = re.findall(r'&#x(\w+);', res)
        if not to_replace:  # 不需要替换字体
            return res

        base64_str = re.findall('data:application/font-woff;charset=utf-8;base64,(.*)format', res)
        bin_data = ''
        if not base64_str:
            font_url = re.findall(r'@font-face {font-family:"customfont"; src:url\((.*?)\)', res, re.S)
            if font_url:
                font_url = 'https:' + font_url[0]
                l.info(f'font url: {font_url}')
                kwargs = {
                    'url': font_url,
                }
                font_res = self.send_request(method='get', **kwargs)
                bin_data = io.BytesIO(font_res.content)
        else:
            bin_data = base64.b64decode(base64_str[0])
            bin_data = io.BytesIO(bin_data)
        if not bin_data:
            raise Exception('get font Bytes error...')
        fonts = TTFont(bin_data)
        fonts.saveXML(xml_path)
        maps = self.xml_to_unimap(xml_path)
        # print(maps)
        raw = {v: k for k, v in raw.items()}
        for i in to_replace:
            new = 'uni' + i.upper()
            hash_graph = maps.get(new)
            # print(hash_graph)
            font = raw.get(hash_graph, None)
            if not font:
                raise Exception('get none from woff maps, maybe the web font file has changed...')
            # print(font)
            json_str = json_str.replace('&#x{};'.format(i), font)
        return json_str

    def _query_cookies(self):
        # mysql 取cookies
        with session_scope() as s:
            query = s.query(CookieStore).filter(CookieStore.tag == self.tag).first()
            if not query:
                return None
            if query.status == COOKIES_STATUS.ok:
                return query.cookies
            return None

    def query_cookies_change_cookies(self):
        l = self.l
        while True:
            cookies = self._query_cookies()
            if not cookies:
                l.info('tag: {} has no cookies now, sleep 10s.')
                time.sleep(10)
                continue
            l.info(f'get cookies {self.tag} from mysql: {cookies}')
            self.s.headers['cookie'] = cookies
            return

    def query_detail_page(self, url):
        '''
        打开58job详情页面
        '''
        l = self.l
        l.info('aid+page: {}'.format(url))

        cid = 158  # 158是武汉，暂时只是抓取武汉
        # aid, nid = keyword.strip().split('+')
        aid, page_to_go = url.strip().split('+')
        nid = '-1'

        jq = self.gene_jq_name()
        search_url = f'https://employer.58.com/resume/searchresume'
        params = {
            'cid': cid,
            'aid': aid,
            'nid': nid,
            'eduabove': '0',
            'workabove': '0',
            'pc': '0',
            'mc': '0',
            'pageindex': page_to_go,
            'resumeSort': 'time',
            'update24Hours': '1',
            'keyword': '',
            'pageSize': '70',
            'fontKey': '6e929d7529484474a0c456fca2822d0b',  # todo 对应的字体文件
            'callback': jq,
            '_': str(int(time.time() * 1000)),
        }

        self.current_url = search_url
        retry_time = 15
        time.sleep(6)
        kwargs = {
            'url': search_url,
            'params': params
        }

        for _ in range(retry_time):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query list page failed, try another time...')
                continue
            conn = res.content.decode()
            conn = conn.replace(jq + '(', '')[:-1]
            if '频繁' in conn:
                l.info(f'crawl too frequent, sleep 10~15s and change proxy...')
                time.sleep(random.uniform(10, 15))
                self.proxy = {}  # 换ip
                continue
            tmp = json.loads(conn)
            tmp['index'] = int(page_to_go)
            conn = json.dumps(tmp, ensure_ascii=False)
            l.info(f'{"*" * 5}  get job detail success, len:{len(conn)} {"*" * 5}')
            # print(conn)
            # sys.exit()
            return conn
        return ''


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
