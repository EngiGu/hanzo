import redis


class NoAsRedis:
    def __init__(self, host, port, db):
        self.init_redis(host, port, db)

    def init_redis(self, host, port, db):
        self.redis_client = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(host=host, port=port, db=db),
            decode_responses=True,  # 自动解码
        )

    def len(self, key):
        res = self.redis_client.llen(key)
        if not res:
            return 0
        return res

    def get(self, key):
        res = self.redis_client.get(key)
        if res is None:
            return None
        return res.decode()

    def client(self):
        return self.redis_client


if __name__ == '__main__':
    # from model import session_scope, KaMi
    import os

    # rds = NoAsRedis('192.168.170.132', 6379, 1)
    rds = NoAsRedis('10.0.0.48', 6379, 1)
    keys = rds.redis_client.keys()
    # print(keys)
    keys = [i.decode() for i in keys]
    print(keys)

    for i in keys:
        if i.startswith('hr58n'):
            rds.redis_client.delete(i)
            print('has deleted: %s' % i)


    # 导入新脚本
    os.system('python3.6 async_import_task_hr58n.py')