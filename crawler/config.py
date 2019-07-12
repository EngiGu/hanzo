import os

ROOT_PATH = os.path.dirname(__file__)

# PROXY_URL = 'http://192.168.11.191:5010/get/'
PROXY_URL = 'http://sooko.ml:5010/get/'
REDIS_TASK_URI = 'http://192.168.11.191:3333/task'

# MONGODB_HOST = "mongodb://aizhaopin:aizhaopin%402017@dds-2ze05f9b880291d41.mongodb.rds.aliyuncs.com:3717, dds-2ze05f9b880291d42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4570175"

NUM_PER_MACHINE = 20

# rabbitmq
RABBITMQ_HOST = '192.168.11.191'
RABBITMQ_PORT = 5673
RABBITMQ_USER = 'guest'
RABBITMQ_PWD = 'guest'
RABBITMQ_EXCHANGE = 'spider'
QUEUE = 'tc58'
TEST_QUEUE = 'test_queue'



