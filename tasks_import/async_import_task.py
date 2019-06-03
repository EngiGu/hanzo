import asyncio
import json
import time

import redis
import aredis

redis_pool = aredis.ConnectionPool(
    host='10.0.0.48',
    port=6379,
    db=1
)

def aredis_cli():
    return aredis.StrictRedis(
        connection_pool=redis_pool,
        decode_responses=True,  # 自动解码
    )

class TaskModel():
    def __init__(self, *args, **kwargs):
        self.redis_client = aredis_cli()

    async def push(self, semaphore, site, type, value):
        async with semaphore:
            await self.redis_client.lpush('{}_{}'.format(site, type), value)


if __name__ == '__main__':

    file = 'key_dajie.list'
    site = 'dajie'


    def company():

        city_code = range(1, 359)
        finance_status = range(1, 9)
        industry_status = [24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 38, 41, 43, 45, 47, 48, 49] + list(
            range(15793, 15804))
        scale_status = range(1, 7)

        for city in city_code:
            for finance in finance_status:
                for industry in industry_status:
                    for scale in scale_status:
                        key_word = "{}-{}-{}-{}".format(city, finance, industry, scale)
                        yield key_word

    def gene(to_fill):
        task = {'page': 1, 'site': 'lagou', 'type': 1, 'keyword': to_fill}
        return json.dumps(task, ensure_ascii=False)


    loop = asyncio.get_event_loop()
    t = TaskModel().push
    semaphore = asyncio.Semaphore(500)
    task = [asyncio.ensure_future(t(semaphore, site ,type=1, value=gene(i))) for i in company()]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()
