#! /usr/bin/env python3
# coding=utf-8
from datetime import datetime
import hashlib

from lxml import etree

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
        page_source1, page_source2 = page_source.split("+d135638806955c0ee9d255c64a952705+")  # [,]
        # 初始化参数
        self.add_dic = page_source2
        print(page_source2)
        self.tree = etree.HTML(page_source1)
        t = self.tree
        # check
        try:
            name = t.xpath('//*[@id="name"]/text()')[0] # 姓名资料，验证简历是否存在
            if self.debug:
                pass
            return True
        except IndexError:
            return False
        except AssertionError:
            return False
    # 2/14
    def resume_source(self):
        t = self.tree

        try:
            resume_id = t.xpath('//div[@id="noInviteNum_noticeDiv"]/following::div[1]/input[@name="rid"]/@value')[0] # 简历ID不等于用户ID
        except IndexError:
            resume_id = str()
        if self.debug:
            print(('resume_id: %s' % resume_id))
        try:
            update_time = t.xpath('//*[@id="updateDate"]/@value')[0]  # 更新时间：1小时前     分钟  小时  昨天  今天  几天前 2019-05-05
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
        return {
            "source": 21,  # 来源，1=猎聘，2=51job，3=智联招聘, 4=400w,5=Boss直聘,...,8=大街,9=纷简历,10=招聘狗,11=人才啊, 21是job58简历
            "source_resume_id": resume_id,
            "source_resume_name": '',
            "last_update": round(update_time_raw_str)
        }

    def check_exist(self, element):
        if element:
            return element[0].replace('\xa0',' ').strip()
        else:
            return ''

    @staticmethod
    def convert_update_time(t_str='2017-08-19'):
        return int(time.mktime(datetime.strptime(t_str, '%Y-%m-%d').timetuple()))
    # 3/14
    def profile(self): # 待修改
        part1 = self.profile_part1()

        profile = {
            "name": "",
            "mobile_phone": "",
            "tele_phone": "",
            "email": "",
            "weixin": "",
            "gender": 0,
            "age": 0,  # 年龄，格式：int，0-150，0=未知
            "marital_status": 0, # ?
            "work_year": { # 应届生？1年？
                "from": -1,
                "to": -1,
            },
            "highest_degree": -1,
            "find_job_status": self.profile_part2(),
            "self_evaluation": self.profile_part3(), # 有的没有
        }
        profile.update(part1)

        return profile

    # 基本信息
    def profile_part1(self):
        t = self.tree

        try:
            box_element = t.xpath('//div[@class="base-info"]')[0]
        except IndexError:
            return {
            "name": '',
            "mobile_phone": '',  # 手机号码不可见
            "tele_phone": '',  # 固定电话不可见
            "email": '',  # 电子邮箱不可见
            "weixin": '',  # 微信号不可见
            "gender": 0,
            "age": 0,
            "marital_status": 0, # 无婚姻状况
            "work_year": {
                "from": -1,
                "to": -1
            },
            "highest_degree": -1
        }

        # 性别，年龄，工作经验（时长），学历，婚姻状况，现居住地，户口，政治面貌
        name = t.xpath('//*[@id="name"]/text()')[0]
        base_detail_box = t.xpath('//div[@class="base-detail"]')[0] if t.xpath('//div[@class="base-detail"]') else ""
        if not len(base_detail_box):
            age_str = 0
            gender = ""
            work_year_from = 0
            work_year_to = 0
            gender_degree = "其他"
        else:
            context_text = base_detail_box.xpath('string()').replace("\n", "").strip() # 所有信息的集合放一起
            gender_sex = base_detail_box.xpath('.//span[@class="sex stonefont"]/text()')[0]
            gender_age = base_detail_box.xpath('.//span[@class="age stonefont"]/text()')[0]
            gender_degree = base_detail_box.xpath('.//span[@class="edu stonefont"]/text()')[0]
            gender_workyear = base_detail_box.xpath('.//span[@class="stonefont"]/text()')[0]
            self.location_info = context_text.replace(gender_age, "").replace(gender_sex, "").replace(gender_degree, "").replace(gender_workyear, "").replace("\t","").strip()
            try:
                age_str = re.findall('(\d+)', gender_age)[0]
            except IndexError:
                age_str = int()
            if gender_sex == '男':
                gender = 1
            elif gender_sex == '女':
                gender = 2
            else:
                gender = 0
            # 女 30岁 中专/技校 5-10年工作经验 衡水人 现居北京昌平城南
            if "-" in gender_workyear:
                work_year_from, work_year_to = re.findall(r"(\d+)-(\d+)", gender_workyear)[0]
            else:
                work_year_from = 0
                work_year_to = re.findall(r"(\d+)年", gender_workyear)[0] if re.findall(r"(\d+)年", gender_workyear) else 0


        if self.debug:
            print(('work_year: %s-%s' % (work_year_from, work_year_to)))

        return {
            "name": name,
            "mobile_phone": '',  # 手机号码不可见
            "tele_phone": '',  # 固定电话不可见
            "email": '',  # 电子邮箱不可见
            "weixin": '',  # 微信号不可见
            "gender": gender,
            "age": int(age_str),
            "marital_status": 0, # 无婚姻状况
            "work_year": {
                "from": int(work_year_from),
                "to": int(work_year_to)
            },
            "highest_degree": self.degree_str_to_digit(degree_str=gender_degree)
        }

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

    # 求职状态
    def profile_part2(self):
        t = self.tree

        try:
            box_element = t.xpath('//div[@id="rd_containerDiv"]/div[3]/div[contains(text(),"求职状态")]/text()')[0].strip()
        except IndexError:
            return 0
        tmp = box_element  # box_element为一段文字

        # 有以下几种情况?
        if tmp in ['目前正在找工作', '我目前处于离职状态']:
            return 1
        if tmp == '我目前在职，正考虑换个新环境':
            return 2
        elif tmp in ['观望有好机会会考虑','我对现有工作还算满意，如有更好的工作机会，我也可以考虑']:
            return 3
        elif tmp == '应届毕业生':
            return 1
        else:
            return 0

    # 自我评价？？
    def profile_part3(self):
        t = self.tree
        try:
            # 注意字符串前后的空格和换行
            self_evaluation = t.xpath('//div[@id="rd_containerDiv"]/div[contains(text(),"自我介绍")]/following::div[1]/pre[@class="rd-content"]/text()')[0].strip()
        except IndexError:
            return ''
        return self_evaluation

    # 4/14
    def location(self):
        t = self.tree
        if not len(self.location_info):
            return {
            'province': '', # 省
            'city': '', # 市
            'district': '', # 区
            'native_place': '' # 户籍
        }
        # 衡水人现居北京昌平城南
        location_str = self.location_info
        print(location_str)
        city = ''
        province = re.findall(r'现居(\w{2})', location_str)[0] if re.findall(r'现居(\w{2})', location_str) else ''
        district = ''
        native_place = ''
        location_dict = {
            'province': province, # 省
            'city': city, # 市
            'district': district, # 区
            'native_place': native_place # 户籍
        }
        return location_dict

    # @staticmethod
    # def location_str_to_dict(location_str):
    #     pcd_json = codecs.open(filename='./lib/province_city_distrinct.json', mode='r', encoding='utf8')
    #     pcd = json.load(fp=pcd_json, encoding='utf8')
    #     location_dict = {
    #         'province': '',
    #         'city': '',
    #         'district': '',
    #     }
    #
    #     # Search province:
    #     for i in range(0, len(pcd)):
    #         province_dict = pcd[i]
    #         if province_dict['province_short_name'] in location_str:
    #             location_dict['province'] = province_dict['province_short_name']
    #             # print '`province`: ', location_dict['province']
    #         # In some cases, there is no province name, but city name.
    #         # Search city:
    #         for j in range(0, len(province_dict['city_list'])):
    #             city_dict = province_dict['city_list'][j]
    #             if city_dict['city_short_name'] in location_str:
    #                 location_dict['city'] = city_dict['city_short_name']
    #                 # print '`city`: ', location_dict['city']
    #
    #                 if 'district_list' in list(city_dict.keys()):
    #                     for k in range(0, len(city_dict['district_list'])):
    #                         district_dict = city_dict['district_list'][k]
    #                         if district_dict['district_short_name'] in location_str:
    #                             location_dict['district'] = district_dict['district_full_name']
    #                             # print '`district`: ', location_dict['district']
    #                             break
    #                 else:
    #                     location_dict['district'] = ''
    #                     break
    #     return location_dict

    # 5/14
    def education_experience(self):  # 5/14
        edu_list = list()
        t = self.tree
        try:
            edu_column = t.xpath('//div[@class="education experience"]/div[@class="edu-detail"]')
        except IndexError:
            return [{
                    "start": int(),
                    "end": int(),
                    "school": '',
                    "degree": int(),
                    "unified_entrance": -1,
                    "major": '',
                    "main_course": []
                }]
        end = 0
        school = ""
        major = ""
        for edu in edu_column:
            school = self.check_exist(edu.xpath('.//span[@class="college-name"]/text()'))
            start_end = self.check_exist(edu.xpath('.//span[@class="graduate-time"]/text()')) #2005年09月毕业
            start_end_str = re.findall(r'(\d+年\d+月)', start_end)[0]
            major = self.check_exist(edu.xpath('.//span[@class="professional"]/text()'))
            start, end = self.start_end_str_to_unix(start_end_str=start_end_str) if start_end_str else (int(), int())

        edu_list.append(
            {
                "start": 0,
                "end": end,
                "school": school,
                "degree": 0,
                "unified_entrance": -1,
                "major": major,
                "main_course": []
            }
        )

        return edu_list

    # 2015.03-至今
    # 待修改
    def start_end_str_to_unix(self, start_end_str):
        if "-" in start_end_str:
            tmp_list = re.split('\-', start_end_str)
            if self.debug:
                print(tmp_list)
            start = int(time.mktime(time.strptime(tmp_list[0], "%Y.%m")))
            if '今' in tmp_list[1]:
                end = 999
            else:
                end = int(time.mktime(time.strptime(tmp_list[1], "%Y.%m")))
        elif "年" in start_end_str:
            start = 0
            end =int(time.mktime(time.strptime(start_end_str, "%Y年%m月")))
        else:
            start, end = 0, 0
        return start, end # 返回的是一个元组

    # 6/14
    def award_experience(self):  # 6/14
        return []


    @staticmethod
    def duration_to_year(start_year, end_year):  # 3年2个月
        try:
            int(start_year)
        except:
            start_year = time.ctime().split(' ')[-1]

        if '至今' in end_year:
            end_year = str(time.ctime().split(' ')[-1])
        elif len(str(end_year)) > 1:
            end_year = str(end_year).split('年')[0]
        if len(start_year.split('年')) > 1:
            start_year = str(start_year).split('年')[0]
        try:
            year = int(end_year) - int(start_year)
        except ValueError:
            year = 0
        if year < 0:
            year = 0
        return year

    # 7/14
    def job_experience(self):

        job_list = list()
        t = self.tree
        work_elements = t.xpath('//div[@class="work experience"]/div[@class="experience-detail"]')
        if not len(work_elements):
            salary = {
                'type': 1,
                'monthly_salary': {
                    'from': int(),
                    'to': int(),
                    'num_per_year': 12
                },
                'annual_salary': {
                    'from': 0,
                    'to': 0
                }
            }
            job_list = [{
                "start": int(),
                "end": int(),
                "industry": list(),
                "company": '',
                "location": '',
                "work_year": int(),
                "department": '',
                "position": '',
                "responsibility": '',
                "report_to": '',
                "achievement": '',
                "salary": salary,
                "last_job": 0
            }]
            return job_list, job_list[0]
        for job in work_elements:
            # 2016.12 至 2017.5
            # 6个月 | 1年5个月
            company = job.xpath('.//div[@class="itemName"]/text()')[0] if job.xpath('.//div[@class="itemName"]/text()') else ""
            # 2015年09月-2017年09月（2年）
            start_end_ele = job.xpath('.//div[@class="project-content"]/p[starts-with(text(), "工作时间")]/span/text()')
            salary_ele = job.xpath('.//div[@class="project-content"]/p[starts-with(text(), "薪资水平")]/span/text()')
            position_ele = job.xpath('.//div[@class="project-content"]/p[starts-with(text(), "在职职位")]/span/text()')
            responsibility_ele = job.xpath('.//div[@class="title-content"]/div[@class="item-content"]/text()')
            start_end_str = start_end_ele[0] if start_end_ele else ""
            salary_ele_str = salary_ele[0] if salary_ele else 0  # 1000-2000
            position_str = position_ele[0] if position_ele else ""
            responsibility_str = responsibility_ele[0].replace("\n", "").replace("\t", "").replace(" ", "").strip() if responsibility_ele else ""
            if not responsibility_str:
                continue
            start_end = re.findall(r'\d+年\d+月-\d+年\d+月', start_end_str)[0].replace("年", '.').replace("月","").strip() if re.findall(
                r'\d+年\d+月-\d+年\d+月', start_end_str) else ""
            if "-" in salary_ele_str:
                salary_from = salary_ele_str.split("-")[0]
                salary_to = salary_ele_str.split("-")[1]
            else:
                salary_from = 0
                salary_to = 0
            start, end = self.start_end_str_to_unix(start_end)
            salary_str = job.xpath('div[@class="col-xs-9"]/div[contains(text(),"薪资")]/text()')
            # ‘薪资：1000-2000元/月’
            # ‘薪资：面议’

            salary = {
                'type': 1,
                'monthly_salary': {
                    'from': int(salary_from),
                    'to': int(salary_to),
                    'num_per_year': 12
                    },
                'annual_salary': {
                    'from': 0,
                    'to': 0
                    }
                }

            job_dict = {
                "start": start,
                "end": end,
                "industry": "",
                "company": company,
                "location": '',
                "work_year": "",
                "department": "",
                "position": position_str,
                "responsibility": responsibility_str,
                "report_to": "",
                "achievement": '',
                "salary": salary,
                "last_job": 1 if end == 999 else 0
            }
            job_list.append(job_dict)
        if len(job_list) == 0:
            job_list = [{
                "start": int(),
                "end": int(),
                "industry": list(),
                "company": '',
                "location": '',
                "work_year": int(),
                "department": '',
                "position": '',
                "responsibility": '',
                "report_to": '',
                "achievement": '',
                "salary": 0,
                "last_job": 0
            }]

        return job_list, job_list[0]  # new in v0.2: job_list[0] is the last job experience

    # 8/14
    def project_experience(self):  # 8/14
        project_list = list()
        t = self.tree
        box_element = t.xpath('//div[contains(text(),"项目经历")]')
        if not box_element:
            return [{
                "start": 0,
                "end": 0,
                "name": '',
                "description": '',
                "position": '',
                "company": '',
                "responsibility": '',
                "achievement": '',
                "other": ''
            }]
        projects_list = t.xpath('//div[contains(text(),"项目经历")]/following-sibling::*')
        projects = list()
        for p in projects_list:
            if p.xpath('self::*/@class')[0] != "rd-title":  # or if e.xpath('attribute::class')[0] != "rd-title": or e.xpath('@class')[0] != "rd-title"
                if p.xpath('self::*/@class')[0] != "rd-hline":
                    projects.append(p)
            else:
                break
        for project in projects:

            start_end = project.xpath('div[@class="col-xs-3"]/div[1]/text()')[0].strip()
            start, end = self.start_end_str_to_unix(start_end)
            name = project.xpath('div[@class="col-xs-9"]/div[1]/text()')[0].strip()
            position = ''
            company = ''
            achievement = ''
            try:
                project_description = project.xpath('div[@class="col-xs-9"]/div[contains(text(),"项目描述")]/following-sibling::pre[1]/text()')[0].strip()
            except IndexError:
                project_description = ''
            try:
                responsibility = project.xpath('div[@class="col-xs-9"]/div[contains(text(),"责任描述")]/following-sibling::pre[1]/text()')[0].strip()
            except:
                responsibility = ''
            project_dict = {
                "start": start,
                "end": end,
                "name": name,
                "description": project_description,
                "position": position,
                "company": company,
                "responsibility": responsibility,
                "achievement": achievement,
                "other": ''
            }
            project_list.append(project_dict)
        return project_list

    def language_skill(self):  # 9/14
        t = self.tree
        text = ''
        skill_list = list()
        default = {
                "skill_list": skill_list,
                # 因为目前（2016-07-14）对语言技能的处理还不够成熟，所以保留原始字段，交由人工判断
                "raw_string": text
            }
        return default

    # 10/14
    def professional_skill(self):  # 10/14
        t = self.tree
        skill_list = []
        return skill_list

    # 11/14
    def expect_job(self):  # 11/14
        t = self.tree
        element = t.xpath('//div[@class="expectInfo"]')
        if not element:
            return {
            "salary": {
                        "monthly_salary": {
                                "from": 0,
                                "to": 0
                        },
                        "type": 0
                },
            "position": list(),
            "industry": list(),
            "location": list(),
            "blocked_company": [],
            "company_stage": 0,
            "consider_startup_company": -1,
            "other": ""
        }
        location_str = self.check_exist(t.xpath('//*[@id="expectLocation"]/text()'))
        if location_str:
            location_list = location_str.split("、")
        else:
            location_list = list()
        salary_str = self.check_exist('//div[@class="expectInfo"]//p[@class="stonefont"]/text()').strip()
        position_str = self.check_exist(t.xpath('//*[@id="expectJob"]/text()'))

        # 不显示职位月薪范围
        # 期望月薪：8-10万元/年；面议
        # 期望月薪：2万以下元/年
        if "-" in salary_str:
            try:
                salary_from = re.findall('(\d+)\-',salary_str)[0]
                salary_from = int(salary_from)
                salary_to = re.findall('\-(\d+)',salary_str)[0]
                salary_to = int(salary_to)
                salary_dict = {
                    'type': 1,
                    'monthly_salary': {
                        'from': salary_from,
                        'to': salary_to
                    }
                }
            except:
                salary = int(int(re.findall('(\d+)',salary_str)[0])*10000/12)
                salary_dict = {
                    'type': 1,
                    'monthly_salary': {
                        'from': salary,
                        'to': salary
                    }
                }
        else:
            salary_dict = {
                'type': 0
            }

        # 数据分析、数据挖掘、搜索算法、推荐算法、自然语言处理
        position_list = list()
        if position_str:
            for i in re.split(r'[,、]',position_str):
                position_list.append(i.strip())
            if self.debug:
                print('position: ')
                for i in position_list:
                    print(('%d  _%s_' % (position_list.index(i), i)))

        # 计算机硬件、通信/电信运营
        industry_list = list()


        return {
            "salary": salary_dict,
            "position": position_list,
            "industry": industry_list,
            "location": location_list,
            "blocked_company": [],
            "company_stage": 0,
            "consider_startup_company": -1,
            "other": ""
        }

    # 12/14
    def additional_content(self):  # 12/14
        return ''

    # 13/14
    def jx_status(self):  # 13/14
        return {
            'jx_pass': -1
        }


    def crawler_info(self):  # 14/14
        # doc = self.doc

        return {
            "keyword": [],
            "crawler_update": time.time()
        }

    def active_info(self):
        """
        {\"b\":26,\"c\":0,\"d\":0,\"dw\":7,\"f\":3,\"r\":0,\"re\":1}"}
        \"be_viewed\":被浏览次数,
        \"check_company_phone_times\":查看过几家企业的电话
        \"apply_job_counts\":主动申请的职位数,
        \"be_download_counts\":被下载次数,
        \"be_interested_counts\":对他感兴趣的人数,
        \"be_interviewed_counts\":收到面试邀请次数}
        :return:
        """
        real_dic = json.loads(json.loads(self.add_dic).get("entity", {}))
        new_dic = {}
        new_dic["be_viewed"] =  real_dic.get("b", 0)
        new_dic["check_company_phone_times"] = real_dic.get("c", 0)
        new_dic["be_download_counts"]= real_dic.get("dw", 0)
        new_dic["be_interested_counts"]= real_dic.get("f", 0)
        new_dic["be_interviewed_counts"]= real_dic.get("re", 0)

        return new_dic

    def get_metadata(self):
        img = self.tree.xpath("//div[@class='rd-head-photo']/img/@src")
        if img:
            try:
                img = img[0]
            except:
                img = img
        else:
            img = str()
        return img

    def get_yoda(self):
        yoda = dict()
        try:
            yoda['avatar'] = self.tree.xpath("//div[@class='rd-head-photo']/img/@src")[0]
        except Exception:
            yoda['avatar'] = ''
        return yoda

    def auto_html_to_dict(self, html_doc=None, debug=False):
        self.debug = debug
        site = html_doc.get("site")
        self.source = SITE_SOURCE_MAP.get(site)
        if not self.source:
            raise Exception('config.py has not source on site: {}'.format(site))
        self.content = html_doc.get("content", "")
        if self.load_html(page_source=self.content):

            job_exp_list, last_job_exp = self.job_experience()

            return {
                # "_id": self.doc['_id'],
                # "jx_resume_id": str(self.doc['_id']),
                "resume_source": self.resume_source(),
                "active_info": self.active_info(),
                "profile": self.profile(),
                "location": self.location(),
                "education_experience": self.education_experience(),
                "award_experience": self.award_experience(),
                "job_experience": job_exp_list,
                'last_job_experience': last_job_exp,
                "project_experience": self.project_experience(),
                "language_skill": self.language_skill(),
                "professional_skill": self.professional_skill(),
                "expect_job": self.expect_job(),
                "additional_content": self.additional_content(),
                "jx_status": self.jx_status(),
                "crawler": self.crawler_info(),
                'metadata_FFng': self.get_metadata(),
                "_yoda": self.get_yoda(),
            }
        else:
            return None



    #
    # def auto_html_to_dict(self, html_doc=None, debug=False):
    #     self.debug = debug
    #     site = html_doc.get("site")
    #     self.source = SITE_SOURCE_MAP.get(site)
    #     if not self.source:
    #         raise Exception('config.py has not source on site: {}'.format(site))
    #     self.content = html_doc.get("content", "")
    #     if self.load_html(page_source=self.content):
    #         self.resume_info()  # 调核心解析函数
    #         return self.resume
    #     else:
    #         return None


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




