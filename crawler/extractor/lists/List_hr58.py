import hashlib
import json
import sys

from lxml import etree
from core.base import Base


class ListToUrl(Base):

    def get_hashkey(self, resume):
        hashed_key = hashlib.md5(json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[
                     8:-8]
        hashed_id = int(hashed_key, 16)
        return hashed_id

    def first(self, xpath_res):
        return xpath_res[0].strip() if xpath_res else ''

    def parser(self, page):
        """数据为html格式"""

        tree = json.loads(page)
        # base_url = 'http://www.rencaiaaa.com/rdetail/searchRencaiDetail.do?' \
        #              'ext={ext}&resumeType={resumetype}&rid={rid}' \
        #              '&updateDate={date}&updateDateFlag={flag}'
        resume_list = tree["data"].get("resumeList", [])
        # current_page = int(tree.get("pageindex", "1"))
        current_page = int(tree['index'])
        # last_page = round(int(tree["data"].get("count", "0")) / 50)
        last_page = 30

        resumes = []
        for res in resume_list:
            resume = {}
            resume['resume_id'] = res.get("resumeID", "")
            resume['url'] = res.get("url", "")
            if len(resume['url']):
                resume['url'] = "https:" + resume['url']
            resume["hashed_key"] = self.get_hashkey(resume)
            resumes.append(resume)
        result = {
            "resume_list": resumes,
            "current_page": current_page,
            "last_page": last_page,
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('dajie_1.html', 'r', encoding="utf-8") as f:
        page = f.read()
    url = 'https://www.zhipin.com'
    print(a.parser(page))
