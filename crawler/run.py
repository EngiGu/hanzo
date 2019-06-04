import json
import os
import sys
import time
import traceback
import requests

from config import *
from core.func import load_module
from core.exceptions import *
from core.rabbitmq import MqSession
from core.logger import Logger

# import logging

SPIDERS_MAPS = load_module('spiders', __file__, 'cp_')

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')
#

class Run:
    def __init__(self, site, st_flag=100):
        self.site = site

        # self.logger = logging
        self.logger = Logger(f'run_{site}_{st_flag}')
        self.mq = MqSession(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_EXCHANGE)

        # self.logger.info(f'loaded list parser: {str(EXTRACT_LIST)}')
        # self.logger.info(f'loaded detail parser: {str(EXTRACT_RESUME)}')
        self.logger.info(f'loaded spiders: {str(SPIDERS_MAPS)}')

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

        retry_times = 8
        if action.lower() == 'get':
            for _ in range(retry_times):
                try:
                    res = requests.get(REDIS_TASK_URI, params={'site': site}, timeout=10).json()
                    if res['code'] == 0:
                        return json.loads(res['task'])
                    return None
                except Exception as e:
                    l.warning(f'apply task error: {e.__context__}, tb: {traceback.format_exc()}')
            raise ApplyRequestError('apply task request error.')
        elif action.lower() == 'push':
            for _ in range(retry_times):
                try:
                    res = requests.post(REDIS_TASK_URI, data=task, timeout=10).json()
                    if res['code'] == 0:
                        l.info(f'push task: {str(task)} to queue success.')
                    return
                except Exception as e:
                    l.warning(f'push task error: {e.__context__}, tb: {traceback.format_exc()}')
            raise ApplyRequestError('push task request error.')
        else:
            raise ApplyActionError(f'task action: {action} error..')

    # def parser(self, site, type, res, curr_task, failed=False):
    #     """
    #
    #     :param site:
    #     :param type:
    #     :param res: {"site":"boss", "content":"<html></html>", "resume_info": curr_task}
    #     :param curr_task: 当前任务信息
    #     :param failed: 是否是之前失败的任务
    #     :return:
    #     """
    #     l = self.logger
    #     _res = {"site": site, "content": res, "resume_info": curr_task}
    #     if type == 1:
    #         list_parser = EXTRACT_LIST.get(site, None)
    #         if not list_parser:
    #             raise ListParseDoNotExists(f'site: {self.site} has no corresponding list parser.')
    #         try:
    #             detail = list_parser().parser(_res)
    #             detail_list = detail['resume_list']
    #             current_page = detail['current_page']
    #             last_page = detail['last_page']
    #             for one in detail_list:
    #                 hash_key = one.get("hashed_key", 0)
    #                 if bfr.is_exists(hash_key):  # todo 布隆list过滤
    #                     l.info(f"site: {site} task has crawled before, skip. task: {str(one)}")
    #                     continue
    #                 data = {
    #                     'type': 2,
    #                     'site': site,
    #                     'origin_task': curr_task,
    #                     'list_task': one
    #                 }
    #                 task_data = {'task': json.dumps(data)}
    #                 push_res = self.apply_task(action='push', task=task_data)
    #                 if push_res['code'] == 0:
    #                     l.info(f'has pushed site: {site} {str(task_data)}')
    #                 else:
    #                     l.info(f'pushed site wrong: {site} {str(task_data)} \n wrong code {push_res["code"]}')
    #             if last_page > current_page:
    #                 _curr_task = curr_task
    #                 _curr_task['page'] += 1
    #                 _curr_task['origin_task'] = curr_task
    #                 _curr_task['type'] = 3
    #                 task_data = {'task': json.dumps(_curr_task)}
    #                 if not failed:
    #                     # 不是失败队列过来的任务,解决失败一直翻页问题
    #                     self.apply_task(action='push', task=task_data)
    #         except Exception as e:
    #             _curr_task = curr_task
    #             _curr_task['type'] = 4
    #             task_data = {'task': json.dumps(_curr_task)}
    #             self.apply_task(action='push', task=task_data)
    #             l.warning(f'parse list error: {e.__context__}, tb: {traceback.format_exc()}')
    #
    #     elif type == 2:
    #         detail_parser = EXTRACT_RESUME.get(site, None)
    #         if not detail_parser:
    #             raise DetailParseDoNotExists(f'site: {self.site} has no corresponding detail parser.')
    #         try:
    #             detail = detail_parser().auto_html_to_dict(_res)
    #             if not detail:
    #                 l.info(f"site: {site} detail parse res: None")
    #                 _curr_task = curr_task
    #                 _curr_task['type'] = 5  # type2 解析失败放回失败队列
    #                 data = {'task': json.dumps(_curr_task)}
    #                 self.apply_task(action='push', task=data)
    #                 l.info(f"has pushed site: {site} to type5 queue, task: {str(_curr_task)}")
    #                 return
    #             # todo insert mongo
    #             # resume计算去重
    #             mongo_ur(detail)  # todo 测试一下
    #
    #
    #         except Exception as e:
    #             _curr_task = curr_task
    #             _curr_task['type'] = 5  # type2 解析失败放回失败队列
    #             data = {'task': json.dumps(_curr_task)}
    #             self.apply_task(action='push', task=data)
    #             l.info(f"has pushed site: {site} to type5 queue, task: {str(_curr_task)}")
    #             l.warning(f'parse detail task error: {e.__context__}, tb: {traceback.format_exc()}')

    def push_to_rabbitmq(self, site, type, curr_task, content):
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        elif isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        if content:
            msg = {"site": site, "type": type, "content": content, "curr_task": curr_task}
            msg = json.dumps(msg, ensure_ascii=False)
            st = time.time()
            self.mq.put(QUEUE, msg)
            self.logger.info(f"push crawl content(len: {len(content)}) to rabbitmq cost"
                             f" {(time.time() - st) * 1000:.3f} ms.")

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

                    c = SPIDERS_MAPS[self.site](self.logger)

                    if type in [1, 3, 4]:
                        try:

                            res = c.query_list_page(one_task['keyword'], one_task['page'])
                            # res = """html test!!!!
                            # """
                            print('res:', res)
                        except Exception as e:
                            l.error(f'spider query_list_page error: {e.__context__}, tb: {traceback.format_exc()}')
                            raise SpiderError('query_list_page error')
                        # TODO parse list
                        # self.parser(site, type, res, one_task, failed=True if type == 4 else False)
                        self.push_to_rabbitmq(site, type, one_task, res)
                        # sys.exit(666)

                    elif type in [2, 5]:
                        try:
                            res = c.query_detail_page(one_task['url'])
                            # res = """html test type2 !!!!
                            #                             """
                            print('res:', res)
                        except Exception as e:
                            l.error(f'spider query_detail_page error: {e.__context__}, tb: {traceback.format_exc()}')
                            raise SpiderError('query_detail_page error')
                        # TODO parse detail
                        # self.parser(site, type, res, one_task, failed=False)
                        self.push_to_rabbitmq(site, type, one_task, res)
                        # sys.exit(666)

                    else:
                        raise ApplyTypeError(f'apply task type: {type} not in [1,2,3,4,5]!')
                sys.exit()

            except (ListParseDoNotExists, DetailParseDoNotExists, ApplyTypeError, ApplyActionError, ApplySiteError):
                l.error('fatal error, exit...')
                sys.exit()
            except SpiderError:
                l.error('spider error, exit...')
                sys.exit()
            except ApplyRequestError:
                l.error('apply task request error, exit...')
                sys.exit()
            except Exception as e:
                l.warning(f'main run loop error: {e.__context__}, tb: {traceback.format_exc()}')
                sys.exit()


if __name__ == '__main__':
    from multiprocessing import Process
    print(SPIDERS_MAPS)
    site = sys.argv[1]
    if site not in SPIDERS_MAPS:
        raise SpiderDoNotExists(f"no site's spider found!")

    st_flag = 100
    p_list = []
    for i in range(NUM_PER_MACHINE):
        p =  Process(target=Run(site=site, st_flag=st_flag+i).run, name=f'Process-{site}-{st_flag+i}')
        p.start()
        p_list.append(p)
        time.sleep(30)

    for p in p_list:
        p.join()