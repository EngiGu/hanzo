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
        try:
            res_json = json.loads(page)
        except Exception as e:
            logging.error(e)
            return result

        data = res_json.get("data", {})
        if not len(data):
            return result
        page = data.get("page")
        total_count = page.get("total")
        curr_page = int(page.get("page"))
        totalCount = round(int(total_count)//20)
        if totalCount:
            last_page = totalCount
        else:
            last_page = 1

        result = data.get("data", [])
        resumes = []
        for one in result:
            resume = {}
            resume['company'] = one.get("register_name", "")
            company_id = one.get("id", 0)
            resume['url'] = f"https://www.itjuzi.com/company/{company_id}" if company_id else ""
            resume['info'] = one.get("des", "")
            resume["hashed_key"]= self.get_hashkey(resume)
            resumes.append(resume)
        result = {
            "resume_list": resumes,
            "current_page": curr_page,
            "last_page": last_page
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('juzi_1.html','r', encoding="utf-8") as f:
        page = f.read()
    print(a.parser(page))
