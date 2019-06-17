from core.base import Base
import re
import json
import time

try:
    from .base import *
except:
    from base import *


class BaiDu(SpiderBase, Base):
    name = 'baidu_photo'

    def __init__(self, logger=None, *args):
        super(BaiDu, self).__init__(logger, *args)

    def query_list_page(self, key, page_to_go):
        return ""

    def extractor_photo(self, html_s, name):
        """
        :param html: text
        :return: {}
        """

        html = "".join(html_s.split())
        # print(html)
        res = re.findall(r"app.setData\('imgData',(.*?\})\);", html)[0]
        res = res.replace("\\", "").replace("<strong>", "").replace("</strong>", "").replace("\n", "").replace("\'", "\"")
        res = re.sub(r'(\w)"(\w)', "\g<1>'\g<2>", res)
        res = res.replace("\".", "").replace("\"?", "")
        res_dic = json.loads(res)
        datas = res_dic.get("data")
        res = {}
        photo_url_list = []
        res["source"] = 303
        res["full_name"] = name
        res["update_time"] = int(time.time())
        for photo_infos in datas:
            photo_url = photo_infos.get("middleURL", "")
            photo_desc = photo_infos.get("fromPageTitle", "")
            if name in photo_desc:
                photo_url_list.append(photo_url)
        res["photo_urls"] = photo_url_list
        return res

    def query_detail_page(self, url):
        l = self.l

        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1560758575606_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E6%AD%A6%E6%B1%89%E6%99%BA%E5%AF%BB%E5%A4%A9%E4%B8%8B%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = (
            ('tn', 'baiduimage'),
            ('ipn', 'r'),
            ('ct', '201326592'),
            ('cl', '2'),
            ('lm', '-1'),
            ('st', '-1'),
            ('fm', 'result'),
            ('fr', ''),
            ('sf', '1'),
            ('fmq', ''),
            ('pv', ''),
            ('ic', ''),
            ('nc', '1'),
            ('z', ''),
            ('hd', ''),
            ('latest', ''),
            ('copyright', ''),
            ('se', '1'),
            ('showtab', '0'),
            ('fb', '0'),
            ('width', ''),
            ('height', ''),
            ('face', '0'),
            ('istype', '2'),
            ('ie', 'utf-8'),
            ('ctd', ''),
            ('sid', ''),
            ('word', url),
        )

        response = requests.get('https://image.baidu.com/search/index', headers=headers, params=params)
        try:
            res = self.extractor_photo(response.text, url)
            return json.dumps(res, ensure_ascii=False)
        except Exception as e:
            l.error(e)
        return ""

if __name__ == '__main__':
    a = BaiDu()
    res = a.query_detail_page("中交水运规划设计院有限公司")
    print(res)
