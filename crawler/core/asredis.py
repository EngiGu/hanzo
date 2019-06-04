import asyncio
import time
import traceback
from inspect import iscoroutinefunction

import aredis
import redis
import logging


def redis_retry(func):
    def wrapper(self, *args, **kwargs):
        for _ in range(5):
            try:
                func(self, *args, **kwargs)
                return
            except:
                logging.error(f"redis error with retry:{_+1} ::: {traceback.format_exc()}")
                self.init_redis()
                # func(self, *args, **kwargs)

    async def as_wrapper(self, *args, **kwargs):
        for _ in range(5):
            try:
                await func(self, *args, **kwargs)
                return
            except:
                logging.error(f"redis error with retry:{_+1} ::: {traceback.format_exc()}")
                self.init_redis()
                # func(self, *args, **kwargs)

    return as_wrapper if iscoroutinefunction(func) else wrapper


class AsRedis:
    def __init__(self, host, port, db):
        # self.redis_client = self.aredis_cli(host, port, db)
        # print(self.redis_client)
        self.init_redis(host, port, db)

    def init_redis(self, host, port, db):
        self.redis_client = aredis.StrictRedis(
            connection_pool=aredis.ConnectionPool(host=host, port=port, db=db),
            decode_responses=True,  # 自动解码
        )

    @redis_retry
    async def push(self, key: object, value: object):
        await self.redis_client.lpush(key, value)

    @redis_retry
    async def len(self, key):
        return await self.redis_client.llen(key)

    @redis_retry
    async def get(self, key):
        await self.redis_client.rpop(key)


class NoAsRedis:
    def __init__(self, host, port, db):
        # self.redis_client = self.redis_cli(host, port, db)
        # print(self.redis_client)
        # self.redis_client = init_redis
        self.init_redis(host, port, db)

    def init_redis(self, host, port, db):
        self.redis_client = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(host=host, port=port, db=db),
            decode_responses=True,  # 自动解码
        )

    @redis_retry
    def push(self, key: object, value: object):
        self.redis_client.lpush(key, value)

    @redis_retry
    def len(self, key):
        self.redis_client.llen(key)

    @redis_retry
    def get(self, key):
        self.redis_client.rpop(key)

    @redis_retry
    def incr(self, key):
        self.redis_client.incr(key)


def t_as():
    host = '192.168.48.129'
    port = 6379
    db = 1
    loop = asyncio.get_event_loop()
    t = AsRedis(host, port, db).push
    task = [asyncio.ensure_future(t(key='hahh', value='{"page":1, "keyword": "%s", "site":"zhilian"}' % i)) for i in
            range(100)]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()


def t_n():
    host = '192.168.170.132'
    port = 6379
    db = 2
    NoAsRedis(host, port, db).incr('dajie_208_finsh')


if __name__ == '__main__':
    for _ in range(100):
        t_n()
