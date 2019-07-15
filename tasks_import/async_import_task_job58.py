import asyncio
import json
import time

import redis
import aredis

redis_pool = aredis.ConnectionPool(
    host='192.168.11.191',
    port=6380,
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
    # file = 'hr58.txt'
    site = 'job58'

    # area = [159, 160, 161, 162, 163, 165, 166, 167, 168, 169, 170, 171, 1913, 8000, 15298]
    # url = 'https://wh.58.com/yewu/pn{}/'
    url = ['https://wh.58.com/yewu/pn{}/',
           'https://wh.58.com/kefu/pn{}/',
           'https://wh.58.com/renli/pn{}/',
           'https://wh.58.com/zplvyoujiudian/pn{}/',
           'https://wh.58.com/zpjiudian/pn{}/',
           'https://wh.58.com/jiudianzp/pn{}/',
           'https://wh.58.com/chaoshishangye/pn{}/',
           'https://wh.58.com/meirongjianshen/pn{}/',
           'https://wh.58.com/zpanmo/pn{}/',
           'https://wh.58.com/zpjianshen/pn{}/',
           'https://wh.58.com/zpshengchankaifa/pn{}/',
           'https://wh.58.com/zpshengchan/pn{}/',
           'https://wh.58.com/zpqiche/pn{}/',
           'https://wh.58.com/zpfangchanjianzhu/pn{}/',
           'https://wh.58.com/zpwuye/pn{}/',
           'https://wh.58.com/zpfangchan/pn{}/',
           'https://wh.58.com/jiazhengbaojiexin/pn{}/',
           'https://wh.58.com/siji/pn{}/',
           'https://wh.58.com/zpshangwumaoyi/pn{}/',
           'https://wh.58.com/zpwuliucangchu/pn{}/',
           'https://wh.58.com/zptaobao/pn{}/',
           'https://wh.58.com/zpmeishu/pn{}/',
           'https://wh.58.com/shichang/pn{}/',
           'https://wh.58.com/zpguanggao/pn{}/',
           'https://wh.58.com/zpwentiyingshi/pn{}/',
           'https://wh.58.com/zhuanye/pn{}/',
           'https://wh.58.com/zpcaiwushenji/pn{}/',
           'https://wh.58.com/zpfalvzixun/pn{}/',
           'https://wh.58.com/fanyizhaopin/pn{}/',
           'https://wh.58.com/zpxiezuochuban/pn{}/',
           'https://wh.58.com/tech/pn{}/',
           'https://wh.58.com/zpjixieyiqi/pn{}/',
           'https://wh.58.com/zpjixie/pn{}/',
           'https://wh.58.com/jinrongtouzi/pn{}/',
           'https://wh.58.com/zpjinrongbaoxian/pn{}/',
           'https://wh.58.com/zpyiyuanyiliao/pn{}/',
           'https://wh.58.com/zpzhiyao/pn{}/',
           'https://wh.58.com/xiaofeipin/pn{}/',
           'https://wh.58.com/huanbao/pn{}/',
           'https://wh.58.com/huagonggy/pn{}/',
           'https://wh.58.com/zhikonganfang/pn{}/',
           'https://wh.58.com/zpguanli/pn{}/',
           'https://wh.58.com/nonglinmuyu/pn{}/',
           'https://wh.58.com/zhaopin/pn{}/',
           'https://wh.58.com/feiyingli/pn{}/',
           'https://wh.58.com/zhaopinhui/pn{}/',
           'https://wh.58.com/zhiyuanzhe/pn{}/',
           'https://wh.58.com/shixishengpeixundeng/pn{}/',
           'https://wh.58.com/zpzhiyepeixun/pn{}/',
           'https://wh.58.com/zpxielei/pn{}/']

    area = ['hongshan',
            'wuchang',
            'jiangan',
            'jiangxia',
            'hanyang',
            'jianghan',
            'qiaokou',
            'dongxihu',
            'huangpo',
            'whtkfq',
            # 'whqingshanqu',
            # 'caidian',
            # 'xinzhouqu', # 数量太少去掉
            # 'hannan',
            # 'wuhan'
            ]


    # area = [159]

    def gene(to_fill):
        task = {'site': site, 'type': 2, 'url': to_fill}
        return json.dumps(task, ensure_ascii=False)


    loop = asyncio.get_event_loop()
    t = TaskModel().push
    semaphore = asyncio.Semaphore(500)
    task = [asyncio.ensure_future(
        t(semaphore, site, type=2, value=gene(i.format(j).replace('https://wh.58.com', 'https://wh.58.com/' + k))))
        for i in url
        for j in range(1, 71) for k in area]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()
