import hashlib
from .config import BIT_SIZE


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilterRedis(object):
    def __init__(self, server, key, blockNum=1):
        self.bit_size = BIT_SIZE  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        # self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = [SimpleHash(self.bit_size, seed) for seed in self.seeds]

    def is_exists(self, raw):
        flag = True  # 默认存在
        value = hashlib.md5(raw.encode()).hexdigest()[8:-8]
        block_No = int(value, 16) % self.blockNum  # partition block
        name = self.key % {'no': block_No}  # redis key name
        for hash_func in self.hashfunc:
            loc = hash_func.hash(value)
            if self.server.getbit(name, loc) == 0:
                self.server.setbit(name, loc, 1)
                flag = False
        return flag

    # 效率没有上面高
    # def is_exists(self, spider_name, request_fp):
    #     ret = True
    #     block_No = str(int(request_fp[0:2], 16) % self.blockNum)  # partition block
    #     name = self.key % {'spider_name': spider_name, 'no': block_No}  # redis key name
    #     for f in self.hashfunc:
    #         loc = f.hash(request_fp)
    #         ret = ret & self.server.getbit(name, loc)
    #     return bool(ret)   # 全是 1 返回 True，存在
    #
    # def insert(self, spider_name, request_fp):
    #     block_No = str(int(request_fp[0:2], 16) % self.blockNum)  # partition block
    #     name = self.key % {'spider_name': spider_name, 'no': block_No}  # redis key name
    #     for f in self.hashfunc:
    #         loc = f.hash(request_fp)
    #         self.server.setbit(name, loc, 1)


if __name__ == '__main__':
    from connection import BFR as bfr
    print(bfr.is_exists('123456'))