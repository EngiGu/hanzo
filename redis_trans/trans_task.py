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
    from model import session_scope, KaMi

    # rds = NoAsRedis('192.168.170.132', 6379, 3)
    rds = NoAsRedis('127.0.0.1', 6379, 5)
    keys = rds.redis_client.keys()
    all_data = {k.decode(): rds.get(k) for k in keys}
    print(all_data)
    # all_data = {'20_total': '103074', '21_2019-06-06': '569', '21_2019-06-10_total': '10745', '21_2019-06-10': '3823', '20_2019-06-06': '1886', '20_2019-06-10_total': '53747', '20_2019-06-10': '37254', '20_2019-06-11': '29199', '20_2019-06-11_total': '45885', '21_total': '24121', '21_2019-06-11': '974', '21_2019-06-11_total': '9103'}

    for k, v in all_data.items():
        date = None
        site = int(k[:2])
        if site != 22:  # 只更新58外页
            continue
        if len(k) == 13:
            k = '{}_update'.format(k)
        if len(k) >= 13:
            date = k[3:13]
        with session_scope() as s:
            if s.query(KaMi).filter(KaMi.rds_key == k).all():
                s.query(KaMi).filter(KaMi.rds_key == k).update({'num': int(v), 'date': date})
            else:
                s.add(KaMi(rds_key=k, num=int(v), date=date, site=site))
