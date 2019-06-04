import os
import random

import logging
import requests
from core.base import Base

try:
    from .base import *
except:
    from base import *


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')

import logging

class LaGou(SpiderBase, Base):
    name = 'lagou'


    def __init__(self, logger=None):
        super(LaGou, self).__init__(logger)


    def open_search_home(self):
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        args = {
            "url": "https://www.lagou.com/gongsi/",
            "headers": headers
         }
        self.send_request("get", **args)

    def query_list_page(self, key, page_to_go):

        headers = {
            'Origin': 'https://www.lagou.com',
            'X-Anit-Forge-Code': '0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/gongsi/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'X-Anit-Forge-Token': 'None',
        }

        data = {
            'first': 'false',
            'pn': str(page_to_go),
            'sortField': '0',
            'havemark': '0'
        }
        # retry_times = 10
        retry_times = 0
        frequence_time = 0
        while True:
            if retry_times >= 20:
                self.l.info("no result with 10 times retry")
                break
            try:
                args = {
                    "url": f'https://www.lagou.com/gongsi/{key}.json',
                    "headers": headers,
                    "data": data
                }
                retry_times += 1
                self.s.cookies = requests.utils.cookiejar_from_dict({})  # 置空cookies
                self.open_search_home()
                res = self.send_request("post", **args)
            except Exception as e:
                continue
            # {
            #     "status": false,
            #     "msg": "您操作太频繁,请稍后再访问",
            #     "clientIp": "221.234.157.165",
            #     "state": 2403
            # }
            if (res.status_code == 200):
                if "result" in res.text:
                    self.l.info("search success !!!")
                    return res.text
                elif "操作太频繁" in res.text:
                    self.l.info(f"操作太频繁:{frequence_time}")
                    # 直接更换代理
                    self.proxy_fa = 10
                    self.proxy = {}
                    continue
                else:
                    self.l.info("公司的搜索页面有问题")
                    self.proxy_fa = 10
                    self.proxy = {}
                    continue
            else:
                self.l.error(f"response status_code is wrong:{res.status_code}")
                # 直接更换代理
                self.proxy_fa = 10
                self.proxy = {}
                continue
        return ""



    def query_detail_page(self, url):
        l = self.l

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        # response = self.session.get(url, headers=headers, timeout=30)

        args = {
            "url": url,
            "headers": headers
        }

        retry_times = 0
        while True:
            if retry_times >= 20:
                self.l.info("no result with 10 times retry")
                break
            try:
                retry_times += 1
                self.s.cookies = requests.utils.cookiejar_from_dict({})  # 重置cookies
                self.open_search_home()
                response = self.send_request("get", **args)
            except Exception as e:
                continue
            if (response.status_code == 200):
                if "公司主页" in response.text:
                    l.info("search success !!!")
                    return response.text
                elif ("封禁" in response.text) or ("请按住滑块，拖动到最右边" in response.text) or ("存在异常访问行为" in response.text):
                    l.info(f"ip被封禁了")
                    # 直接更换代理
                    self.proxy_fa = 10
                    self.proxy = {}
                    continue
                else:
                    l.info("公司的搜索页面有问题")
                    self.proxy_fa = 10
                    self.proxy = {}
                    continue
            else:
                l.error(f"response status_code is wrong:{response.status_code}")
                # 直接更换代理
                self.proxy_fa = 10
                self.proxy = {}
                continue
        return ""


if __name__ == '__main__':
    # l = DaJie()
    # l.run(['112233'])
    pass
