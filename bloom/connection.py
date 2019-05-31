import redis

import BloomfilterOnRedis
from config import *


def bloom_filter_from_defaults(redis_url):
    _redis = redis.StrictRedis
    return _redis.from_url(redis_url)


_server = bloom_filter_from_defaults(BLOOM_REDIS_URI)
BFR = BloomfilterOnRedis.BloomFilterRedis(_server, BLOOM_KEY_NAME, BLOCK_NUM)
