import hashlib
import json
from lxml import etree
from core.base import Base


class ListToUrl(Base):

    def get_hashkey(self, resume):
        hashed_key = hashlib.md5(json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-8]
        hashed_id = int(hashed_key, 16)
        return hashed_id

    def parser(self, page):
        """
        :param page:
        :return:  hashed_key 为url去重的关键字
        """
        tree = etree.HTML(page)
        result = tree.xpath('//div[@class="job-list"]//li')[0]
        resumes = []
        resume = {}
        resume['company'] = result.xpath('.//div[@class="info-company"]//h3[@class="name"]/a/text()')[0].strip() if result.xpath('.//div[@class="info-company"]//h3[@class="name"]/a/text()') else ''
        resume['url'] = ("https://www.zhipin.com" + result.xpath('.//div[@class="info-company"]//h3[@class="name"]/a/@href')[0].strip()) if result.xpath('.//div[@class="info-company"]//h3[@class="name"]/a/@href') else ''
        resume['info'] = result.xpath('.//div[@class="info-company"]/p')[0].xpath('string()').replace(" ", "").replace("\n", "").strip() if result.xpath('.//div[@class="info-company"]/p') else ''
        resume["hashed_key"]= self.get_hashkey(resume)
        resumes.append(resume)
        result = {
            "resume_list": resumes,  # [{},{},{}]
            "current_page": 1,
            "last_page": 1
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('boss_2.html','r', encoding="utf-8") as f:
        page = f.read()
    url = 'https://www.zhipin.com'
    print(a.parser(page))
