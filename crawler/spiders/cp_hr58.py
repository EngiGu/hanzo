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
        self.font = None
        self.font_key = None
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
        res = """ @font-face{font-family:"customfont"; src:url(data:application/font-woff;charset=utf-8;base64,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)  format("woff");}"""
        xml_path = f'/tmp/font_{os.getpid()}.xml'
        to_replace = re.findall(r'&#x(\w+);', json_str)
        if not to_replace:  # 不需要替换字体
            l.error('fontKey may has expired...')
            return None
        # base64_str = re.findall('data:application/font-woff;charset=utf-8;base64,(.*)format', res)
        base64_str = self.font_key
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

    def get_font_and_font_key(self):
        l = self.l
        url = 'https://employer.58.com/resumesearch'
        kwargs = {
            'url': url
        }
        for i in range(10):
            res = self.send_request(method='get', **kwargs)
            if res == '':
                l.info(f'current query list page failed, try another time...')
                continue
            conn = res.content.decode()
            if '<title>用户登录-58同城</title>' in conn:
                self._update_cookies_status(COOKIES_STATUS.broken)
                l.info(f'cookies broken, has updated {self.tag} status -> {COOKIES_STATUS.broken}')
                # 重新获取cookies
                self.query_cookies_change_cookies()
                return ''
            base64_str = re.findall('data:application/font-woff;charset=utf-8;base64,(.*)format', res)
            self.font = base64_str
            self.font_key = re.findall(r'fontKey: "(.*?)",', conn, re.S)[0]

    def _query_cookies(self):
        # mysql 取cookies
        with session_scope() as s:
            query = s.query(CookieStore).filter(CookieStore.tag == self.tag).first()
            if not query:
                return None
            if query.status == COOKIES_STATUS.ok:
                return query.cookies
            return None

    def _update_cookies_status(self, status):
        # mysql 取cookies
        with session_scope() as s:
            s.query(CookieStore).filter(CookieStore.tag == self.tag).update({'status': status})

    def query_cookies_change_cookies(self):
        l = self.l
        while True:
            cookies = self._query_cookies()
            if not cookies:
                l.info('tag: {} has no avail cookies now, sleep 10s.')
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

        if not self.font_key:
            self.get_font_and_font_key()

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
            'fontKey': self.font_key,  # todo 对应的字体文件
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
            if '<title>用户登录-58同城</title>' in conn:
                self._update_cookies_status(COOKIES_STATUS.broken)
                l.info(f'cookies broken, has updated {self.tag} status -> {COOKIES_STATUS.broken}')
                # 重新获取cookies
                self.query_cookies_change_cookies()
                return ''
            conn = conn.replace(jq + '(', '')[:-1]
            if '频繁' in conn:
                l.info(f'crawl too frequent, sleep 10~15s and change proxy...')
                time.sleep(random.uniform(10, 15))
                self.proxy = {}  # 换ip
                continue
            tmp = json.loads(conn)
            tmp['index'] = int(page_to_go)
            conn = json.dumps(tmp, ensure_ascii=False)
            conn = self.resource_page(conn, self.raw)
            if not conn:
                self.get_font_and_font_key()
                return ''
            l.info(f'{"*" * 5}  get job detail success, len:{len(conn)} {"*" * 5}')
            # print(conn)
            # sys.exit()
            return conn
        return ''


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
