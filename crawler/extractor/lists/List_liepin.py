import hashlib
import json
import sys
import logging

from lxml import etree
from core.base import Base
import re


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
            tree = etree.HTML(page)
        except Exception as e:
            logging.error(e)
            return {
            "resume_list": [],
            "current_page": 1,
            "last_page": 1
        }
        curr_page_ele = tree.xpath('//span[@class="page-number page-current"]/a/text()')
        curr_page = curr_page_ele[0] if curr_page_ele else 1
        last_page_page_ele = tree.xpath('//span[@class="page-next"]/a[starts-with(text(),"末页")]/@href')
        last_page = int(re.findall(r'curPage=(\d+)', last_page_page_ele[0])[0])+1 if last_page_page_ele else int(curr_page)
        result = tree.xpath('//div[@class="jobs-list"]/dl')
        resumes = []
        for one in result:
            resume = {}
            resume['company'] = one.xpath('./dd//a/text()')[0]
            resume['url'] = one.xpath('./dd//a/@href')[0]
            resume['info'] = one.xpath('./dd[@class="detail"]')[0].xpath('string()').replace("\t", "").replace("\n", "").replace("\xa0", "").strip()
            resume["hashed_key"]= self.get_hashkey(resume)
            resumes.append(resume)
        result = {
            "resume_list": resumes,
            "current_page": int(curr_page),
            "last_page": last_page
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('./tmp/liepin_1.html','r', encoding="utf-8") as f:
        page = f.read()
    print(a.parser(page))
