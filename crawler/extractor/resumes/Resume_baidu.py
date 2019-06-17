#! /usr/bin/env python3
# coding=utf-8

try:
    from .resume_base import BaseExtract
except:
    from resume_base import BaseExtract
from core.base import Base
import json


class HtmlToDict(BaseExtract, Base):

    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        self.content = html_doc.get("content", "")
        res = self.content
        try:
            resume = json.loads(res)
            return resume
        except Exception as e:
            return None


def main():
    with open('lagou_1.html', mode='r+',encoding="utf-8") as f:
        info = f.read()
    # print(info)
    h = HtmlToDict()
    print(h)
    h.debug = False
    if h.load_html(info):
        h.resume_info()  # 调核心解析函数
        print(h.resume)
    return


if __name__ == '__main__':
    main()




