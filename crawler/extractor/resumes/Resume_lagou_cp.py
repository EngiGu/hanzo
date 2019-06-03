#! /usr/bin/env python3
# coding=utf-8

from .resume_base import BaseExtract
import time
import re
from core.base import Base
from config import SITE_SOURCE_MAP
import json
from copy import deepcopy

class HtmlToDict(BaseExtract, Base):

    def set_unix_time(self, str_time):
        # 2013-08-15 16:20:48
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S")))

    # 2/14
    def resume_info(self):
        """独立的解析函数"""
        print("start resume info")
        tree = self.tree
        company_busness_info = tree.xpath('//*[@id="companyInfoData"]/text()')
        if not company_busness_info:
            return
        else:
            company_busness_info = company_busness_info[0]  # 格式为json
            try:
                res = json.loads(company_busness_info)
            except:
                return
            # 公司注册信息
            addressList = res.get("addressList",[])
            if len(addressList) > 0:
                addresslist = addressList[0]
                found_time = addresslist.get("createTime", "")  # 2013-08-15 16:20:48
                self.found_time = self.set_unix_time(found_time) if found_time else 0
                head_address = addresslist.get("detailAddress", "")
                self.head_address = head_address if head_address else ""
                office_cities = None  # 暂时没看到分布信息
                self.office_cities = office_cities if office_cities else []

            # 公司核心信息
            coreInfo = res.get("coreInfo", {})
            if len(coreInfo) > 0:
                short_name = coreInfo.get("companyShortName", "")
                self.short_name = short_name if short_name else ""
                full_name = coreInfo.get("companyName", "")
                self.full_name = full_name if full_name else ""
                if not self.full_name:
                    self.full_name = self.short_name
                logo = coreInfo.get("logo", "")
                self.logo = f"https://www.lagou.com/{logo}" if logo else ""
                self.url = coreInfo.get("companyUrl", "")
            type = None  # 没有写公司类型
            self.type = type[0] if type else ""

            # 公司基本信息
            company_id = ""
            baseInfo = res.get("baseInfo", {})
            if len(baseInfo) > 0:
                industry = baseInfo.get("industryField", "")
                self.industry = industry if industry else ""
                company_id = baseInfo.get("companyId", "")
        tag = res.get("labels", [])
        self.tag = tag if tag else ""
        introduce = res["introduction"].get("companyProfile", "")
        self.introduce = introduce.replace("\n", "").strip() if introduce else ""
        if company_id:
            original_url = f"https://www.lagou.com/gongsi/{company_id}.html"
        else:
            original_url = ""
        self.origin_url = original_url if original_url else "" # https://www.zhipin.com/gongsi/6f1aa1d6b1d033ad33B43N0~.html
        self.develops = []
        develop = {}
        scale = res["baseInfo"].get("companySize", "")
        develop["scale"] = self.company_scale_map(scale) if scale else ""  #  映射
        develop["invest"] = res["baseInfo"].get("financeStage", "")
        develop["state"] = 1  # 0 表示倒闭
        develop["create_time"] = self.found_time
        develop["update_time"] = int(time.time())
        self.develops.append(develop)
        self.id = self.create_hash_id(self.full_name, self.origin_url, str(self.source))

        # self.productions = []
        production_list = res.get("products", [])
        if len(production_list) > 0:
            for pro in production_list:
                production = {}  # 置空
                production["desc"] = re.sub(r"<.*?>","", pro.get("productprofile", "")).replace("\n", "").strip()
                production["name"] = pro.get("product", "")
                production["pic"] = ("https://www.lagou.com/" + pro.get("productpicurl", "")) if pro.get("productpicurl", "") else ""
                production["tags"] = pro.get("producttype", [])  # boss暂无标签
                production["url"] = pro.get("producturl", "") # 产品官网
                production["create_time"] = 0  # 暂无创建时间
                production["update_time"] = int(time.time())  # 更新时间
                self.productions.append(production)

        cxos_ele = res.get("leaders")
        if len(cxos_ele) > 0:
            for ele in cxos_ele:
                cxos = {}  # 置空
                cxos["cxo_name"] = ele.get("name", "")
                cxos["cxo_position"] = ele.get("position", "")
                cxos["cxo_pic_url"] = ("https://www.lagou.com/" + ele.get("photo", "")) if ele.get("photo", "") else ""
                cxos["cxo_desc"] = ele.get("remark", "").replace("\n", "").replace("\r", "").strip()  # boss暂无标签
                cxos["cxo_tag"] = []  # 暂无tag
                cxos["create_time"] = 0  # 暂无创建时间
                cxos["update_time"] = int(time.time())  # 更新时间
                self.cxos.append(cxos)
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
        jx_resume_id = self.set_jx_resume_id(deepcopy(self.resume))  # 获取jx_resume_id
        self.resume["jx_resume_id"] = jx_resume_id
        return

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




