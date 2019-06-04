# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pymongo import ASCENDING
import logging
from config import MONGODB_HOST

class MongoDb():

    def __init__(self, dbs, collections):
        """初始化的时候确定数据库以及表"""
        self.conn = MongoClient(MONGODB_HOST, connect=False)    #connect to mongodb
        self.db = self.conn[dbs]  # 使用脉脉数据库
        self.collection = self.db[collections]
        self.logger = logging

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(MongoDb, cls).__new__(cls)
        return cls._instance

    def search(self, query=None, type=1, count=500):
        """查询的结果是dict生成器"""

        if type==1:
            # 只查找一个
            doc = self.collection.find_one(no_cursor_timeout = True)
            if not doc:
                self.logger.info(f"search result is None")
                return None
            self.logger.info(f"search success！")
            return doc
        else:
            array = self.collection.find(query, no_cursor_timeout = True).limit(count)
            if not array:
                self.logger.info(f"search result is None")
                return None
            self.logger.info(f"search success！")
            return array

    def insert(self, text=dict):
        """插入数据"""
        try:
            self.collection.insert(text)
            self.logger.info(f"insert success！")
        except Exception as e:
            self.logger.error(f"insert failed :{e} \n insert text is {text}")

    def update(self, query=dict, new_text=dict, multi=False):
        """更新插入的数据以及选择更新的次数"""
        if not multi:
            try:
                self.collection.update(query,{"$set":new_text}, upsert=True)
                self.logger.info(f"upload onc success！")
            except Exception as e:
                self.logger.error(f"upload onc failed:{e} \n update text is {new_text}")
        else:
            try:
                self.collection.update(query, {"$set": new_text}, upsert=True, multi=True)
                self.logger.info(f"upload multi success！")
            except Exception as e:
                self.logger.error(f"upload multi failed:{e} \n update text is {new_text}")

    def delete(self, query=dict, multi=False):
        """删除不需要的数据"""
        if multi:
            try:
                self.collection.remove(query)
                self.logger.info(f"delete one success！")
            except Exception as e:
                self.logger.error(f"upload onc failed:{e} \n delete query is {query}")
        else:
            try:
                res = self.collection.find_one_and_delete(query)
                self.logger.info(f"delete multi success！")
            except Exception as e:
                self.logger.error(f"delete multi failed:{e} \n delete query is {query}")


if __name__ == '__main__':
    import time
    m = Mongo_db("aizhaopin", "position_infos")
    # company_infos
    # position_infos
    # for i in range(10):
    # m.insert({'spider_time': 1547693690, 'original_school': 2, 'type': 2, 'company_name': '浙江泽世供应链管理有限公司', 'last_time': 1564502400, 'resume_url': 'http://xsjy.whu.edu.cn/zftal-web/zfjy!wzxx/dwzpxx_cxWzDwzpxxNry.html?dwxxid=JG0015712', 'trants_status': 0, 'reset_id': 32743190, '_id': ObjectId('5c3fee7a39cbcd3b74d6679a')})
    # m.update({"key":1},{"count":2},multi=True)
    # m.delete({}, multi=True)
    # res = m.search().sort("last_time",ASCENDING)
    res = m.search({"source":105},type=2,count=100000)
    # m.delete({"source":102}, True)
    # print(res)
    count = 0
    for i in res:
        # print(i)
        count += 1
        time.sleep(0.000001)
    print(count)
    # for i in res:
    #     print(i)
