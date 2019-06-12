import datetime

import redis
from flask import Flask, render_template, jsonify
import json
#
#
#
#
#
SITE_SOURCE_MAP = {
    "lagou": 201,
    "dajie": 208,
    "yinguo": 211,
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
    data = all_res
    site_list = [k for k,v in data.items()]  # site ["lagou", "dajie"]
    datatime = all_res.get(site_list[0])
    datatime_list = [k for k,v in datatime.items()]
    datatime_list.pop()  #  ["2019-06-05"......]

    datas = {}
    for site in site_list:
        datas[site] = []
        for d in datatime_list:
            if data[site][d]:
                datas[site].append(data[site][d])
            else:
                datas[site].append(0)
        # 追加total
        datas[site].append(data[site]["total"])

    tasks = query_task()

    res = {"data": datas,  # {"lagou": [1,2,3,4,5,6,7], "dajie": [1,2,3,4,5,6,7]}
           "datatime_list": datatime_list,
           "tasks": tasks}
    return render_template('show.html', res=res)


def query_task():
    all_res = {}
    desc = {
        1: 'import task',  # 导入
        2: 'parse to type2',  # 详情
        3: 'parse to type1',  # list翻页
        4: 'parse type1 error',  # list错误
        5: 'parse type2 error'  # resume错误
    }
    for k, v in SITE_SOURCE_MAP.items():
        query_list = gene_task_maps(k)
        query_res = {i.replace('{}_'.format(k), ''): t.len(i) for i in query_list}
        all_res[k] = query_res
    new_res = {}
    for site, v in all_res.items():
        new_res[site] = []
        for i in ["1","2","3","4","5"]:
            new_res[site].append(v[i])
    return new_res


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=2333)


if __name__ == '__main__':
    run()
