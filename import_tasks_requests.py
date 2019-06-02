import asyncio
import json
import random
import time

import requests

url = 'http://127.0.0.1:3333/task'
# for i in range(10000):
async def push(i):
    data = {
        'task': json.dumps({
            'page': i,
            'site': 'dajie',
            'type': 1,
            # 'type': 2,
            'keyword': 'xxxxxxxxxxxxx'
            # 'url': 'yyyyyyy'
        })
    }
    print(i)
    print(requests.post(url, data=data).content.decode())
    # print(requests.get(url).content.decode())
    # break


loop = asyncio.get_event_loop()
task = [asyncio.ensure_future(push(i)) for i in range(100)]
start = time.time()
loop.run_until_complete(asyncio.wait(task))
endtime = time.time()-start
print(endtime)
loop.close()