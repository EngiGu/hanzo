#! /usr/bin/env python3
# coding=utf-8
import hashlib
from datetime import datetime

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

    def salary_to_int(self, salary_str):
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

    @staticmethod
    def convert_update_time(t_str='2017-08-19'):
        return int(time.mktime(datetime.strptime(t_str, '%Y-%m-%d').timetuple()))

    def trans_pub_time(self, update_time):
        # print(update_time)
        try:
            # update_time = t.xpath('//*[@id="updateDate"]/@value')[0]  # 更新时间：1小时前     分钟  小时  昨天  今天  几天前 2019-05-05
            # print(update_time)
            if "分钟" in update_time:
                hour_before = re.match(r'(\d)+分钟', update_time).group(1) if re.match(r'(\d)+分钟', update_time) else 0
                update_time_raw_str = time.time() - 60 * int(hour_before)
            elif "小时" in update_time:
                hour_before = re.match(r'(\d)+小时', update_time).group(1) if re.match(r'(\d)+小时', update_time) else 0
                update_time_raw_str = time.time() - 3600 * int(hour_before)
            elif "天" in update_time:
                if "昨天" in update_time:
                    hour_before = 1
                elif "今天" in update_time:
                    hour_before = 0
                else:
                    hour_before = re.match(r'(\d)+天', update_time).group(1) if re.match(r'(\d)+天', update_time) else 0
                update_time_raw_str = time.time() - 24 * 3600 * int(hour_before)
            elif "-" in update_time:
                update_time_raw_str = self.convert_update_time(update_time)
            else:
                update_time_raw_str = time.time()
        except:
            update_time_raw_str = time.time()
        return update_time_raw_str

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

    def time_stamp_format(self, time_stamp, format):
        # 1562831661.5719736
        return time.strftime(format, time.localtime(time_stamp))

    def __return_format_time(self, t):
        return {
            'stamp': t,
            'YmdHMS': self.time_stamp_format(t, "%Y-%m-%d %H:%M:%S"),
            'Ymd': self.time_stamp_format(t, "%Y-%m-%d")
        }

    # 2/14
    def resume_info(self):
        tree = self.tree
        results = tree.xpath('//ul[@id="list_con"]/li')
        resumes = []
        print(len(results))
        for result in results:
            conn = result.xpath('string(.)')
            conn =  ''.join(conn.split())
            # print(conn)
            if conn == '':
                # 广告位置，跳过
                continue
            company = result.xpath('.//div[@class="comp_name"]/a/@title')[0].strip() if result.xpath(
                './/div[@class="comp_name"]/a/@title') else ''
            url = result.xpath('.//div[@class="job_name clearfix"]/a/@href')[0].strip() if result.xpath(
                './/div[@class="job_name clearfix"]/a/@href') else ''

            position_title = result.xpath('.//span[@class="name"]/text()')[0].strip() if result.xpath(
                './/span[@class="name"]/text()') else ''

            # print(company, url, position_title)
            # 职位类型 学历 年限提取
            _tmp = result.xpath('.//p[@class="job_require"]/span/text()')
            print(_tmp)
            position = _tmp[0]
            degree = self.degree_str_to_digit(_tmp[1])
            work_from, work_to = self.workyear_to_int(_tmp[2])

            # 薪资
            salary_str = result.xpath('.//p[@class="job_salary"]/text()')
            salary_from, salary_to = self.salary_to_int(salary_str[0])

            # 福利tag
            tag = result.xpath('.//div[@class="job_wel clearfix"]/span/text()')
            if '广告' in tag:
                tag.remove('广告')  # 去除里面的广告信息

            put_type = result.xpath('.//a[@class="item_con apply"]/following-sibling::a[1]/text()')
            # put_type = result.xpath('.//a[@class="sign"]/text()')
            if not put_type:
                put_type = result.xpath('.//a[@class="item_con apply"]/following-sibling::span[1]/text()')
            put_type = put_type[0].replace(' ', '') if put_type else ''
            put_type = put_type if put_type in ['置顶', '精准', '优选'] else ''
            # print(put_type)

            # 发布时间
            pub_str = result.xpath('.//span[@class="sign"]/text()')
            if put_type in ['置顶', '精准', '优选']:
                pub_str = ['今天']  # 这个标签出现的话会把时间覆盖
            # print('pub_str', pub_str)
            pub_time = self.trans_pub_time(pub_str[0])
            # print('pub_time', self.time_stamp_format(pub_time))

            now = time.time()
            resume = {
                'company': company,
                'url': url,
                'salary': {'from': salary_from, 'to': salary_to},
                'tag': tag,  # 职位福利tags
                'degree': degree,
                'work_experience': {'from': work_from, 'to': work_to},  # 工作年限
                'position': position,  # 职位类型
                'position_title': position_title,  # 职位标题
                'put_type': put_type,  # 职位投放类型 精准 置顶还是什么
                'pub_time': self.__return_format_time(pub_time),
                # 发布时间
                'crawl_time': self.__return_format_time(now),  # 抓取时间
                'source': self.source
            }
            resumes.append(resume)

            # print(resume)
            # break
        # print(len(resumes))
        # result = {
        #     "resume_list": resumes,
        #     "current_page": int(current_page),
        #     "last_page": int(last_page),
        # }

        # raise SystemExit(666)
        self.resume = resumes
        print(len(resumes))

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
    with open('./tmp/job58_3.html', mode='r+', encoding="utf-8") as f:
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
