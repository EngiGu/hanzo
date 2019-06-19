from core.base import Base

try:
    from .base import *
except:
    from base import *


class Liepin(SpiderBase, Base):
    name = 'lagou'


    def __init__(self, logger=None, *args):
        super(Liepin, self).__init__(logger, *args)


    def query_list_page(self, key, page_to_go):
        l = self.l
        dq, industry = key.split("+")
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://www.liepin.com/company/so/?pagesize=30&keywords=&dq=280020&industry=030',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        params = (
            ('pagesize', '30'),
            ('keywords', ''),
            ('dq', dq),
            ('industry', industry),
            ('curPage', page_to_go),
        )
        response = requests.get('https://www.liepin.com/company/so/', headers=headers, params=params, proxies=self.proxy, timeout=30)
        proxy_change_time = 0
        while True:
            if proxy_change_time >= 20:
                l.info("20 times retry with no right response~")
                break
            try:
                self.get_proxy()
                proxy_change_time += 1
                response = requests.get('https://www.liepin.com/zhaopin/', headers=headers, params=params,
                                        proxies=self.proxy, timeout=30)
            except:
                self.proxy_fa += 1  # 当代理不可用时计数加一
                time.sleep(1)
                continue
            if response.status_code == 200:
                if "末页" in response.text:
                    print("search success!!!")
                    return response.text
                elif "没有符合搜索条件的企业" in response.text:
                    l.info(f"没有符合搜索条件的企业:{key}")
                    return ""
                else:
                    l.info("公司的搜索页面有问题")
                    l.info(f"res is:{response.text}")
                    self.proxy = {}
                    continue
            else:
                l.error(f"response status_code is wrong:{response.status_code}")
                self.proxy = {}
                continue
        return ""



    def query_detail_page(self, url):
        l = self.l
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        proxy_change_time = 0
        while True:
            if proxy_change_time >= 20:
                l.info("20 times retry with no right response~")
                break
            try:
                self.get_proxy()
                proxy_change_time += 1
                response = requests.get(url, headers=headers, proxies=self.proxy, timeout=30)
            except:
                self.proxy_fa += 1  # 当代理不可用时计数加一
                time.sleep(1)
                continue
            if response.status_code == 200:
                if "招聘职位" in response.text:
                    print("resume success!!!")
                    return response.text
                else:
                    l.info(f'请求的url:{url}')
                    l.info("公司的详情页面有问题")
                    self.proxy = {}
                    continue
            else:
                l.error(f"response status_code is wrong:{response.status_code}")
                self.proxy = {}
                continue
        return ""


if __name__ == '__main__':
    l = Liepin()
    res_list = l.query_list_page("050090110+400", 1)
    print(res_list)
    res_resume = l.query_detail_page("https://www.liepin.com/company/8051055/")
    print(res_resume)