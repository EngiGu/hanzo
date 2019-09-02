import datetime
import os
import sys
import time
import logging
import requests

from config import PROXY_URL


class SpiderBase():
    selenium = False
    name = 'base'

    def __init__(self, logger=None, account=None):
        # self.name = 'base'
        self.l = logger if logger else logging
        self.driver = None
        self.account = account
        self.pid = os.getpid()
        self.s = requests.session()
        self.proxy = {}
        self.proxy_fa = 0
        self.change_proxy_times = 0
        self.retry_get_proxy_times = 20
        self.retry_send_request_times = 20
        self.proxy_api = PROXY_URL
        self.proxy_request_delay = 5

    def get_proxy(self):
        l = self.l
        if self.proxy and self.proxy_fa < 3:
            return self.proxy

        for _ in range(self.retry_get_proxy_times):
            try:
                l.info(f"start get proxy...")
                ret_ip = requests.get(self.proxy_api, timeout=10)
                # IP = ret_ip.text.strip()
                IP = ret_ip.json()['proxy']
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

        lineno = sys._getframe().f_back.f_lineno
        called_func = sys._getframe().f_back.f_code.co_name

        method = method.lower()
        func = func_dict.get(method, None)
        if not func:
            raise Exception('method:{} error'.format(method))

        try:
            kwargs.pop('verify')
        except:
            pass

        if not kwargs.get('timeout', None):
            kwargs['timeout'] = 30

        for _ in range(self.retry_send_request_times):
            proxies = self.get_proxy()
            kwargs['proxies'] = proxies
            l.info(
                f'{self.name} pid:{self.pid} -> retry: {_+1}, change: {self.change_proxy_times}, failed: {self.proxy_fa}, '
                f'current: {proxies["http"]}, called: {called_func}:{lineno}')
            try:
                res = func(**kwargs)
                self.proxy_fa = 0
                return res
            except Exception as e:
                self.proxy_fa += 1
                l.warning(f"request error: {e.__context__}")
                if self.proxy_request_delay:
                    l.info(f"send request sleep {self.proxy_request_delay}s.")
                    time.sleep(self.proxy_request_delay)

        raise Exception(f"failed to get page response after {self.retry_send_request_times} times....")

    def query_list_page(self, key, page):
        pass

    def query_detail_page(self, url):
        pass
