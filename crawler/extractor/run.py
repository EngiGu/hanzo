import logging
import asyncio
import os
import json
import sys

import resumes
import lists

from common import CRAWLER_MESSAGE_TYPE_MAP, update_query_dispatch_status
from dummy_interface.dummy_interface import DummyInterface
import dummy_interface.dummy_mysql as mysql
import dummy_interface.async_queue_adapter as queue
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] [%(module)s %(filename)s %(lineno)d %(funcName)s] %(message)s"
)

async def invalid_message_handler(msg, db_pool):
    print('invalid message, %s' % msg)
    await update_query_dispatch_status(db_pool, msg['url_sign'], 'parse_error')

CRAWLER_MESSAGE_DISPATCH_KEY_MAP = {
    'reversed': invalid_message_handler,
    'lists': lists.handler,
    'resumes': resumes.handler,
}
CRAWLER_MESSAGE_DISPATCH_INDEX_MAP = {
    CRAWLER_MESSAGE_TYPE_MAP[key]: handler
    for key, handler in CRAWLER_MESSAGE_DISPATCH_KEY_MAP.items()
}

BASE_DIR = os.path.dirname(__file__)
DUMMY_DATA = os.path.join(BASE_DIR, 'dummy_interface/web_crawler_queue.json')

async def main_loop():
    """
    根据`msg['type']`分发消息至对应处理函数
    """
    async with mysql.AsyncConnectionPool() as db_pool, (await queue.AsyncMqSession()) as mq:
        while True:
            tag, msg = await mq.get('web-crawler-queue')
            try:
                msg = json.loads(msg.decode('utf8'))
                logging.info('get: %s', json.dumps({
                    'query': msg['query'],
                    'url': msg['url'],
                    'url_sign': msg['url_sign'],
                }, ensure_ascii=False))
                handler = CRAWLER_MESSAGE_DISPATCH_INDEX_MAP.get(msg.get('type'), invalid_message_handler)
                await handler(msg, db_pool)
            except:
                logging.warning('nack: %s', msg, exc_info=True, stack_info=True)
                await mq.nack(tag, requeue=False)
                try:
                    if isinstance(msg, bytes):
                        msg = json.loads(msg.decode('utf8'))
                    await update_query_dispatch_status(db_pool, msg["url_sign"], "parse_error")
                except:
                    logging.error('', exc_info=True, stack_info=True)
            else:
                logging.info('ack: %s', json.dumps({
                    'query': msg['query'],
                    'url': msg['url'],
                    'url_sign': msg['url_sign'],
                }, ensure_ascii=False))
                await mq.ack(tag)
            sys.stderr.flush()


def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_loop())
    finally:
        # loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

if __name__ == '__main__':
    handle_process = []
    for i in range(1):
        p = multiprocessing.Process(target=run)
        handle_process.append(p)
    for p in handle_process:
        p.start()
    for p in handle_process:
        p.join()
