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

        if '搜索信息获取失败' in page:  # 超过翻页限制异常
            return {
                "resume_list": [],
                "current_page": 1,
                "last_page": 1
            }

        res = json.loads(page)
        curr_page = res['index']  # 页面返回没有这个，spider从任务添加这字段
        # total_page = 1000 # 测试限制在1000页
        # total_page = int(total_page)
        # print(total_page, curr_page)
        # sys.exit()
        result = json.loads(res['data'])['company']['infos']
        total_page = json.loads(res['data'])['company']['count']
        total_page = int(total_page) // 10 + 1
        print(total_page, curr_page)
        resumes = []
        for one in result:
            resume = {}
            resume['company'] = one['name']
            resume['url'] = 'https://www.innotree.cn/inno/company/%s.html' % one['ncid']
            resume["hashed_key"] = self.get_hashkey(resume)
            resumes.append(resume)
        result = {
            "resume_list": resumes,
            "current_page": curr_page,
            "last_page": total_page
        }
        return result


if __name__ == '__main__':
    a = ListToUrl()
    with open('./tmp/yinguo_1.html', 'r', encoding="utf-8") as f:
        page = f.read()
    url = 'https://www.zhipin.com'
    print(a.parser(page))
