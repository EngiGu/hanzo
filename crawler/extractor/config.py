# extractor config


SITE_SOURCE_MAP = {
    "lagou": 201,
    "dajie": 208,
    "hr58": 22,
    "juzi": 209,
    'yinguo':211
}


# rabbitmq
RABBITMQ_HOST = '10.0.0.33'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PWD = 'admin'
RABBITMQ_EXCHANGE = 'spider'
QUEUE = 'company'
TEST_QUEUE = 'test_queue'


# redis
REDIS_HOST = '10.0.0.48'
REDIS_PORT = 6379
REDIS_DB = 1

# count_redis
C_REDIS_HOST = '10.0.0.48'
C_REDIS_PORT = 6379
C_REDIS_DB = 2

# mongo
MONGODB_HOST = "mongodb://aizhaopin:aizhaopin%402017@dds-2ze05f9b880291d41.mongodb.rds.aliyuncs.com:3717, dds-2ze05f9b880291d42.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4570175"

