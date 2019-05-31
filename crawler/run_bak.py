# import asyncio
import json
import os
import random, importlib, inspect
import traceback

import requests

from config import REDIS_TASK_URI
from core.func import load_module
from core.exceptions import *
import logging

SPIDERS_MAPS = load_module('spiders', 'cp_')


class Run:
    def __init__(self):
        self.logger = logging
        pass

    def apply_task(self, action="get", task=None):
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
                res = requests.get(REDIS_TASK_URI, timeout=10).json()
                if res['code'] == 0:
                    return json.loads(res['task'])
            except Exception as e:
                l.warning(f'apply task error: {e.__context__}, tb: {traceback.format_exc()}')
            return None
        elif action.lower() == 'push':
            try:
                res = requests.post(REDIS_TASK_URI, data=task, timeout=10).json()
                if res['code'] == 0:
                    l.info(f're push task: {str(task)} to queue success.')
            except Exception as e:
                l.warning(f're push task error: {e.__context__}, tb: {traceback.format_exc()}')
        else:
            raise ApplyActionError(f'task action: {action} error..')

    def run(self):
        l = self.logger
        while True:
            try:
                one_task = self.apply_task(action='get')
                if one_task:
                    site = one_task.get('site', None)
                    if not site:
                        raise ApplySiteError('apply task has no site!')
                    type = one_task.get('type', None)
                    if not site:
                        raise ApplyTypeError('apply task has no type!')

                    crawler = SPIDERS_MAPS.get(site, None)
                    if not crawler:
                        raise SpiderDoNotExists(f'site: {site} has no corresponding crawler.')

                    c = crawler()
                    if type == 1:
                        res = c.query_list_page(one_task['keyword'], one_task['page'])
                        # TODO parse list
                    elif type == 2:
                        res = c.query_detail_page(one_task['url'])
                        # TODO parse detail
                    else:
                        raise ApplyTypeError(f'apply task type: {type} not in 1 or 2!')

            except Exception as e:
                l.warning(f'main run loop error: {e.__context__}, tb: {traceback.format_exc()}')


if __name__ == '__main__':
    print(SPIDERS_MAPS)

    # r = Run()
    # r.run()
