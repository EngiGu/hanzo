from core.base import Base
import time
import requests
import json
import re
try:
    from .base import *
except:
    from base import *


def check(func):
    def wapper(self, *args, **kwargs):
        max_retry_times = 5  # 请求失败后重试次数
        retry_times = 0
        while True:
            if max_retry_times <= retry_times:
                break
            type, response = func(self, *args, **kwargs)
            if response.status_code == 200:
                res = response.text.encode('utf-8').decode('unicode_escape').replace("\\", "")
                return res
            else:
                self.l.info(f"site:{type} is false")
                self.l.info(response.status_code)
                retry_times += 1
                self.login()
                self.l.info(f"now retry counts :{retry_times}")
            time.sleep(2)
        return False
    return wapper


class JuZi(SpiderBase, Base):
    name = 'juzi'

    def __init__(self, logger=None):
        super(JuZi, self).__init__(logger)
        self.token = ""
        self.login()

    def query_list_page(self, key, page_to_go):
        pass

    def login(self):
        headers = {
            'Origin': 'https://www.itjuzi.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'CURLOPT_FOLLOWLOCATION': 'true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.itjuzi.com/login?url=%2Fcompany',
            'Connection': 'keep-alive',
        }
        data = '{"account":"15948430604","password":"jianxun123"}'
        response = requests.post('https://www.itjuzi.com/api/authorizations', headers=headers, data=data)
        res = response.text.encode('utf-8').decode('unicode_escape').replace("\\", "")
        if res:
            res_t = json.loads(res)
            self.token = res_t.get("data").get("token")
            self.l.info("login success")
        else:
            raise Exception("login failed!")
        return response

    @check
    def get_info(self, id ,type_str):

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.itjuzi.com/company/34629354',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'CURLOPT_FOLLOWLOCATION': 'true'
        }
        params = (
            ('type', type_str),
        )
        if type_str == "commerce":
            headers["Authorization"] = self.token
            response = requests.get(f'https://www.itjuzi.com/api/companies/{id}/commerce', headers=headers, timeout=20)
        else:
            response = requests.get(f'https://www.itjuzi.com/api/companies/{id}', headers=headers, params=params, timeout=20)
        return type_str, response

    def remove_xa0(self, _str):
        move = dict.fromkeys((ord(c) for c in "\xa0"))
        return _str.translate(move).strip()

    def query_detail_page(self, url):
        l = self.l
        self.l.info(f"now is :https://www.itjuzi.com/company/{url}")
        result = {}
        for type in ["basic", "contact", "person", "commerce"]:  # "basic", "contact", "person",
            res = self.get_info(url, type)
            if res:
                res = res.replace("\r\n", "").replace("\n\t", "").replace("\t", "").replace("\n", "")
                new_res = re.sub(r'<.*?>', "", res)
                try:
                    result[type] = json.loads(self.remove_xa0(new_res))
                except Exception as e:
                    print(e)
                    print(res)
                    print("************")
                    new_res = re.sub(r'<.*?"', "", new_res)
                    print(new_res)
                    result[type] = json.loads(new_res)
        new_res = json.dumps(result, ensure_ascii=False)
        return new_res


if __name__ == '__main__':
    a = JuZi()
    for id in range(1,1000):
        res = a.query_detail_page(id)
        # print(res)
        print(f"success: {id}")
        time.sleep(1)
        with open(f"{id}.text", mode="w", encoding="utf-8") as f:
            f.write(res)