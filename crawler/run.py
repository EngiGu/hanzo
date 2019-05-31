# import asyncio
import json
import os
import random, importlib, inspect
import sys
import traceback

import requests

from config import REDIS_TASK_URI, ROOT_PATH
from core.func import load_module
from core.exceptions import *
from extractor.handel import EXTRACT_LIST, EXTRACT_RESUME

import logging

SPIDERS_MAPS = load_module(os.path.join(ROOT_PATH, 'spiders'), 'cp_')
print(EXTRACT_LIST, EXTRACT_RESUME)


class Run:
    def __init__(self, site):
        self.site = site
        self.logger = logging
        pass

    def apply_task(self, action="get", site=None, task=None):
        '''
        {
        code: 0,
        msg: "success",
        task: "{"page":1, "keyword": "广州一招制胜信息科技有限公司", "site":"zhilian"}"
        }
        :param action:
        :return:
        '''
        l = self.logger
        if action.lower() == 'get':
            try:
                res = requests.get(REDIS_TASK_URI, params={'site': site}, timeout=10).json()
                print(res)
                if res['code'] == 0:
                    return json.loads(res['task'])
            except Exception as e:
                l.warning(f'apply task error: {e.__context__}, tb: {traceback.format_exc()}')
            return None
        elif action.lower() == 'push':
            try:
                print('*'*10, task)
                res = requests.post(REDIS_TASK_URI, data=task, timeout=10).json()
                if res['code'] == 0:
                    l.info(f'push task: {str(task)} to queue success.')
            except Exception as e:
                l.warning(f'push task error: {e.__context__}, tb: {traceback.format_exc()}')
        else:
            raise ApplyActionError(f'task action: {action} error..')

    def parser(self, site, type, res, curr_task, failed=False):
        """

        :param site:
        :param type:
        :param res: 要解析的内容
        :param curr_task: 当前任务信息
        :param failed: 是否是之前失败的任务
        :return:
        """
        l = self.logger

        if type == 1:
            list_parser = EXTRACT_LIST.get(site, None)
            if not list_parser:
                raise ListParseDoNotExists(f'site: {self.site} has no corresponding list parser.')
            try:
                detail = list_parser().parser(res)
                raise Exception
                if not detail:
                    l.info(f"site: {site} list parse res: None") #TODO 其实解析失败不返回None
                    print(f"site: {site} list parse res: None") #TODO 其实解析失败不返回None
                    return
                detail_list = detail['resume_list']
                current_page = detail['current_page']
                last_page = detail['last_page']
                for one in detail_list:
                    data ={
                        'type': 2,
                        'site': site,
                        'origin_task': curr_task,
                        'list_task': one
                    }
                    data = {'task': json.dumps(data)}
                    res = self.apply_task(action='push', task=data)
                    if res['code'] == 0:
                        l.info(f'has pushed site: {site} {str(data)}')
                if last_page > current_page:
                    _curr_task = curr_task
                    _curr_task['page'] += 1
                    _curr_task['origin_task'] = curr_task
                    _curr_task['type'] = 3
                    data = {'task': json.dumps(_curr_task)}
                    if not failed:
                        # 不是失败队列过来的任务,解决失败一直翻页问题
                        self.apply_task(action='push', task=data)
            except Exception as e:
                _curr_task = curr_task
                _curr_task['type'] = 4
                data = {'task': json.dumps(_curr_task)}
                self.apply_task(action='push', task=data)
                l.warning(f'parse list error: {e.__context__}, tb: {traceback.format_exc()}')

        elif type == 2:
            detail_parser = EXTRACT_RESUME.get(site, None)
            if not detail_parser:
                raise DetailParseDoNotExists(f'site: {self.site} has no corresponding detail parser.')
            try:
                detail = detail_parser().auto_html_to_dict(res)
                if not detail:
                    l.info(f"site: {site} detail parse res: None")
                    _curr_task = curr_task
                    _curr_task['type'] = 5  # type2 解析失败放回失败队列
                    data = {'task': json.dumps(_curr_task)}
                    self.apply_task(action='push', task=data)
                    l.info(f"has pushed site: {site} to type5 queue, task: {str(_curr_task)}")
                    return
                # todo  insert mongo
            except Exception as e:
                _curr_task = curr_task
                _curr_task['type'] = 5  # type2 解析失败放回失败队列
                data = {'task': json.dumps(_curr_task)}
                self.apply_task(action='push', task=data)
                l.info(f"has pushed site: {site} to type5 queue, task: {str(_curr_task)}")
                l.warning(f'parse detail task error: {e.__context__}, tb: {traceback.format_exc()}')


    def run(self):
        l = self.logger
        if self.site not in SPIDERS_MAPS:
            raise SpiderDoNotExists(f'site: {self.site} has no corresponding crawler.')

        while True:
            try:
                one_task = self.apply_task(action='get', site=self.site)
                print('one_task:', one_task)
                l.info(f'get site: {site}, task: {str(one_task)}')
                if one_task:
                    type = one_task.get('type', None)
                    if not type:
                        raise ApplyTypeError('apply task has no type!')

                    c = SPIDERS_MAPS[self.site]()

                    if type in [1, 3, 4]:
                        try:
                            res = c.query_list_page(one_task['keyword'], one_task['page'])
                        except Exception as e:
                            l.error(f'spider query_list_page error: {e.__context__}, tb: {traceback.format_exc()}')
                            raise SpiderError('query_list_page error')
                        # TODO parse list
                        self.parser(site, type, res, one_task, failed=True if type == 4 else False)

                    elif type in [2, 5]:
                        try:
                            res = c.query_detail_page(one_task['url'])
                        except Exception as e:
                            l.error(f'spider query_detail_page error: {e.__context__}, tb: {traceback.format_exc()}')
                            raise SpiderError('query_detail_page error')
                        # TODO parse detail
                        self.parser(site, type, res, one_task, failed=False)
                    else:
                        raise ApplyTypeError(f'apply task type: {type} not in [1,2,3,4,5]!')
                # sys.exit()

            except (ListParseDoNotExists, DetailParseDoNotExists, ApplyTypeError, ApplyActionError, ApplySiteError):
                l.error('fatal error, exit...')
                sys.exit()
            except SpiderError:
                l.error('spider error, exit...')
                sys.exit()
            except Exception as e:
                l.warning(f'main run loop error: {e.__context__}, tb: {traceback.format_exc()}')


if __name__ == '__main__':
    print(SPIDERS_MAPS)
    site = 'dajie'

    r = Run(site)
    r.run()
