import time

import hashlib
import json
from core.mongo_db import MongoDb
from core.asredis import NoAsRedis
from core.mysql import session_scope
from core.schema import DailyHrCrawl, DailyJobCrawl
import logging
from config import *
from copy import deepcopy


# MT_cp = MongoDb("aizhaopin", "tc58")
MT_cp = MongoDb("aizhaopin", "tongcheng_58_new")
# cards = NoAsRedis(C_REDIS_HOST, C_REDIS_PORT, C_REDIS_DB)



def hr58_update(resume, logger):
    # logger.info(f"hr58 update: {str(resume)}")
    source = resume["source"]
    update_day = resume['pub_time']['Ymd']
    today = time.strftime("%Y-%m-%d", time.localtime())
    # is_today_update = 1 if today == update_day else 0
    # resume['is_today_update'] = is_today_update

    if today == update_day:
        is_today_update = 1
        # rds_key = '{}_{}'.format(source, today)
        # cards.incr(rds_key)
        logger.info(f'{resume["jx_resume_id"]} is today update!')
    else:
        is_today_update = 0
        logger.info(f'{resume["jx_resume_id"]} is NOT today update!')
    resume['is_today_update'] = is_today_update

    # today_total_key = '{}_{}_{}'.format(source, today, 'total')
    # total_key = '{}_{}'.format(source, 'total')
    # cards.incr(today_total_key)
    # cards.incr(total_key)
    if source == SITE_SOURCE_MAP['job58']:
        d = DailyJobCrawl(
            jx_resume_id=resume['jx_resume_id'],
            position=resume['position']
        )
        logger.info(f"job58 update: {str(resume)}")
    elif source == SITE_SOURCE_MAP['hr58']:
        d = DailyHrCrawl(
            jx_resume_id=resume['jx_resume_id'],
            position=resume['targetPosition'],
            positions=resume['resumeTp'],
        )
        logger.info(f"hr58 update: {str(resume)}")
    else:
        raise Exception('insert mysql source error, jx_resume_id: {}'.format(resume['jx_resume_id']))

    with session_scope() as s:
        s.add(d)  # 插入mysql统计表

    MT_cp.insert(resume)

def mongo_ur(resume: dict, mode: str, logger: logging):
    # print('*'*5, resume)
    # return

    if mode == 'online':
        hr58_update(resume, logger=logger)

        # source = resume.get("source", None)
        #
        # if source in range(200, 300):
        #     company_update_func(resume, logger=logger)
        # elif source == 22:
        #     hr58_update(resume, logger=logger)
        # else:
        #     raise Exception(f"source num: {source} wrong: {resume}")
    else:
        logger.info(f"mongo run mode: {mode}, resume: {str(resume)}")


if __name__ == '__main__':
    mongo_ur('xxx')
