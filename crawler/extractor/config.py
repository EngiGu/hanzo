# extractor config


SITE_SOURCE_MAP = {
    "lagou": 201,
    "dajie": 208,
    # "hr58": 21,
    # "hr58n": 22,
    "juzi": 209,
    'yinguo':211,
    'job58': 23,
    'hr58':24
}


# rabbitmq
RABBITMQ_HOST = '192.168.11.191'
RABBITMQ_PORT = 5673
RABBITMQ_USER = 'guest'
RABBITMQ_PWD = 'guest'
RABBITMQ_EXCHANGE = 'spider'
QUEUE = 'tc58'
TEST_QUEUE = 'test_queue'


# task redis
REDIS_HOST = '192.168.11.191'
REDIS_PORT = 6380
REDIS_DB = 1

# count redis
C_REDIS_HOST = '192.168.11.191'
C_REDIS_PORT = 6380
C_REDIS_DB = 2

# mongo
MONGODB_HOST = "mongodb://aizhaopin:aizhaopin%402017@dds-2ze05f9b880291d41.mongodb.rds.aliyuncs.com:3717, dds-2ze05f9b880291d42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4570175"
# MONGODB_HOST = "127.0.0.1:27017"

