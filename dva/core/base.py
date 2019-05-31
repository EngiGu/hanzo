import asyncio
import time
import logging

import requests
from settings import PROXY_URL

class Base:

    def __init__(self):
        self.name = 'base'
        self.driver = None
        # self.pid = os.getpid()
        # self.s = requests.session()
        self.s = requests
        self.proxy = {}
        self.l = logging
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
                l.warn(f"query: {self.proxy_api}, get proxy error, sleep 5s and try again.... {str(e)}")
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

        for _ in range(self.retry_send_request_times):
            proxies = self.get_proxy()
            kwargs['proxies'] = proxies
            l.info(
                f'{self.name} -> query: {_ + 1}, change proxy times: {self.change_proxy_times}, proxy failed times: {self.proxy_fa}, '
                f'current proxy: {str(proxies).replace(" ", "")}')
            try:
                res = func(**kwargs)
                return res
            except Exception as e:
                self.proxy_fa += 1
                l.warn(f"query page error, sleep 5s and try again.... {str(e)}")
                time.sleep(5)

        raise Exception(f"failed to get page response after {self.retry_send_request_times} times....")

    async def query_list(self):
        pass

    async def query_detail(self):
        pass

    async def run(self):
        pass


if __name__ == '__main__':
    b = Base()
