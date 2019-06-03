import time

from core.base_model import ARedisModel


# TYPE1_NUM = 3


class TaskModel(ARedisModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def push(self, site, type, value):
        await self.redis_client.lpush(site + "_" + str(type), value)  # lagou_2  lagou_3 lagou_1 lagou_4

    async def len(self, key):
        return await self.redis_client.llen(key)

    async def get(self, site):
        query = [site + "_" + str(i) for i in [2, 3, 1, 4, 5]]

        for key in query:
            res = await self.redis_client.rpop(key)
            if res: return res
        return res
