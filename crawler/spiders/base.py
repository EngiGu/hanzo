import datetime
import os
import sys
import time

import requests

from config import PROXY_URL
# from core.logger import Logger
# from core.base import Base
# import logging
#
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')



# def try_catch(pid):
#     def debug(func):
#         # @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             pid = os.getpid()
#             print(pid)
#             l = args[0].l
#             func_name = func.__qualname__
#             # l.info("enter {}()".format(func_name))
#             l.info('{} pid:{} key: {}, await 7s for page content'.format(func_name, pid, args[-1]))
#             # print(*args)
#             # for i in dir(func):
#             #     print('func.' + i + ' ---- ', eval('func.' + i))
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 l.info('{} pid:{} error ===>>> {}'.format(func_name, pid, str(e)))
#             l.info('{} key: {}, crawl end...'.format(func_name, args[-1]))
#
#         return wrapper
#
#     return debug



class SpiderBase():
    selenium = False
    name = 'base'

    def __init__(self, logger=None):
        # self.name = 'base'
        self.l = logger if logger else logging
        self.driver = None
        self.pid = os.getpid()
        self.s = requests.session()
        self.proxy = {}
        self.proxy_fa = 0
        self.change_proxy_times = 0
        self.retry_get_proxy_times = 20
        self.retry_send_request_times = 20
        self.proxy_api = PROXY_URL

    def get_proxy(self):
        l = self.l
        if self.proxy and self.proxy_fa < 3:
            return self.proxy
        for _ in range(self.retry_get_proxy_times):
            try:
                l.info(f"start get proxy...")
                ret_ip = requests.get(self.proxy_api, timeout=10)
                IP = ret_ip.text.strip()
                proxies = {"http": "http://%s" % IP, "https": "https://%s" % IP}
                self.proxy = proxies
                self.proxy_fa = 0
                self.change_proxy_times += 1
                return proxies
            except Exception as e:
                l.warning(f"query: {self.proxy_api}, get proxy error, sleep 5s and try again.... {str(e)}")
                time.sleep(5)
        # 代理api挂掉
        raise Exception(f"failed to ge proxy after {self.retry_get_proxy_times} times....")

    def send_request(self, method, **kwargs):
        l = self.l
        func_dict = {
            'get': self.s.get,
            'post': self.s.post
        }

        method = method.lower()
        func = func_dict.get(method, None)
        if not func:
            raise Exception('method:{} error'.format(method))
        
        try:
            kwargs.pop('verify')
        except:
            pass

        if kwargs.get('timeout', None):
            kwargs['timeout'] = 30

        for _ in range(self.retry_send_request_times):
            proxies = self.get_proxy()
            kwargs['proxies'] = proxies
            l.info(
                f'{self.name}:{self.pid} -> query: {_+1}, change proxy times: {self.change_proxy_times}, proxy failed times: {self.proxy_fa}, '
                f'current proxy: {str(proxies).replace(" ", "")}')
            try:
                res = func(**kwargs)
                return res
            except Exception as e:
                self.proxy_fa += 1
                l.warning(f"query page error, sleep 5s and try again.... {str(e)}")
                time.sleep(5)

        raise Exception(f"failed to get page response after {self.retry_send_request_times} times....")

    def query_list_page(self, key, page):
        pass

    def query_detail_page(self, url):
        pass
