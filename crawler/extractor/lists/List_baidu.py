import hashlib
import json
import sys
import logging

from lxml import etree
from core.base import Base


class ListToUrl(Base):

    def get_hashkey(self, resume):
        hashed_key = hashlib.md5(json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-8]
        hashed_id = int(hashed_key, 16)
        return hashed_id

    def parser(self, page):
        """数据为html格式"""
        # return        {
        #     "resume_list": [{'url': 'tests_url', 'hashed_key': '823hhjjkkjdffdsgd'}],
        #     "current_page": 1,
        #     "last_page": 10
        # }

        result = {
            "resume_list": [],
            "current_page": 1,
            "last_page": 1
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('baidu_1.html','r', encoding="utf-8") as f:
        page = f.read()
    print(a.parser(page))
