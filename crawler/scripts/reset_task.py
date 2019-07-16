import time, sys, os
import redis

sys.path.append(os.path.abspath('../'))
from extractor import config as ex_conf


class NoAsRedis:
    def __init__(self, host, port, db):
        self.init_redis(host, port, db)

    def init_redis(self, host, port, db):
        self.redis_client = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(host=host, port=port, db=db),
            decode_responses=True,  # 自动解码
        )

    def client(self):
        return self.redis_client


def redis_cli():
    return NoAsRedis(ex_conf.REDIS_HOST, ex_conf.C_REDIS_PORT, ex_conf.REDIS_DB).client()


def del_all_tasks():
    sites = ['hr58', 'job58']
    r_cli = redis_cli()
    all_keys = [i.decode() for i in r_cli.keys()]
    for key in all_keys:
        for site in sites:
            if key.startswith(site):
                r_cli.delete(key)  # 找到这个site开头的那就删掉
                print('has deleted {}'.format(key))


if __name__ == '__main__':
    del_all_tasks()
