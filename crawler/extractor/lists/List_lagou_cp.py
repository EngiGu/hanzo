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
        try:
            res_json = json.loads(page)
        except Exception as e:
            logging.error(e)
            return {
            "resume_list": [],
            "current_page": 1,
            "last_page": 1
        }
        curr_page = res_json.get("pageNo", 1)
        totalCount = res_json.get("totalCount", 16)
        result = res_json.get("result", [])
        total_page = round(int(totalCount)//16)
        if total_page:
            if total_page> 60:
                last_page = 60
            else:
                last_page = total_page
        else:
            last_page = 1

        resumes = []
        for one in result:
            resume = {}
            resume['company'] = one.get("companyFullName", "")
            company_id = one.get("companyId", 0)
            resume['url'] = f"https://www.lagou.com/gongsi/{company_id}.html" if company_id else ""
            resume['info'] = one.get("companyFeatures", "")
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
    with open('lagou_1.html','r', encoding="utf-8") as f:
        page = f.read()
    print(a.parser(page))
