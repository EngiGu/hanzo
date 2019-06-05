import datetime

import redis
from flask import Flask, render_template, jsonify

#
#
#
#
#
SITE_SOURCE_MAP = {
    "lagou": 201,
    "dajie": 208
}


#
#
#
#
#
#
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


def gene_query_maps(source):
    day_list = []
    for i in range(7):
        day = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        day_list.append('{}_{}'.format(source, day))
    day_list.append('{}_total'.format(source))
    return day_list


def gene_task_maps(source):
    task_list = []
    for i in range(1, 6):
        task_list.append('{}_{}'.format(source, i))
    return task_list


app = Flask(__name__)
r = NoAsRedis('s19.natfrp.org', 30694, 2)
t = NoAsRedis('s19.natfrp.org', 30694, 1)


@app.route('/')
def index():
    return 'WELCOME TO WORLD! <br />Usage: /status &nbsp;&nbsp;&nbsp; /task'


@app.route('/status', methods=['get'])
def query_info():
    all_res = {}
    for k, v in SITE_SOURCE_MAP.items():
        query_list = gene_query_maps(v)
        query_res = {i.replace('{}_'.format(v), ''): r.get(i) for i in query_list}
        all_res[k] = query_res
    return jsonify({'error': 0, 'msg': 'succ', 'data': all_res})


@app.route('/task', methods=['get'])
def query_task():
    all_res = {}
    desc = {
        1: 'import task',
        2: 'parse to type2',
        3: 'parse to type1',
        4: 'parse type1 error',
        5: 'parse type2 error'
    }
    for k, v in SITE_SOURCE_MAP.items():
        query_list = gene_task_maps(k)
        query_res = {i.replace('{}_'.format(k), ''): t.len(i) for i in query_list}
        all_res[k] = query_res
    return jsonify({'error': 0, 'msg': 'succ', 'data': all_res, 'desc': desc})


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=2333)


if __name__ == '__main__':
    run()
