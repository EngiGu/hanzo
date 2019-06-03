#! /usr/bin/env python3
# coding=utf-8

from .resume_base import BaseExtract
import time
import re
from core.base import Base
from config import SITE_SOURCE_MAP

class HtmlToDict(BaseExtract, Base):

    def set_unix_time(self, str_time):
        # 2010年3月
        # 2012-05-08 > 15524789624
        return int(time.mktime(time.strptime(str_time, "%Y年%m月")))

    # 2/14
    def resume_info(self):
        """独立的解析函数"""
        tree = self.tree
        company_busness_info = tree.xpath('//div[@class="job-sec company-business"]')
        if company_busness_info:
            company_busness_info = company_busness_info[0]

            found_time = company_busness_info.xpath('.//li[starts-with(text(),"注册时间：")]/text()').replace("注册时间：", "").strip()
            self.found_time = self.set_unix_time(found_time[0]) if found_time else ""
            type = company_busness_info.xpath('.//p[@class="financing-info-summary"]')[0].xpath('./span/text()')[0]
            self.type = type[0] if type else ""

        head_address = tree.xpath('//ul[@class="new-compintro"]/li[@data-selector="company-address"]/text()')
        self.head_address = head_address[0] if head_address else ""
        office_cities = None  # 暂时没看到分布信息
        self.office_cities = office_cities if office_cities else []

        short_name = tree.xpath('//div[@class="name-and-welfare"]/h1/text()')
        self.short_name = short_name[0] if short_name else ""
        industry = tree.xpath('//div[@class="comp-summary-tag"]/a/text()')  # 上市  | 10000人以上 | 北京 | 互联网/电子商务
        self.industry = industry[3] if industry else ""
        tag = tree.xpath('//div[@class="comp-tag-box"]//li/span/text()')
        self.tag = tag if tag else ""
        introduce = tree.xpath('//div[@class="company-introduction clearfix"]/p[@class="profile"]/text()')
        self.introduce = introduce[0].replace("\n", "").strip() if introduce else ""
        full_name = re.findall(r'（全称(.*)?）', self.introduce)
        self.full_name = full_name[0] if full_name else ""
        if not self.full_name:
            self.full_name = self.short_name
        self.url = ""
        original_url = tree.xpath('//link[@rel="alternate"]/@href')
        self.origin_url = original_url[0] if original_url else "" # https://www.zhipin.com/gongsi/6f1aa1d6b1d033ad33B43N0~.html
        self.develops = []
        develop = {}
        develop["scale"] = self.company_scale_map(industry[1]) if industry else ""  #  映射
        develop["invest"] = self.type
        develop["state"] = 1  # 0 表示倒闭
        develop["create_time"] = self.found_time
        develop["update_time"] = int(time.time())
        self.develops.append(develop)
        self.id = self.create_hash_id(self.full_name, self.origin_url, str(self.source))
        self.logo = tree.xpath('//img[@class="bigELogo"]/@src')[0] if tree.xpath('//img[@class="bigELogo"]/@src') else ""
        self.resume = {
                "id": self.id,  # 字符串
                "full_name": self.full_name,  # 字符串
                "short_name": self.short_name,  # 字符串
                "industry": self.industry,  # 字符串
                "found_time": self.found_time,  # 字符串2019-01-01
                "type": self.type,  #todo  字符串or map
                "introduce": self.introduce,
                "tag": self.tag,  # 标签
                "url": self.url,  # 公司主页
                "origin_url": self.origin_url,  # 原始网页
                "head_address": self.head_address,
                "office_cities": self.office_cities,
                "source": self.source,  # 来源
                "develops": self.develops,
                "logo": self.logo,
                "productions": self.productions,
                "cxos": self.cxos
            }
        jx_resume_id = self.set_jx_resume_id(self.resume)  # 获取jx_resume_id
        self.resume["jx_resume_id"] = jx_resume_id
        return

    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        site = html_doc.get("site")
        # SITE_SOURCE_MAP = {
        #     "lagou": 201,
        #     "job51": 205
        # }
        self.source = SITE_SOURCE_MAP.get(site)
        self.content = html_doc.get("content", "")
        if self.load_html(page_source=self.content):
            self.resume_info()  # 调核心解析函数
            return self.resume
        else:
            return None


def main():
    with open('liepin_1.html', mode='r+',encoding="utf-8") as f:
        info = f.read()
    # print(info)
    h = HtmlToDict(BaseExtract)
    h.debug = False
    if h.load_html(page_source=info):
        print({
                "id": h.id,  # 字符串
                "full_name": h.full_name,  # 字符串
                "short_name": h.short_name,  # 字符串
                "industry": h.industry,  # 字符串
                "found_time": h.found_time,  # 字符串2019-01-01
                "type": h.type,  #todo  字符串or map
                "introduce": h.introduce,
                "tag": h.tag,  # 标签
                "url": h.url,  # 公司主页
                "origin_url": h.origin_url,  # 原始网页
                "head_address": h.head_address,
                "office_cities": h.office_cities,
                "source": h.source,  # 来源
                "develops": h.develops,
                "logo": h.logo,
                "productions": h.productions,
                "cxos": h.cxos
            })
    return


if __name__ == '__main__':
    main()




