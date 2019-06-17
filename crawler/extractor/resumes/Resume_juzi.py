#! /usr/bin/env python3
# coding=utf-8

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
import logging

class HtmlToDict(BaseExtract, Base):

    # def __init__(self):
    #     super(BaseExtract, self).__init__()
    #     self.registered_capital = ""
    #     self.registered_owner = ""
    #     self.registered_phone = ""

    def set_unix_time(self, str_time):
        # "2009-11"
        design =  re.findall("-", str_time)
        if len(design) == 1:
            return int(time.mktime(time.strptime(str_time, "%Y-%m")))
        elif len(design) == 2:
            return int(time.mktime(time.strptime(str_time, "%Y-%m-%d")))
        else:
            return 0

    def load_html(self, page_source=None):
        """json格式的详情页"""
        if not page_source:
            return False
        else:
            try:
                self.tree = json.loads(page_source)
                return True
            except Exception as e:
                logging.error(e)
                return False


    def reset_style(self, res):
        """去掉html标签 保证换行符"""
        # json格式的换成str
        resumes = re.sub(r'<br\s*/>','\n', res)
        resumes = re.sub(r'<.*?>',"", resumes)
        return resumes

    # 2/14
    def resume_info(self):
        """独立的解析函数"""
        tree = self.tree  # json格式
        print(type(tree))
        basic_info = tree.get("basic", {})
        contact_info = tree.get("contact", {})
        person_info = tree.get("person", {})
        commerce_info = tree.get("commerce", {})
        # print(f"commerce_info is {commerce_info}")

        # 基本信息
        if len(str(basic_info)) > 10:
            basic_dic = basic_info.get("data").get("basic", {})
            if len(str(basic_dic)):
                found_time = basic_dic.get("com_born_date", "")  # "2009-11"
                self.found_time = self.set_unix_time(found_time) if found_time else 0
                self.head_address = basic_dic.get("com_local", "")
                office_cities = None  # 暂时没看到分布信息
                self.office_cities = office_cities if office_cities else []
                self.short_name = basic_dic.get("com_name", "")
                self.full_name = basic_dic.get("com_registered_name", "")
                self.logo = basic_dic.get("com_logo_archive", "")
                self.url = basic_dic.get("com_url", "")
                self.industry = basic_dic.get("com_scope").get("cat_name", "") if basic_dic.get("com_scope") else ""
                company_id = basic_dic.get("com_id", "")
                introduce = basic_dic.get("com_des", "")
                self.introduce = self.reset_style(introduce) if introduce else ""
                if company_id:
                    original_url = f"https://www.itjuzi.com/company/{company_id}"
                else:
                    original_url = ""
                self.origin_url = original_url if original_url else ""   # https://www.itjuzi.com/company/1
                tag_info = basic_dic.get("tag_info", {})
                if len(tag_info):
                    tag_list = tag_info.get("normal_tag", []) + tag_info.get("especial_tag", [])
                    tag = [i.get("name", "") for i in tag_list]
                else:
                    tag = []
                self.tag = tag if tag else []

                self.develops = []
                develop = {}
                scale = basic_dic.get("company_scale", {})
                if scale:
                    scale = scale.get("com_scale_name", "")
                else:
                    scale = ""
                develop["scale"] = self.company_scale_map(scale) if scale else ""  # 映射
                develop["invest"] = basic_dic.get("com_fund_needs_name", "")
                develop["state"] = 1  # 0 表示倒闭
                develop["create_time"] = self.found_time
                develop["update_time"] = int(time.time())
                self.develops.append(develop)
                self.id = self.create_hash_id(self.full_name, self.origin_url, str(self.source))

        # 产品信息 person_info
        if len(str(person_info)) > 10:

            person_data = person_info.get("data", {})
            if person_data:
                # cxo
                person_list = person_data.get("person", [])
                for ele in person_list:
                    cxos = {}  # 置空
                    cxos["cxo_name"] = ele.get("name", "")
                    cxos["cxo_position"] = ele.get("des", "")
                    cxos["cxo_pic_url"] = ele.get("logo", "")
                    cxos["cxo_desc"] = self.reset_style(ele.get("per_des", ""))  # boss暂无标签
                    cxos["cxo_tag"] = []  # 暂无tag
                    cxos["create_time"] = 0  # 暂无创建时间
                    cxos["update_time"] = int(time.time())  # 更新时间
                    self.cxos.append(cxos)
                # 产品
                products_list = person_data.get("products", [])
                for pro in products_list:
                    production = {}  # 置空
                    production["desc"] = re.sub(r"<.*?>", "", str(pro.get("des", ""))).replace("\n", "").strip()
                    production["desc"] = self.reset_style(production["desc"])
                    production["name"] = pro.get("name", "")
                    production["pic"] = pro.get("logo", "")
                    production["tags"] = []  # boss暂无标签
                    production["url"] = pro.get("url", "")  # 产品官网
                    production["create_time"] = 0  # 暂无创建时间
                    production["update_time"] = int(time.time())  # 更新时间
                    self.productions.append(production)

        # 工商信息 commerce_info
        if len(str(commerce_info)) > 10:
            elecredit_basic = commerce_info.get("elecredit_basic", {})
            if len(str(elecredit_basic)):
                self.full_name = elecredit_basic.get("entname")
                self.type = elecredit_basic.get("enttype", "")
                registered_capital = elecredit_basic.get("regcap", "")   # "163.2026 万人民币"  todo
                self.registered_capital = registered_capital + "万人民币" if registered_capital else ""
                self.registered_owner = elecredit_basic.get("frname", "")  # "何斌",  todo
                self.registered_phone = ""  # not found
                esdate = elecredit_basic.get("esdate", "")
                self.found_time = self.set_unix_time(esdate) if esdate else self.found_time

            elecredit_shareholder = commerce_info.get("elecredit_shareholder", [])
            self.shareholders = []  # 董事长
            for ele in elecredit_shareholder:  # todo
                shareholders = {}  # 置空
                shareholders["name"] = ele.get("shaname", "")
                shareholders["money"] = str(ele.get("subconam", "")) + "万" if ele.get("subconam", "") else ""
                shareholders["prencent"] = str(ele.get("fundedratio", "")) + "%" if ele.get("fundedratio", "") else 0
                shareholders["type"] = ele.get("conform", "")  # boss暂无标签
                shareholders["create_time"] = 0  # 暂无创建时间
                shareholders["update_time"] = int(time.time())  # 更新时间
                self.shareholders.append(shareholders)
        else:
            self.registered_capital = ""
            self.registered_owner = ""
            self.registered_phone = ""
            self.shareholders = []  # 董事长
        self.resume = {
                "id": self.id,  # 字符串
                "full_name": self.full_name,  # 字符串
                "short_name": self.short_name,  # 字符串
                "industry": self.industry,  # 字符串
                "found_time": self.found_time,  # 字符串2019-01-01
                "type": self.type,  #todo  字符串or map
                "introduce": self.reset_style(self.introduce),
                "tag": self.tag,  # 标签
                "url": self.url,  # 公司主页
                "registered_capital": self.registered_capital, # "163.2026 万人民币"
                "registered_owner": self.registered_owner, # "何斌"
                "registered_phone": self.registered_phone, # "15435759862"
                "origin_url": self.origin_url,  # 原始网页
                "head_address": self.head_address,
                "office_cities": self.office_cities,
                "source": self.source,  # 来源
                "develops": self.develops,
                "logo": self.logo,
                "productions": self.productions,
                "cxos": self.cxos,
                "shareholders": self.shareholders
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


def main(file_name):
    with open(file_name, mode='r+',encoding="utf-8") as f:
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
    for i in range(1,79):
        main(f"{i}.text")
        time.sleep(0)
        print("*"*100)



