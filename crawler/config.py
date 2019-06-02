import os

ROOT_PATH = os.path.dirname(__file__)

PROXY_URL = 'http://sooko.ooo:5010/get/'
REDIS_TASK_URI = 'http://127.0.0.1:3333/task'

# MONGODB_HOST = "mongodb://aizhaopin:aizhaopin%402017@dds-2ze05f9b880291d41.mongodb.rds.aliyuncs.com:3717, dds-2ze05f9b880291d42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4570175"

SITE_SOURCE_MAP = {
    "lagou": 201,
    "job51": 205
}

# rabbitmq
RABBITMQ_HOST = '192.168.48.129'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PWD = 'admin'
RABBITMQ_EXCHANGE = 'spider'
QUEUE = 'mqmq'
