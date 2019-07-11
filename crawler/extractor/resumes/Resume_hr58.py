#! /usr/bin/env python3
# coding=utf-8
from datetime import datetime
import hashlib

from lxml import etree
import pprint

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
        return int(time.mktime(time.strptime(str_time, "%Y-%m-%d %H:%M:%S")))

    def load_html(self, page_source=None):
        # if page_source is None:
        #     page_source = self.doc['html']  # 传入的文件为HTML
        if page_source is None:
            return False
        # "+++"
        # page_source1, page_source2 = page_source.split("+d135638806955c0ee9d255c64a952705+")  # [,]
        # 初始化参数
        # self.add_dic = page_source2
        # print(page_source2)
        # self.tree = etree.HTML(page_source1)
        # self.tree = etree.HTML(page_source)
        self.page_souce = page_source
        if 'jQuery' in page_source:
            self.page_souce = re.findall(r'jQuery\w+\((.*?)\)', page_source)[0]
        self.raw_json = json.loads(self.page_souce)
        # t = self.tree
        # # check
        # try:
        #     name = t.xpath('//*[@id="name"]/text()')[0] # 姓名资料，验证简历是否存在
        #     if self.debug:
        #         pass
        #     return True
        # except IndexError:
        #     return False
        # except AssertionError:
        #     return False
        return True

    def time_stamp_format(self, time_stamp, format):
        # 1562831661.5719736
        return time.strftime(format, time.localtime(time_stamp))

    def tans_sex(self, sex_str):
        if '男' in sex_str:
            return 1
        elif '女' in sex_str:
            return 2
        else:
            return 0

    def degree_str_to_digit(self, degree_str):
        # 学历的全集：初中|中技|高中|中专|大专|本科|硕士|MBA|EMBA|博士|其他
        if '大专' in degree_str:
            return 1
        elif '本科' in degree_str:
            return 2
        elif '硕士' in degree_str:
            return 3
        elif '博士' in degree_str:
            return 4
        elif '其他' in degree_str:
            return 0
        elif '初中' in degree_str:
            return 0
        elif '中技' in degree_str:
            return 0
        elif '高中' in degree_str:
            return 0
        elif '中专' in degree_str:
            return 0
        elif 'MBA' in degree_str:
            return 3
        elif 'EMBA' in degree_str:
            return 3
        elif degree_str is None:
            return 0
        else:
            if self.debug:
                print(('highest degree: _%s_' % degree_str))
            return 0

    def salary_to_int(self, salary_str):
        salary_str = salary_str.replace('元', '')
        if "-" in salary_str:
            salary_from = salary_str.split("-")[0]
            salary_to = salary_str.split("-")[1]
            salary_from, salary_to = int(salary_from), int(salary_to)
        else:
            salary_from = 0
            salary_to = 0
        return salary_from, salary_to

    def workyear_to_int(self, work_str):
        if "-" in work_str:
            work_year_from, work_year_to = re.findall(r"(\d+)-(\d+)", work_str)[0]
        else:
            work_year_from = 0
            work_year_to = re.findall(r"(\d+)年", work_str)[0] if re.findall(r"(\d+)年", work_str) else 0
        return int(work_year_from), int(work_year_to)

    def resume_info(self):
        resumes = []
        raw_json = self.raw_json
        resume_list = raw_json['data']['resumeList']
        # print(resume_list)

        for one in resume_list:
            age = int(one['ageText'])
            sex = self.tans_sex(one['sexText'])
            degree = self.degree_str_to_digit(one['education'])
            salary_from, salary_to = self.salary_to_int(one['targetSalary'])
            work_from, work_to = self.workyear_to_int(one['workYear'])

            # 时间处理
            pub_time = int(one['updateDateTimeStamp'][:-3])
            now = time.time()
            extra = {
                'age': age,
                'sex': sex,
                'degree': degree,
                'salary': {'from': salary_from, 'to': salary_to},
                'work_experience': {'from': work_from, 'to': work_to},  # 工作年限
                'pub_time': {
                    'stamp': pub_time, 'YmdHMS': self.time_stamp_format(pub_time, "%Y-%m-%d %H:%M:%S"),
                    'Ymd': self.time_stamp_format(pub_time, "%Y-%m-%d")
                },
                # 发布时间
                'crawl_time': {
                    'stamp': now, 'YmdHMS': self.time_stamp_format(now, "%Y-%m-%d %H:%M:%S"),
                    'Ymd': self.time_stamp_format(pub_time, "%Y-%m-%d")

                },  # 抓取时间
            }
            # print(extra['pub_time']['YmdHMS'])
            resume = dict(one, **extra)
            resumes.append(resume)
        return resumes

    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        site = html_doc.get("site")
        self.source = SITE_SOURCE_MAP.get(site)
        if not self.source:
            raise Exception('config.py has not source on site: {}'.format(site))
        self.content = html_doc.get("content", "")
        if self.load_html(page_source=self.content):
            return self.resume_info()
            # 原始字段 原始字段不做任何修改，只添加一些自定义的字段
            # "userID": "275897128",
            # "education": "中专/技校",
            # "infoID": "0",
            # "updateDate": "2019-07-11",
            # "mobile": "",
            # "searchVersion": "0",
            # "trueName": "盛运锋",
            # "nowPosition": "――",
            # "complete": "50",
            # "letter": "",
            # "school": "",
            # "resumeID": "3_neypnenpnEmQTetvnEdplEDk_E6sTEOQ_EzknpsunGyYnGnQMGOfn-5fTegknGrsnEralEyNTeyX",
            # "targetArea": "武汉江岸区",
            # "targetPosition": "服务员",
            # "resumeTp": "服务员、店员/营业员",
            # "experYears": "",
            # "experCount": "",
            # "experCos": "",
            # "age": "0",
            # "url": "//jianli.58.com/resumedetail/single/3_neypnenpnEmQTetvnEdplEDk_E6sTEOQ_EzknpsunGyYnGnQMGOfn-5fTegknGrsnEralEyNTeyX?sourcepath=pc-viplist-gengxin&followparam=%7B%22searchID%22%3A%22264e6eceaa49435ead7c9788e1d4b9df%22%2C%22searchVersion%22%3A0%2C%22searchAreaID%22%3A159%2C%22searchFirstAreaID%22%3A158%2C%22searchPositionID%22%3A0%2C%22searchSecondPositionID%22%3A0%2C%22page%22%3A1%2C%22location%22%3A4%2C%22resumeType%22%3A1%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-viplist-gengxin%22%2C%22operatePage%22%3A%22list%22%7D",
            # "expectCityIds": "159,1913,160",
            # "expectArea": "武汉江岸区",
            # "sex": "0",
            # "targetSalary": "2000-3000元",
            # "workYear": "应届生",
            # "picUrl": "https://pic1.58cdn.com.cn/mobile/big/n_v2894d2449a98144128e41a97b43b4a8cc.jpg",
            # "searchId": "264e6eceaa49435ead7c9788e1d4b9df",
            # "namelimit": "0",
            # "experiences": [
            #
            # ],
            # "expectCateIds": "2181,2500",
            # "updateDateTimeStamp": "1562836056000",
            # "followParam": "%7B%22searchID%22%3A%22264e6eceaa49435ead7c9788e1d4b9df%22%2C%22searchVersion%22%3A0%2C%22searchAreaID%22%3A159%2C%22searchFirstAreaID%22%3A158%2C%22searchPositionID%22%3A0%2C%22searchSecondPositionID%22%3A0%2C%22page%22%3A1%2C%22location%22%3A4%2C%22resumeType%22%3A1%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-viplist-gengxin%22%2C%22operatePage%22%3A%22list%22%7D",
            # "isDownload": null,
            # "lspot": [
            #
            # ],
            # "rencaikulink": null,
            # "isValidaMobile": true,
            # "picCount": "0",
            # "lightSpotCount": "0",
            # "isDelete": false,
            # "sexText": "男",
            # "ageText": "18",
            # "campusResume": "0",
            # "hasFindJob": "0",
            # "pushResume": "3",
            # "sources": null,
            # "downLoadUserId": "0",
            # "showDelButton": true,
            # "shortUpdateDate": null,
            # "isFree": null,
            # "targetAreaId": "159",
            # "source": null
            #
        else:
            return None


def main():
    with open('./tmp/hr58_1.html', mode='r+', encoding="utf-8") as f:
        info = f.read()
    # print(info)
    h = HtmlToDict()
    print(h)
    h.debug = False
    print(h.load_html(info))
    if h.load_html(info):
        pprint.pprint(h.resume_info())  # 调核心解析函数
        # print(h.resume)
    return


if __name__ == '__main__':
    main()
