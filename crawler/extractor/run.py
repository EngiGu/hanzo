import logging
import asyncio
import os
import json
import sys
import multiprocessing

from handlers import handler  # 放前面先把core包环境路径加上
from core.rabbitmq import AsMqSession as AsMq
# from core.asredis import AsRedis as AsRe
from config import *

# print(QUEUE)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s'
)


async def main_loop():
    """
    rabbitmq  消息格式：Str '{"site": "cccc", "type: 1, "content": "content.....", "curr_task": "yyyyy"}'
    """
    async with AsMq(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_EXCHANGE) as mq:
        while True:
            tag, msg = await mq.get(QUEUE)
            if isinstance(msg, bytes):
                msg = msg.decode('utf8')
            msg = json.loads(msg)

            # msg['curr_task'] str
            task_summary = json.dumps({
                'site': msg['site'],
                'type': msg['type'],
                'curr_task': msg['curr_task'],
            }, ensure_ascii=False)
            # print('msg:', msg)
            print('task_summary:', task_summary)
            try:
                logging.info('get: %s', task_summary)
                await handler(msg)

            except:
                logging.info(f"error msg: {str(msg)}")
                logging.warning('nack: %s', task_summary, exc_info=True, stack_info=True)
                await mq.nack(tag, requeue=False)

            else:
                logging.info('ack: %s', task_summary)
                await mq.ack(tag)

            sys.stderr.flush()
            # sys.exit()


def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_loop())
    finally:
        # loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    handle_process = []
    for i in range(10):
        p = multiprocessing.Process(target=run)
        handle_process.append(p)
    for p in handle_process:
        p.start()
    for p in handle_process:
        p.join()
