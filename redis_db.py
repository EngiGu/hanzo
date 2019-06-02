import asyncio
import time

import redis
import aredis

redis_pool = aredis.ConnectionPool(
    host='192.168.170.132',
    port=6379,
    db=1
)


def aredis_cli():
    return aredis.StrictRedis(
        connection_pool=redis_pool,
        decode_responses=True,  # 自动解码
    )


TYPE1_NUM = 3


class TaskModel():
    def __init__(self, *args, **kwargs):
        self.redis_client = aredis_cli()
        self.maps = {
            1: 'type1_%s',
            2: 'type2',
            # 3: 'type1_to_type1',
        }

    def get_slot(self):
        return int(time.time() * 1000) % 3

    async def push(self, semaphore, type, value):
        print(value)
        async with semaphore:
            if type == 1:
                await self.redis_client.lpush(self.maps[1] % self.get_slot(), value)
            else:
                await self.redis_client.lpush(self.maps.get(type), value)

    async def len(self, type):
        return await self.redis_client.llen(self.maps.get(type))

    async def get(self):
        query = [
            'type2',
            # 'type1_to_type1',
            self.maps[1] % self.get_slot()
        ]
        for _type in query:
            res = await self.redis_client.rpop(_type)
            if res: return res
        return res


if __name__ == '__main__':

    def company():
        with open('company_name.list', 'r', encoding='utf-8') as f:
            while True:
                line  =  f.readline()
                if not line:
                    break
                yield line.strip()

    loop = asyncio.get_event_loop()
    t = TaskModel().push
    semaphore = asyncio.Semaphore(500)
    task = [asyncio.ensure_future(t(semaphore, type=1, value='{"page":1, "keyword": "%s", "site":"zhilian"}' % i)) for i in company()]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()