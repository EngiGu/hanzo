import hashlib
import json
import os, sys, traceback
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import logging

from core.func import load_module
from core.exceptions import *
from core.asredis import AsRedis
from bloom.connection import BFR as bfr
from bloom.connection import TEST_BFR as tbfr
from mongo_operate import mongo_ur
from config import *

EXTRACT_LIST = load_module('lists', __file__, "List_")
EXTRACT_RESUME = load_module("resumes", __file__, "Resume_")

ards = AsRedis(REDIS_HOST, REDIS_PORT, REDIS_DB)


def cala_58(resume):
    """58职位和求职去重计算特征值"""
    source = resume['source']
    if source == 23:  # 58job
        # """ job 字段
        # 'company': company,
        # 'url': url,
        # 'salary': {'from': salary_from, 'to': salary_to},
        # 'tag': tag,  # 职位福利tags
        # 'degree': degree,
        # 'work_experience': {'from': work_from, 'to': work_to},  # 工作年限
        # 'position': position,  # 职位类型
        # 'position_title': position_title,  # 职位标题
        # 'put_type': put_type,  # 职位投放类型 精准 置顶还是什么
        # 'pub_time': self.__return_format_time(pub_time),
        # 'crawl_time': self.__return_format_time(now),  # 抓取时间
        # 'source': self.source
        # """
        # resume.pop('url')
        # resume.pop('put_type')
        # resume.pop('pub_time')
        # resume.pop('crawl_time')
        to_cal = {
            'company': resume['company'],
            'salary': resume['salary'],
            'tag': resume['tag'],
            'degree': resume['degree'],
            'work_experience': resume['work_experience'],
            'position': resume['position'],
            'position_title': resume['position_title'],
        }
    elif source == 24:
        # """ hr58 字段
        #   'age': 25,
        #   'ageText': '25',
        #   'campusResume': '0',
        #   'complete': '50',
        #   'crawl_time': {'Ymd': '2019-07-12',
        #                  'YmdHMS': '2019-07-12 15:32:59',
        #                  'stamp': 1562916779.0049305},
        #   'degree': 0,
        #   'downLoadUserId': '0',
        #   'education': '中专/技校',
        #   'expectArea': '武汉江岸区',
        #   'expectCateIds': '3196',
        #   'expectCityIds': '159',
        #   'experCos': '',
        #   'experCount': '',
        #   'experYears': '',
        #   'experiences': [],
        #   'followParam': '%7B%22searchID%22%3A%22264e6eceaa49435ead7c9788e1d4b9df%22%2C%22searchVersion%22%3A0%2C%22searchAreaID%22%3A159%2C%22searchFirstAreaID%22%3A158%2C%22searchPositionID%22%3A0%2C%22searchSecondPositionID%22%3A0%2C%22page%22%3A1%2C%22location%22%3A53%2C%22resumeType%22%3A1%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-viplist-gengxin%22%2C%22operatePage%22%3A%22list%22%7D',
        #   'hasFindJob': '0',
        #   'infoID': '0',
        #   'isDelete': False,
        #   'isDownload': None,
        #   'isFree': None,
        #   'isValidaMobile': True,
        #   'letter': '',
        #   'lightSpotCount': '0',
        #   'lspot': [],
        #   'mobile': '',
        #   'namelimit': '0',
        #   'nowPosition': '――',
        #   'picCount': '0',
        #   'picUrl': '//img.58cdn.com.cn/m58/app58/m_static/img/job/resume/randomboy.png',
        #   'pub_time': {'Ymd': '2019-07-11',
        #                'YmdHMS': '2019-07-11 16:47:54',
        #                'stamp': 1562834874},
        #   'pushResume': '3',
        #   'rencaikulink': None,
        #   'resumeID': '3_neypnvnfTEysnvZX_eyplEDk_E6sTEOQ_EzknpsunGyYnGnQMGOfn-5fTegknGrsnEralEyNTeyX',
        #   'resumeTp': '学徒',
        #   'salary': {'from': 0, 'to': 0},
        #   'school': '',
        #   'searchId': '264e6eceaa49435ead7c9788e1d4b9df',
        #   'searchVersion': '0',
        #   'sex': 1,
        #   'sexText': '男',
        #   'shortUpdateDate': None,
        #   'showDelButton': True,
        #   'source': 202,
        #   'sources': None,
        #   'targetArea': '武汉江岸区',
        #   'targetAreaId': '159',
        #   'targetPosition': '学徒',
        #   'targetSalary': '面议',
        #   'trueName': '涂奔',
        #   'updateDate': '2019-07-11',
        #   'updateDateTimeStamp': '1562834874000',
        #   'url': '//jianli.58.com/resumedetail/single/3_neypnvnfTEysnvZX_eyplEDk_E6sTEOQ_EzknpsunGyYnGnQMGOfn-5fTegknGrsnEralEyNTeyX?sourcepath=pc-viplist-gengxin&followparam=%7B%22searchID%22%3A%22264e6eceaa49435ead7c9788e1d4b9df%22%2C%22searchVersion%22%3A0%2C%22searchAreaID%22%3A159%2C%22searchFirstAreaID%22%3A158%2C%22searchPositionID%22%3A0%2C%22searchSecondPositionID%22%3A0%2C%22page%22%3A1%2C%22location%22%3A53%2C%22resumeType%22%3A1%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-viplist-gengxin%22%2C%22operatePage%22%3A%22list%22%7D',
        #   'userID': '518574571',
        #   'workYear': '5-10年工作经验',
        #   'work_experience': {'from': 5, 'to': 10}}
        # """
        to_cal = {
            # 'userID': resume['userID'],
            'trueName': resume['trueName'],
            'sexText': resume['sexText'],
            'ageText': resume['ageText'],
            'education': resume['education'],
        }
    else:
        raise Exception('source: {} error'.format(source))
    print('--->>>to_cal', to_cal)
    hashed_key = hashlib.md5(json.dumps(to_cal, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-11]
    hashed_id = int(hashed_key, 16)
    return hashed_id


def cal_jx_resume_id(resume):
    resume = deepcopy(resume)
    return cala_58(resume)


# @time_count
async def handler(msg: dict, mode: str, logger: logging):
    # rabbitmq  消息格式：Str '{"site": "cccc", "type: 1, "content": "content.....", "curr_task": "yyyyy"}'
    # l = logging
    site = msg['site']
    l = logging.LoggerAdapter(logger, extra={'site': site})
    _res = {"site": site, "content": msg['content'], "curr_task": msg['curr_task']}

    if msg['type'] in [1, 3, 4]:
        # list_parser = DISPATCH_KEY_MAP.get(site)['list_parser']
        list_parser = EXTRACT_LIST.get(site, None)
        if not list_parser:
            raise ListParseDoNotExists(f'has no corresponding list parser.')
        try:
            detail = list_parser().parser(msg['content'])
            detail_list = detail['resume_list']
            if not detail['resume_list']:
                l.info(f"list parse resume_list is empty list.")
            current_page = detail['current_page']
            last_page = detail['last_page']
            for one in detail_list:
                l.info(f"parse list one res: {str(one)} ")
                hash_key = one.get("hashed_key", 0)
                # TODO 取消掉当日去重
                # bloom = bfr if mode == 'online' else tbfr
                # if bloom.is_exists(str(hash_key)):  # todo 布隆list过滤
                #     l.info(f"task has crawled before, skip. task: {str(one)}")
                #     continue
                data = json.dumps({
                    'type': 2,
                    'site': site,
                    'url': one['url'],
                    'origin_task': msg['curr_task'],
                }, ensure_ascii=False)
                await ards.push('%s_2' % site, data)
                l.info(f'has generated new type2 task: {data}, pushed successfully.')
            l.info(f"page: {current_page} -> {last_page}")
            if last_page > current_page:
                next_page_task = deepcopy(msg['curr_task'])
                _curr_task = deepcopy(msg['curr_task'])
                next_page_task['page'] += 1
                if 'origin_task' in _curr_task:
                    _curr_task.pop('origin_task')
                next_page_task['origin_task'] = _curr_task
                next_page_task['type'] = 3
                task_data = json.dumps(next_page_task, ensure_ascii=False)
                '''
                    1: 'import task',
                    2: 'parse to type2',
                    3: 'parse to type1',
                    4: 'parse type1 error',
                    5: 'parse type2 error'
                '''
                if msg['type'] != 4:
                    # 这个条件主要是防止之前失败的任务一直重复生成新的翻页type1
                    await ards.push('%s_3' % site, task_data)
                    l.info(f'has generated new type1 task: {next_page_task}, pushed successfully.')
        except Exception as e:
            _curr_task = msg['curr_task']
            _curr_task['type'] = 4
            failed_type1_task = json.dumps(_curr_task, ensure_ascii=False)
            await ards.push('%s_4' % site, failed_type1_task)
            l.info(f'parse list Error, has pushed to type4 queue. task: {failed_type1_task}, error: '
                   f'{e.__context__}, tb: {traceback.format_exc()}')

    elif msg['type'] in [2, 5]:
        # detail_parser = DISPATCH_KEY_MAP.get(site)['resume_parser']
        detail_parser = EXTRACT_RESUME.get(site, None)
        if not detail_parser:
            raise DetailParseDoNotExists(f'has no corresponding detail parser.')
        try:
            detail = detail_parser().auto_html_to_dict(_res)
            l.info(f"detail parse res: {str(detail)}")
            if isinstance(detail, list):
                if not detail:
                    # 当前翻页里的搜索结果为空
                    l.info(f"page is a empty page...continue...")
                    return 
            if not detail:
                _curr_task = msg['curr_task']
                _curr_task['type'] = 5  # type2 解析失败放回失败队列
                failed_type2_task = json.dumps(_curr_task, ensure_ascii=False)
                await ards.push('%s_5' % site, failed_type2_task)
                l.info(f"parse resume None, has pushed to type5 queue, task: {str(_curr_task)}")
                return
            ## 只是58爬取解析返回的是list,因为只是爬取list页面
            if isinstance(detail, list):
                for d in detail:
                    d['jx_resume_id'] = cal_jx_resume_id(d)  # 15位整形的hash_id
                    mongo_ur(d, mode=mode, logger=l)
            else: # 解析返回的是dict
                detail['jx_resume_id'] = cal_jx_resume_id(detail)  # 15位整形的hash_id
                mongo_ur(detail, mode=mode, logger=l)

        except Exception as e:
            _curr_task = msg['curr_task']
            _curr_task['type'] = 5  # type2 解析失败放回失败队列
            failed_type2_task = json.dumps(_curr_task, ensure_ascii=False)
            await ards.push('%s_5' % site, failed_type2_task)
            l.error(f"parse resume Error, has pushed to type5 queue, task: {str(_curr_task)}, "
                    f"error: {e.__context__}, tb: {traceback.format_exc()}")

    else:
        raise Exception(f'parser type: {msg["type"]} error!')

    del l


if __name__ == '__main__':
    print(EXTRACT_LIST)
    print(EXTRACT_RESUME)
    # print(DISPATCH_KEY_MAP)
    pass
