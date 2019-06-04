import time

from core.mongo_db import MongoDb
from core.asredis import NoAsRedis
import logging
from config import *


MT_cp = MongoDb("aizhaopin", "company_infos")
cards = NoAsRedis(C_REDIS_HOST, C_REDIS_PORT, C_REDIS_DB)


def company_update_func(resume):
    res = MT_cp.search({"jx_resume_id": resume["jx_resume_id"]})
    if not res:
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
        cards.incr(f'{resume["source"]}_{time.strftime("%Y-%m-%d", time.localtime())}')
        cards.incr(f'{resume["source"]}_total')
        logging.info(f"inserted jx_resume_id: {resume['jx_resume_id']}")
    else:
        develop_old = res.get("develops", [])
        develop_new = resume.get("develops", [])
        resume["develops"] = develop_old + develop_new
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
        cards.incr(f'{resume["source"]}_{time.strftime("%Y-%m-%d", time.localtime())}')
        logging.info(f"updated jx_resume_id: {resume['jx_resume_id']}")



def mongo_ur(resume: dict):
    # print('*'*5, resume)
    # return
    source = resume.get("source", None)

    if source in range(200, 300):
        company_update_func(resume)
    else:
        raise Exception(f"source num: {source} wrong: {resume}")


if __name__ == '__main__':
    mongo_ur('xxx')
