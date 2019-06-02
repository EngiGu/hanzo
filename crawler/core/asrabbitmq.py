import json
import logging
from pprint import pprint
import asyncio
from concurrent.futures import ThreadPoolExecutor

import pika

try:
    from online_config import MQ
except:
    MQ = {
        'host': "192.168.48.129",
    }




class MqSession(object):
    def __init__(self):
        try:
            self.credentials = pika.PlainCredentials(username='admin', password='admin')
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(**MQ, credentials=self.credentials, socket_timeout=20, heartbeat=0))
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)
        except Exception as e:
            logging.warning('', exc_info=True, stack_info=True)

    def put(self, queue, body):
        try:
            self.channel.basic_publish(exchange='spider', routing_key=queue, body=body,
                                       properties=pika.BasicProperties(delivery_mode=2, ))
        except Exception as e:
            logging.warning('', exc_info=True, stack_info=True)
            return -1

    def get(self, queue):
        try:
            for method_frame, properties, body in self.channel.consume(queue):
                print(method_frame, properties, body)
                return method_frame.delivery_tag, body
        except Exception as e:
            logging.warning('', exc_info=True, stack_info=True)
            return None

    def ack(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    def nack(self, delivery_tag, multiple=False, requeue=True):
        self.channel.basic_nack(delivery_tag, multiple=multiple, requeue=requeue)

    def close(self):
        self.connection.close()


class AsyncMqSession:
    """
    This class is NOT thread-safe

    # init
    session = await AsyncMqSession()
    # get
    tag, body = await session.get('name')
    # ack
    await session.ack(tag)
    # put
    await session.put('name', 'body')
    # close
    await session.close()

    # with
    async with (await AsyncMqSession()) as session:
        await session.put('name', 'body')
    """

    def __new__(cls):
        self = super().__new__(cls)
        self.__init__()
        return self

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)  # pika is NOT thread-safe
        self.loop = asyncio.get_event_loop()
        self.session = self.loop.run_in_executor(self.executor, self._init_session)  # type: MqSession

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.close()
        except:
            logging.warning('', exc_info=True, stack_info=True)

    @staticmethod
    def _init_session():
        session = MqSession()
        return session

    async def put(self, queue, body):
        return await self.loop.run_in_executor(self.executor, self.session.put, queue, body)

    async def get(self, queue):
        return await self.loop.run_in_executor(self.executor, self.session.get, queue)

    async def ack(self, tag):
        return await self.loop.run_in_executor(self.executor, self.session.ack, tag)

    async def nack(self, tag, multiple=False, requeue=True):
        return await self.loop.run_in_executor(self.executor, self.session.nack, tag, multiple, requeue)

    async def close(self):
        await self.loop.run_in_executor(self.executor, self.session.close)


def test():
    body = '1pe0sa12'
    session = MqSession()
    print('init')
    session.put('mqmq', body)
    print('put')
    _tag, _body = session.get('mqmq')
    print('get', _body)
    session.ack(_tag)
    print('ack')
    session.close()
    print('close')


def test_async():
    async def main():
        body = '1pe0sa12'
        async with  AsyncMqSession() as session:
            await session.put('mqmq', body)
            print('put')
            _tag, _body = await session.get('mqmq')
            print('get', _body)
            await session.ack(_tag)
            print('ack')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


def clean_queue(name):
    async def main():
        async with (await AsyncMqSession()) as session:
            tag, body = await session.get(name)
            await session.ack(tag)
            print(body)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    # test()
    test_async()
    # test
    # data()
    # clean_queue('extract-result-queue')
    pass
