import asyncio

import pika
from pika.exceptions import ChannelClosed, ConnectionClosed
import logging


# from tornado.options import options


class Singleton(type):
    """
    由于系统中很多地方直接使用的下面的代码发送消息
    pikachu = MqSession()
    pikachu.put(queue, json.dumps({ ... }))
    pikachu.close()
    所以每次创建连接和关闭连接，在消息比较多的时候造成挺大的内存和性能上面的开销
    考虑使用单例模式，只会有一个连接，在put消息的时候会自动重连，并且重试一次推送消息
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MqSession(object, metaclass=Singleton):

    def __init__(self, host, port, user, pwd, exchange):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.exchange = exchange
        self.connect()

    def connect(self):
        try:
            self.credentials = pika.PlainCredentials(username=self.user, password=self.pwd)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host,
                credentials=self.credentials,
                blocked_connection_timeout=2,  # 设置2秒超时，避免阻塞
                port=self.port,
                heartbeat=30  # 心跳时间
            ))
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)
        except Exception as e:
            logging.exception(e)
            return

    def _put(self, queue, body, priority=0, expiration=None):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # 2=消息持久话
                priority=priority,
                expiration=expiration and str(expiration) or None,
            ),
        )

    def put(self, queue, body, priority=0, expiration=None):
        try:
            self._put(queue, body, priority, expiration)
        except (ConnectionClosed, ChannelClosed) as e:
            logging.warning("reconnect and push msg: {} to queue: {}".format(body, queue))
            self.connection.close()
            self.connect()
            self._put(queue, body, priority, expiration)
        except Exception as e:
            logging.exception(e)
            logging.warning("push msg: {} to queue: {} failed".format(body, queue))
            return -1

    def get(self, queue):
        try:
            for method_frame, properties, body in self.channel.consume(queue):
                return method_frame.delivery_tag, body.decode('utf-8')
        except Exception as e:
            logging.exception(e)
            return None

    def ack(self, delivery_tag):
        try:
            self.channel.basic_ack(delivery_tag)
        except Exception as e:
            logging.exception(e)
            return -1

    def nack(self, delivery_tag, multiple=False, requeue=True):
        self.channel.basic_nack(delivery_tag, multiple=multiple, requeue=requeue)

    def close(self):
        # 使用单例模式之后，不用每次都创建连接，所以就不用真实的关闭连接了
        # 在程序退出的时候自动的关闭连接
        # self.connection.close()
        pass


class AsMqSession(object, metaclass=Singleton):
    # 实际上并不是真正上的异步

    def __init__(self, host, port, user, pwd, exchange):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.exchange = exchange
        self.connect()  # 链接不能异步

    def connect(self):
        try:
            self.credentials = pika.PlainCredentials(username=self.user, password=self.pwd)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host,
                credentials=self.credentials,
                blocked_connection_timeout=2,  # 设置2秒超时，避免阻塞
                port=self.port,
                heartbeat=30  # 心跳时间
            ))
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)
        except Exception as e:
            logging.exception(e)
            return

    async def _put(self, queue, body, priority=0, expiration=None):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=queue,
            body=body.encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 2=消息持久话
                priority=priority,
                expiration=expiration and str(expiration) or None,
            ),
        )

    async def put(self, queue, body, priority=0, expiration=None):
        try:
            await self._put(queue, body, priority, expiration)
        except (ConnectionClosed, ChannelClosed) as e:
            logging.warning("reconnect and push msg: {} to queue: {}".format(body, queue))
            self.connection.close()
            await self.connect()
            await self._put(queue, body, priority, expiration)
        except Exception as e:
            logging.exception(e)
            logging.warning("push msg: {} to queue: {} failed".format(body, queue))
            return -1

    async def get(self, queue):
        try:
            for method_frame, properties, body in self.channel.consume(queue):
                return method_frame.delivery_tag, body.decode('utf-8')
        except Exception as e:
            logging.exception(e)
            return None

    async def ack(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    async def nack(self, delivery_tag, multiple=False, requeue=True):
        self.channel.basic_nack(delivery_tag, multiple=multiple, requeue=requeue)

    async def close(self):
        self.connection.close()

    async def __aenter__(self):  # with
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.close()
        except:
            logging.warning('', exc_info=True, stack_info=True)


def test_mq():
    RABBITMQ_HOST = '192.168.48.129'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'admin'
    RABBITMQ_PWD = 'admin'
    RABBITMQ_EXCHANGE = 'spider'
    QUEUE = 'mqmq'

    mq = MqSession(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PWD, RABBITMQ_EXCHANGE)
    # mq.put(QUEUE, 'hello world')
    tag, msg = mq.get(QUEUE)
    print(tag, msg)
    # mq.put(QUEUE, {'faf': 6666})
    # print(mq.nack(tag))
    print(mq.ack(tag))


def test_as_mq():
    RABBITMQ_HOST = '192.168.48.129'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'admin'
    RABBITMQ_PWD = 'admin'
    RABBITMQ_EXCHANGE = 'spider'
    QUEUE = 'mqmq'

    async def main():
        body = '1pe0sa12'
        async with  AsMqSession(RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PWD,
                                RABBITMQ_EXCHANGE) as session:
            # await session.put('mqmq', body)
            # print('put')
            _tag, _body = await session.get('mqmq')
            print('get', _body)
            await session.ack(_tag)
            print('ack')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    # test_mq()
    test_as_mq()
