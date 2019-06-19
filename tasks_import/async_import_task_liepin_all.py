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

    file = 'liepin.txt'
    site = 'liepin'


    def company():
        with open(file, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                # tmp = line.strip().split(' ')
                # yield tmp[0] + '+' + tmp[2]
                yield line.strip()


    def gene(to_fill):
        task = {'page': 1, 'site': site, 'type': 1, 'keyword': to_fill}
        return json.dumps(task, ensure_ascii=False)


    loop = asyncio.get_event_loop()
    t = TaskModel().push
    semaphore = asyncio.Semaphore(500)
    task = [asyncio.ensure_future(t(semaphore, site, type=1, value=gene(i))) for i in company()]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()
