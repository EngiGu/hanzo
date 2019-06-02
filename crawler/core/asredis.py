import asyncio
import time
import aredis

class AsRedis:
    def __init__(self, host, port, db):
        self.redis_client = self.aredis_cli(host, port, db)
        print(self.redis_client)

    def aredis_cli(self, host, port, db):
        return aredis.StrictRedis(
            connection_pool=aredis.ConnectionPool(host=host, port=port, db=db),
            decode_responses=True,  # 自动解码
        )

    async def push(self, key: object, value: object) -> object:
        await self.redis_client.lpush(key, value)


    async def len(self, key):
        return await self.redis_client.llen(key)

    async def get(self, key):
        await self.redis_client.rpop(key)


if __name__ == '__main__':
    host='192.168.48.129'
    port=6379
    db=1
    loop = asyncio.get_event_loop()
    t = AsRedis(host, port, db).push
    task = [asyncio.ensure_future(t(key='hahh', value='{"page":1, "keyword": "%s", "site":"zhilian"}' % i)) for i in
            range(100)]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()
