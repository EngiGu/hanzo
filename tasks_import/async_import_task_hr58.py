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
    site = 'hr58'

    # def company():
    #     with open(file, 'r', encoding='utf-8') as f:
    #         while True:
    #             line = f.readline()
    #             if not line:
    #                 break
    #             tmp = line.strip().split(' ')
    #             yield tmp[0] + '+' + tmp[2]
    # area = [159, 160, 161, 162, 163, 165, 166, 167, 168, 169, 170, 171, 1913, 8000, 15298]
    dsid = {'13136': '餐饮', '13083': '家政保洁/安保', '13093': '美容/美发', '391123': '酒店', '38824': '旅游', '13146': '娱乐/休闲',
            '38829': '保健按摩', '38830': '运动健身', '13126': '人事/行政/后勤', '13080': '司机', '13897': '高级管理', '13139': '销售',
            '13122': '客服', '13133': '贸易/采购', '13803': '超市/百货/零售', '38665': '淘宝职位', '38823': '房产中介', '13125': '市场/媒介/公关',
            '13140': '广告/会展/咨询', '38826': '美术/设计/创意', '13137': '普工/技工', '38825': '生产管理/研发', '13134': '物流/仓储',
            '24581': '服装/纺织/食品', '24571': '质控/安防', '13145': '汽车制造/服务', '13129': '计算机/互联网/通信', '13144': '电子/电气',
            '38828': '机械/仪器仪表', '13128': '法律', '13148': '教育培训', '23197': '翻译', '13147': '编辑/出版/印刷', '13127': '财务/审计/统计',
            '23195': '金融/银行/证券/投资', '13132': '保险', '13141': '医院/医疗/护理', '38827': '制药/生物工程', '24515': '环保',
            '13135': '建筑', '38822': '物业管理', '24476': '农/林/牧/渔业', '13149': '其他职位'}


    # area = [159]

    def gene(to_fill):
        task = {'site': site, 'type': 2, 'url': to_fill}
        return json.dumps(task, ensure_ascii=False)


    loop = asyncio.get_event_loop()
    t = TaskModel().push
    semaphore = asyncio.Semaphore(500)
    task = [asyncio.ensure_future(t(semaphore, site, type=2, value=gene('{}+{}'.format(i, j)))) for i in dsid.keys() for j in
            range(1, 71)]
    start = time.time()
    loop.run_until_complete(asyncio.wait(task))
    endtime = time.time() - start
    print(endtime)
    loop.close()
