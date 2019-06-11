#! /usr/bin/env python3
# coding=utf-8
import hashlib

try:
    from .resume_base import BaseExtract
except:
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
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d")))

    # 2/14
    def format_scale(self, scale_str):
        '''
         0：未知
         1：1-15人
         2：15-50人
         3：50-150人,
         4：150-500人,
         5：500-2000人,
         6：2000人以上,
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
        move = dict.fromkeys((ord(c) for c in "\xa0"))
        return _str.translate(move).strip()

    # def shareholders_is_null(self, _str):
    #     return f

    # 2/14
    def resume_info(self):
        tree = self.tree

        url = first(tree.xpath('//a[@class="mech_170822_nav_d02_a02"]/@href'))

        base_info = tree.xpath('//div[@class="de_170822_d01_d"]//td/span/text()')
        print(base_info)
        found_time = self.set_unix_time(base_info[9])
        full_name = base_info[1]
        registered_phone = base_info[11]

        short_name = tree.xpath('//h3[@class="mech_170525_nav_h3"]/text()')
        short_name = self.remove_xa0(first(short_name))
        # print(short_name)

        invest = tree.xpath('//h3[@class="mech_170525_nav_h3"]/span/text()')
        invest = self.remove_xa0(first(invest)).replace('(', '').replace(')', '')
        # print(invest)

        labels = tree.xpath('//div[@id="tagsImg"]/span/a/text()')
        head_address = base_info[5]
        # print(head_address)

        introduce = tree.xpath('//div[@class="de_170822_d01_d02"]/p/text()')
        introduce = self.remove_xa0(first(introduce)).replace('\u2028', '')
        # print(introduce)

        registered_capital = base_info[3]
        registered_owner = base_info[7]

        origin_url = re.findall(r"ncid:'(\w+)'", ''.join(self.page_souce.split()))
        origin_url = 'https://www.innotree.cn/inno/company/%s.html' % origin_url[0]
        # print(origin_url)

        logo = tree.xpath('//img[@class="mech_170525_nav_img"]/@src')
        logo = first(logo)
        # print(logo)

        now_stmp = int(time.time())

        'https://www.innotree.cn/inno/company/ajax/projectlist?compId=932789097471238742'
        product = self.page_souce.split('+d8053f3eb827b6bc22006b7200ba2f5e+')[1]
        products = [{"desc": i['introduction'],
                     "name": i['sName'],
                     "pic": i['logo'],
                     "tags": [],
                     "url": "",
                     "create_time": 0,
                     "update_time": now_stmp}
                    for i in json.loads(product)['data']]
        # print(products)

        develop = tree.xpath('//div[@class="de_170822_d01_d03"]//tr')
        develops = []
        for i in develop:
            one = {"create_time": 0,
                   "invest": '',
                   "invest_money": "千万人民币",
                   "invest_organ": ['aa投资', 'bb投资'],
                   "scale": 0,
                   "state": 1,
                   "update_time": now_stmp}
            one['create_time'] = i.xpath('./td[1]/span/text()')
            one['create_time'] = self.set_unix_time(first(one['create_time']))
            one['invest'] = i.xpath('./td[2]/span/span/text()')
            one['invest'] = first(one['invest'])
            one['invest_money'] = i.xpath('./td[3]/span/text()')
            one['invest_money'] = first(one['invest_money'])
            one['invest_organ'] = i.xpath('./td[4]/a/text()')
            tmp = i.xpath('./td[4]/a/span/text()')
            one['invest_organ'] = one['invest_organ'] + tmp
            # print(one['invest_organ'])
            develops.append(one)

        develops.reverse()

        cxos = [
            {
                "cxo_name": self.remove_xa0(i.xpath('string(./td[2])')),
                "cxo_position": self.remove_xa0(i.xpath('string(./td[3])')),  # 高管职位
                "cxo_pic_url": '',  # 图片存储地址
                "cxo_desc": self.remove_xa0(i.xpath('string(./td[4])')),  # 描述信息
                "cxo_tag": '',  # 标签信息
                "create_time": 0,
                "update_time": now_stmp
            }
            for i in tree.xpath('//div[@id="foundersInfo_info"]//tr')
        ]

        shareholders = [
            {
                "name": self.remove_xa0(i.xpath('string(./td[1])')),
                "money": self.remove_xa0(i.xpath('string(./td[2])')),
                "prencent": self.remove_xa0(i.xpath('string(./td[3])')),
                "type": "",
                "create_time": 0,
                "update_time": now_stmp
            }
            for i in tree.xpath('//div[@class="de_170822_d01_d04_d01"]//tr')
        ]
        # print('shareholders', shareholders)
        id = self.create_hash_id(str(full_name), url=origin_url, source=str(self.source))

        self.resume = {
            "id": id,  # 使用full_name +origin_url 联合hash成一个id
            "found_time": found_time,
            "full_name": full_name,
            "short_name": short_name,
            "tag": [],
            "labels": labels,
            "type": "",
            "url": url,
            "head_address": head_address,
            "industry": "",
            "introduce": introduce,
            "registered_capital": registered_capital,
            "registered_owner": registered_owner,
            "registered_phone": registered_phone,
            "office_cities": [],
            "origin_url": origin_url,
            "logo": logo,
            "source": 101,
            "productions": products,
            "develops": develops,
            "cxos": cxos,
            "shareholders": shareholders
        }

    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        site = html_doc.get("site")
        self.source = SITE_SOURCE_MAP.get(site)
        if not self.source:
            raise Exception('config.py has not source on site: {}'.format(site))
        self.content = html_doc.get("content", "")
        if self.load_html(page_source=self.content):
            self.resume_info()  # 调核心解析函数
            return self.resume
        else:
            return None


def main():
    with open('./tmp/yinguo_1.html', mode='r+', encoding="utf-8") as f:
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
