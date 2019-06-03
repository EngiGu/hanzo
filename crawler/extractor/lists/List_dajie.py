import hashlib
import json
import sys

from lxml import etree
from core.base import Base


class ListToUrl(Base):

    def get_hashkey(self, resume):
        hashed_key = hashlib.md5(json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-8]
        hashed_id = int(hashed_key, 16)
        return hashed_id

    def first(self, xpath_res):
        return xpath_res[0].strip() if xpath_res else  ''


    def parser(self, page):
        """数据为html格式"""
        # return        {
        #     "resume_list": [{'url': 'tests_url', 'hashed_key': '823hhjjkkjdffdsgd'}],
        #     "current_page": 1,
        #     "last_page": 10
        # }
        tree = etree.HTML(page)
        result = tree.xpath('//div[@class="listBox"]/ul/li')
        # print(len(result))
        curr_page = tree.xpath('//div[@class="paging"]/span[@class="current"]/text()')[0]
        curr_page = int(curr_page)
        # print(curr_page)
        total_page = tree.xpath('//div[@class="paging"]/a[@class="next"]/preceding-sibling::a[1]/text()')[0]
        total_page = int(total_page)
        # print(total_page)
        # sys.exit()
        resumes = []
        for one in result:
            resume = {}
            resume['company'] = one.xpath('.//p[@class="job-name"]//a/text()')
            resume['company'] = self.first(resume['company'])
            resume['url'] = one.xpath('.//p[@class="job-name"]/span[@class="attention"]/@data-corp-id')
            resume['url'] = 'https://www.dajie.com/corp/%s/index/intro' % self.first(resume['url'])
            resume["hashed_key"]= self.get_hashkey(resume)
            resumes.append(resume)
        result = {
            "resume_list": resumes,
            "current_page": curr_page,
            "last_page": total_page
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('dajie_1.html','r', encoding="utf-8") as f:
        page = f.read()
    url = 'https://www.zhipin.com'
    print(a.parser(page))
