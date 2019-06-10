import time
from lxml import etree
import hashlib
import re
import json


class BaseExtract(object):
    """
    {
    "id": "2478347934938493",  # 字符串
    "full_name": "武汉智寻天下科技有限公司",  # 字符串
    "short_name": "简寻",  # 字符串
    "industry": "IT/互联网",  # 字符串
    "found_time": 1557819205,  # 字符串2019-01-01
    "type": "私企",  #todo  字符串or map
    "introduce": "企业简介",
    "tag": ["五险一金"],  # 标签
    "url": "https://www.jianxun.io",  # 公司主页
    "origin_url": "https://jobs.51job.com/all/co3779673.html",  # 原始网页
    "head_address": "总部地址",
    "office_cities": ["北京", "武汉"],
    "logo":"",
    "develops":[
        {
            "scale": "0-50",  # todo 是否修改为 map
            "invest": "A轮",
            "state": 0,  # bool 1公司是否关闭
            "create_time": 1557819205,  # 时间
            "update_time": 1557819205,  # 更新时间戳
        }
    ]
    "production":[{
        "desc":"",
        "name":"",
        "pic":"",
        "tags":"",
        "url":"",
        "create_time":"",
        "update_time":""
    }],
    "cxos":[{
        "cxo_name":"",
        "cxo_position":"",
        "cxo_pic_url":"",
        "cxo_desc":"",
        "cxo_tag":"",
        "create_time":"",
        "update_time":""
    }]
    }
    """

    def __init__(self, doc=None):
        """初始化参数"""

        if doc:
            # doc 内容{}
            # print(doc)
            self.update_time_unix = 0
            self.doc = doc
            self.tree = None
            self.debug = False
        self.source = 202 # todo site映射
        self.id = ""
        self.full_name = ""
        self.short_name = ""
        self.industry = ""
        self.found_time = int(time.time())
        self.type = 0
        self.introduce = ""
        self.tag = []
        self.url = ""
        self.origin_url = ""
        self.head_address = ""
        self.office_cities = []
        self.logo = ""
        self.productions = []  # 公司产品介绍
        self.develops = []
        self.cxos = []  # 高管信息

    def load_html(self, page_source=None):
        """加载文档
        {
        "site":"job51",  # todo site_source map
        "content":"<html>...</html>",
        "spider_info":"{}"
        }
        """
        if page_source is None:
            page_source = self.doc  # 传入的文件为HTML
        if page_source is None:
            return False
        if self.debug:
            print("page_source is :{}".format(page_source))
        try:
            self.tree = etree.HTML(page_source)
        except Exception as e:
            print(e)
            return False
        return True

    def create_hash_id(self, name, url='', source='100'):
        """生成id"""
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

    def company_scale_map(self, scale_str):
        """
        0：未知
         1：1-15人
         2：15-50人
         3：50-150人，
         4：150-500人，
         5：500-2000人，
         6：2000人以上，
        :param scale_str:
        :return:
        """
        scale_str = scale_str.replace(" ", "")
        if "以上" in scale_str:
            scale_from = re.findall(r'\d+', scale_str)[0] if re.findall(r'\d+', scale_str) else 0
            scale_to = scale_from
        else:
            scale_from, scale_to = re.findall(r'(\d+)-(\d+)', scale_str)[0] if re.findall(r'(\d+)-(\d+)', scale_str) else (0,0)
        scale_to = int(scale_to)
        if scale_to==0:
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
        elif scale_to > 2000:
            return 6
        else:
            return 0

    def set_jx_resume_id(self, resume):
        if isinstance(resume, dict):
            if resume['source'] > 200:
                pop_list = ["id", "develops", "office_cities", "tag", "cxos", "productions", "introduce", "logo"]
            elif 90 < resume['source'] < 200:
                pop_list = ['id', 'introduce', 'create_time', 'update_time', 'tag']
            else:
                raise Exception('source: %r is invailed.' % resume['source'])
            for key in pop_list:
                if key in resume:
                    resume.pop(key)
            hashed_key = hashlib.md5(
                json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[
                         8:-8]
            hashed_id = int(hashed_key, 16)
            return hashed_id
        else:
            return 0




if __name__ == '__main__':
    pass