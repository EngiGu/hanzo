#! /usr/bin/env python3
# coding=utf-8
import hashlib

from resume_base import BaseExtract
import time
import re
from core.base import Base
from config import SITE_SOURCE_MAP
import json
from copy import deepcopy


def first(tree_res):
    return tree_res[0] if tree_res else ""


class HtmlToDict(BaseExtract, Base):

    def set_unix_time(self, str_time):
        # 2013-08-15 16:20:48
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S")))

    # 2/14
    def format_scale(self, scale_str):
        '''
         0：未知
         1：1-15人
         2：15-50人
         3：50-150人，
         4：150-500人，
         5：500-2000人，
         6：2000人以上，
        :param tmp:
        :return:
        '''

        scale_from = 0
        scale_to = 0
        if "以上" in scale_str:
            scale_from = re.findall(r'\d+', scale_str)[0] if re.findall(r'\d+', scale_str) else 0
            scale_to = scale_from
        else:
            scale_from, scale_to = re.findall(r'(\d+)-(\d+)', scale_str)[0] if re.findall(r'(\d+)-(\d+)',
                                                                                          scale_str) else (0, 0)
        scale_to = int(scale_to)
        if scale_to == 0:
            return 0
        elif scale_to <= 15:
            return 1
        elif scale_to <= 50:
            return 2
        elif scale_to <= 150:
            return 3
        elif scale_to <= 500:
            return 4
        elif scale_to <= 2000:
            return 5
        else:
            return 6

    def create_hash_id(self, name, url='', source='100'):
        # todo
        hashed_key = hashlib.md5(name.encode(encoding='utf_8', errors='strict')).hexdigest()
        hashed_key = hashed_key[8:-11]
        hashed_id = str(int(hashed_key, 16))
        for i in range(len(str(hashed_id)), 16):
            hashed_id = '0' + hashed_id
        hashed_key_url = hashlib.md5(url.encode(encoding='utf_8', errors='strict')).hexdigest()[8:-14]
        hashed_id_url = str(int(hashed_key_url, 16))
        for i in range(len(str(hashed_id_url)), 13):
            hashed_id_url = '0' + hashed_id_url
        return source + hashed_id + hashed_id_url

    def remove_xa0(self, _str):
        move = dict.fromkeys((ord(c) for c in "\xa0\n\t"))
        return _str.translate(move).strip()

    # 2/14
    def resume_info(self):
        tree = self.tree
        # self.source = 208
        # self.id = tree.xpath('//div[@class="overview__title"]/h1/text()')[0]

        # company_busness_info = tree.xpath('//div[@class="job-sec company-business"]')
        # company_location_info = tree.xpath('//div[@class="tHeader tHCop"]')[0]
        # if company_busness_info:
        #     company_busness_info = company_busness_info[0]
        full_name = tree.xpath('//span[@class="l-title-content"]/text()')
        self.full_name = first(full_name)
        logo = tree.xpath('//div[@class="cor-logo-img"]/img/@src')
        self.logo = first(logo) if first(logo) else ''
        self.found_time = 0
        # type_and_scale = tree.xpath('//div[@class="cor-details"]/span/text()')
        # print(type_and_scale)
        # print(len(type_and_scale))
        # if len(type_and_scale) == 0:
        #     self.type = ''
        #     scale = ''
        #     industry = ''
        # else:
        #     self.type = type_and_scale[2]
        #     scale = type_and_scale[0].replace(' ', '')
        #     industry = type_and_scale[1]
        #
        self.type = tree.xpath('//div[@class="cor-details"]/span[@class="d-come"]/text()')
        self.type = first(self.type)
        scale = tree.xpath('//div[@class="cor-details"]/span[@class="d-person"]/text()')
        scale =  first(scale)
        industry = tree.xpath('//div[@class="cor-details"]/span[@class="d-type"]/text()')
        industry = first(industry)
        tag = []

        head_address = tree.xpath('//tbody/tr/th[starts-with(text(), "地区")]/../following-sibling::tr[1]/td/text()')
        head_address = first(head_address) if first(head_address) else ''
        self.head_address = ''.join(head_address.split()).replace('t', '')
        # self.head_address = self.remove_xa0(head_address).replace('t', '').replace(' ',)
        self.office_cities = []

        # # short_name = tree.xpath('//div[@class="smallbanner "]//h1[@class="name"]/text()')
        short_name = tree.xpath('//tbody/tr/th[starts-with(text(), "别名")]/../following-sibling::tr[1]/td/text()')
        self.short_name = first(short_name) if first(short_name) else ''
        self.short_name = ''.join(self.short_name.split())
        introduce = tree.xpath('//div[@class="cor-introduce"]/p/text()')
        # self.introduce = introduce[0].xpath('string()').strip() if introduce else ''
        introduce = [self.remove_xa0(i) for i in introduce if self.remove_xa0(i) != '']
        # print(introduce)
        self.introduce = '\n'.join(introduce)
        self.industry = industry.strip()
        #
        self.url = tree.xpath('//div[@class="url-box"]/a/text()')  # 公司主页
        self.url = first(self.url)

        self.origin_url = tree.xpath('//div[@class="more-link"]/a/@href')
        self.origin_url = 'https://www.dajie.com' + first(self.origin_url)

        self.develops = []
        develop = {}
        develop["scale"] = self.format_scale(scale)
        develop["invest"] = ""  # boss暂无融资信息
        develop["state"] = 1  # 0 表示倒闭
        develop["create_time"] = self.found_time
        develop["update_time"] = time.time()
        self.develops.append(develop)
        self.id = self.create_hash_id(str(self.full_name), url=self.origin_url, source=str(self.source))

        self.resume =  {
            "id": self.id,  # 字符串
            "full_name": self.full_name,  # 字符串
            "short_name": self.short_name,  # 字符串
            "industry": self.industry,  # 字符串
            "found_time": self.found_time,  # 字符串2019-01-01
            "type": self.type,  # todo  字符串or map
            "introduce": self.introduce,
            "tag": self.tag,  # 标签
            "url": self.url,  # 公司主页
            "origin_url": self.origin_url,  # 原始网页
            "head_address": self.head_address,
            "office_cities": self.office_cities,
            "source": self.source,  # 来源
            "develops": self.develops,
            "logo": self.logo
        }


    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        site = html_doc.get("site")
        self.source = SITE_SOURCE_MAP.get(site)
        self.content = html_doc.get("content", "")
        if self.load_html(page_source=self.content):
            self.resume_info()  # 调核心解析函数
            return self.resume
        else:
            return None


def main():
    with open('dajie_1.html', mode='r+',encoding="utf-8") as f:
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




