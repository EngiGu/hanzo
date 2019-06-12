import os

ROOT_PATH = os.path.dirname(__file__)

PROXY_URL = 'http://10.0.0.49:5010/get/'
REDIS_TASK_URI = 'http://10.0.0.18:3333/task'

# MONGODB_HOST = "mongodb://aizhaopin:aizhaopin%402017@dds-2ze05f9b880291d41.mongodb.rds.aliyuncs.com:3717, dds-2ze05f9b880291d42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4570175"

NUM_PER_MACHINE = range(20)

# rabbitmq
RABBITMQ_HOST = '10.0.0.33'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PWD = 'admin'
RABBITMQ_EXCHANGE = 'spider'
QUEUE = 'company'
TEST_QUEUE = 'test_queue'

# it橘子账号
IT_Juzi_Accounts = ["15948430604", "13091673603", "13409737314", "13054221162", "13104090498", "13104593209", "13316487995", "15243271043"]