import base64
import hashlib
import io
import json,sys
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

try:
    from .base import *
    from .yima_api import Yima
except:
    from base import *
    from yima_api import Yima


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')


class DaJie(SpiderBase, Base):
    name = 'dajie'
    selenium = True

    def __init__(self, logger=None):
        super(DaJie, self).__init__(logger)
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
            'cookie': 'commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; id58=c5/njVzAJMoIAfoXA3VlAg==; 58tj_uuid=329c9551-6862-43d4-9fbe-4cd1ed969770; als=0; xxzl_deviceid=cp3Mvh7aF0HWvoYmymkjF8hlRJrKFfKVoLB%2BJeerMqgmiahmSXbkf35ND%2BYmMc9Z; wmda_uuid=57aa741ccc8947f8344a4d1bd77f9113; wmda_new_uuid=1; gr_user_id=5d8d983a-96d9-431d-b81f-185f802c5695; mcity=wh; mcityName=%E6%AD%A6%E6%B1%89; nearCity=%5B%7B%22cityName%22%3A%22%E6%AD%A6%E6%B1%89%22%2C%22city%22%3A%22wh%22%7D%5D; Hm_lvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1556098240; cookieuid1=mgjwFVzALL4ODHp9A1s4Ag==; scancat=13915; sessionid=383656a6-92ab-4066-941b-099d2c6c4900; www58com="UserID=43101834184718&UserName=tvxxvc"; 58cooper="userid=43101834184718&username=tvxxvc"; 58uname=tvxxvc; wmda_visited_projects=%3B1731916484865%3B6333604277682%3B2286118353409%3B3381039819650%3B4200524323842%3B4785068453378%3B7790950805815; vip=vipusertype%3D11%26vipuserpline%3D0%26v%3D1%26vipkey%3Dec4ce014365e10286fbb2df23a66a9e9%26masteruserid%3D43101834184718; showOrder=1; 58home=wh; city=wh; xxzl_smartid=5bde2f5023f300d952dd88072029498f; showPTTip=1; ljrzfc=1; bProtectShowed=true; ppStore_fingerprint=860F18A32617495B64C24011EAA3E9CC3C5F76C9BF0DD291%EF%BC%BF1558506851172; PPU="UID=43101834184718&UN=tvxxvc&TT=e13a4bf2f4521dae3d1754a63cdbaea3&PBODY=Ijs-FeB5pqUGFjC_dvgy__My-X5njoSfX_0M8aTKhv2JC4MeBf8p5cc_mb92bCHdTf4_qgb9aasiprisDMEbdHmIp98yUjIoazfWWe_KNMZAwxAcFQMtF-408hmVeIbeLadxwOurffgp-ze6xncDSrafaMzZJWDBpOaaudGiftc&VER=1"; new_uv=40; utm_source=; spm=; init_refer=https%253A%252F%252Femployer.58.com%252Fresumesearch%253FPGTID%253D0d000000-0000-08f1-e2b6-e3b666dda683%2526ClickID%253D29; wmda_session_id_1731916484865=1558515004760-927f44cb-ed8f-a5b0; new_session=0',
            'pragma': 'no-cache',
            'referer': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-0f7d-5880-bbccd08216eb&ClickID=104',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.driver = None
        self.cookies = None
        self.call_login_times = 0
        self.login()

    def login(self):
        l =  self.l
        self.call_login_times += 1
        if self.call_login_times > 10:
            l.info(f"login be called: {self.call_login_times}, exit...")
            sys.exit()

        if not self.cookies:
            for _ in range(10):
                l.info(f"no cookies, starting {_+1}/10 login...")
                cookies =  self._login()
                if cookies:
                    self.cookies = cookies
                    self.s.cookies = requests.utils.cookiejar_from_dict(cookies)
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
        driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/span')[0].click()
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

        driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div[2]')[0].click()
        time.sleep(5)
        driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[2]/ul/li[1]/div[1]/div[3]/p[1]/span[1]')[
            0].click()
        # cookie_str = driver.execute_script('return document.cookie')
        cookies = {i['name']: i['value'] for i in driver.get_cookies()}
        driver.quit()
        return cookies

    def gene_jq_name(self):
        _1 = (str(random.random()) + str(random.random())).replace('0.', '')[3:24]
        _2 = str(int(time.time() * 1000))
        'jQuery180024326300832150838_1557039752063'
        return 'jQuery' + _1 + '_' + _2

    def query_list_page(self, keyword, page_to_go):
        '''58job HTML'''
        # keyword:  159+3084
        l = self.l
        l.info(str([keyword, page_to_go]))

        cid = 158  # 158是武汉，暂时只是抓取武汉
        aid, nid = keyword.strip().split('+')

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
            'resumeSort': 'intelligent',
            'update24Hours': '1',
            'keyword': '',
            'pageSize': '70',
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
            l.info(f'{"*"*5}  get job detail success, len:{len(conn)} {"*"*5}')
            print(conn)
            sys.exit()
            return conn
        return ''

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

    def resource_page(self, res, raw):
        l = self.l
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
            res = res.replace('&#x{};'.format(i), font)
        return res

    def query_detail_page(self, url):
        '''
        打开58job详情页面
        '''
        l = self.l
        # self.session.headers['User-Agent'] = random_ua()
        # https://jianli.58.com/resumedetail/single/3_neyQ_EHunGZanGOpnvr5lEDkTvmQnem5nePknpsfTedYnGnsMG6vMGHplEOsnErsThsfTEdaTm**?sourcepath=pc-viplist-zhineng&followparam=%7B%22searchID%22%3A%2206ca2519d3974dcd98f42181239cc950%22%2C%22searchVersion%22%3A31103%2C%22searchAreaID%22%3A4554%2C%22searchFirstAreaID%22%3A158%2C%22searchPositionID%22%3A0%2C%22searchSecondPositionID%22%3A0%2C%22page%22%3A1%2C%22location%22%3A4%2C%22resumeType%22%3A1%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-viplist-zhineng%22%2C%22operatePage%22%3A%22list%22%7D

        retry_time = 15
        time.sleep(6)

        resumeId = re.findall('single/(.*?)\?', url)
        if not resumeId:
            raise Exception('invalid url...')
        resumeId = resumeId[0]
        l.info(f'resumeId: {resumeId}')

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

            l.info(f'{"*"*5} get detail success, len:{len(conn)} {"*"*5}')
            conn = self.resource_page(conn, self.raw)
            view = self.__get_view(resumeId)
            conn = f'{conn}+d135638806955c0ee9d255c64a952705+{view}'
            if '可能被删除、关闭或根本不存在' in conn:
                l.info('简历可能被删除、关闭或根本不存在')
                return ''
            if '<title>用户登录-58同城</title>' in conn:
                l.info('可能cookies过期，需要重新登录')
                # self.cookies = None
                self.proxy = {}
                self.need_login_times += 1
                if self.need_login_times > 3:
                    raise ('可能cookies过期，需要重新登录')
            return conn
            # print(conn)
            # sys.exit(6666)
        return ''


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
