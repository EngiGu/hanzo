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


def cal_jx_resume_id(resume):
    resume = deepcopy(resume)
    if isinstance(resume, dict):
        if resume['source'] > 200:
            pop_list = ["id", "develops", "office_cities", "tag", "cxos", "productions", "introduce", "logo", "shareholders"]
        elif 90 < resume['source'] < 200:
            pop_list = ['id', 'introduce', 'create_time', 'update_time', 'tag']
        elif resume['source'] == 303:
            return 0
        else:
            raise Exception('source: %r is invailed.' % resume['source'])
        for key in pop_list:
            if key in resume:
                resume.pop(key)
        hashed_key = hashlib.md5(
            json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')
        ).hexdigest()[8:-11]
        hashed_id = int(hashed_key, 16)
        return hashed_id
    else:
        return 0


# @time_count
async def handler(msg: dict, mode: str, logger):
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
                if site not in DO_NOT_NEED_BLOOM:
                    bloom = bfr if mode == 'online' else tbfr
                    if bloom.is_exists(str(hash_key)):  # todo 布隆list过滤
                        l.info(f"task has crawled before, skip. task: {str(one)}")
                        continue
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
            if not detail:
                _curr_task = msg['curr_task']
                _curr_task['type'] = 5  # type2 解析失败放回失败队列
                failed_type2_task = json.dumps(_curr_task, ensure_ascii=False)
                await ards.push('%s_5' % site, failed_type2_task)
                l.info(f"parse resume None, has pushed to type5 queue, task: {str(_curr_task)}")
                return
            if cal_jx_resume_id(detail):  # 15位整形的hash_id
                detail['jx_resume_id'] = cal_jx_resume_id(detail)
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
