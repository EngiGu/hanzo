import time

import hashlib
import json
from core.mongo_db import MongoDb
from core.asredis import NoAsRedis
import logging
from config import *
from copy import deepcopy

MT_cp = MongoDb("aizhaopin", "company_infos")
cards = NoAsRedis(C_REDIS_HOST, C_REDIS_PORT, C_REDIS_DB)


def resume_develop(resume):
    hashed_key = hashlib.md5(
        json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-8]
    hashed_id = int(hashed_key, 16)
    return hashed_id


def company_update_func(resume):
    res = MT_cp.search({"jx_resume_id": resume["jx_resume_id"]})
    st = time.time()
    if not res:
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
        cards.incr(f'{resume["source"]}_{time.strftime("%Y-%m-%d", time.localtime())}')
        cards.incr(f'{resume["source"]}_total')
        logging.info(f"inserted jx_resume_id: {resume['jx_resume_id']}")
    else:
        develop_old = res.get("develops", [])
        develop_new = resume.get("develops", [])  # 2019-6-5 修改develop的更新逻辑
        deep_old = deepcopy(develop_old)[-1]
        deep_new = deepcopy(develop_new)[0]
        deep_old.pop("update_time")
        deep_new.pop("update_time")
        if resume_develop(deep_old) != resume_develop(deep_new):
            resume["develops"] = develop_old + develop_new
        else:
            develop_old[-1]["update_time"] = develop_new[0]["update_time"]
            resume["develops"] = develop_old
        MT_cp.update({"jx_resume_id": resume["jx_resume_id"]}, resume)
        cards.incr(f'{resume["source"]}_{time.strftime("%Y-%m-%d", time.localtime())}')
        logging.info(f"updated jx_resume_id: {resume['jx_resume_id']}")
    logging.info(f"jx_resume_id: {resume['jx_resume_id']} mongo operate cost {(time.time() - st):.3f} s.")


def hr58_update(resume):
    logging.info(f"hr58 update: {str(resume)}")


def mongo_ur(resume: dict):
    # print('*'*5, resume)
    # return
    source = resume.get("source", None)

    if source in range(200, 300):
        company_update_func(resume)
    elif source == 22:
        hr58_update(resume)
    else:
        raise Exception(f"source num: {source} wrong: {resume}")


if __name__ == '__main__':
    mongo_ur('xxx')
