# -*- coding: utf-8 -*-
import hashlib
import json
import time
import pika
import datetime

"""
设置为web_crawl格式：
{   "content": "content",
    "crawl_user_info": "{\"account\": {\"username\": \"13206842776\", \"member\": \"\"}, \"status\": 0, \"identifier\": \"RTC_zhipin_-601\"}", 
    "error_code": 0, 
    "key_info": "{\"profile\": \"\", \"experience\": \"\", \"hashed_key\": 13837894104354789704}",   # 给爬虫去重的
    "query": "{\"site\": \"zhipin\", \"page\": 4, \"keyword\": \"技术经理\", \"_resume\": {}}", 
    "query_sign": 14068236519886200684,   # todo 需要计算 
    "site": "liepin", 
    "subscribe_id": 392, 
    "subscribe_info": "{\"job_description\": {\"name\": \"大数据1\", \"welfare\": [], \"category\": null, \"level\": null, \"salary\": {\"max\": 30000, \"min\": 10000}, \"location\": \"北京\"}, \"job_preference\": {\"product\": null, \"manage_experience\": false, \"school\": {\"special\": [], \"type\": [\"不限\"]}, \"keyword\": [], \"company\": {\"special\": [], \"type\": [\"不限\"]}}, \"exclude\": [], \"threshold\": 99.0, \"job_requirement\": {\"age\": {\"max\": null, \"min\": null}, \"sex\": null, \"skill\": [\"hive\", \"elasticsearch\"], \"requirement_detail\": null, \"education\": \"大专及以上\", \"work_experience\": {\"max\": 8, \"min\": 1}, \"area\": [{\"area_name\": \"数据\", \"year\": \"\"}]}}", 
    "type": 2, 
    "url": "https://mapp-leiting.liepin.com/resume/detail/?res_id_encode=a23sd234877565", 
    "url_sign": 14946429529812689985,   # todo 需要计算
    "user_id": -601
}
"""
COUNT = 0 
DATE = datetime.datetime.now().strftime('%Y-%m-%d')
def push_to_webcrawl(res_dict):
    """入口函数"""
    mq = rabbitmq_init  # 获取mq对象
    # with open(file_name, mode='r', encoding='utf-8') as f:
    while True:
        res = str(res_dict)
        if not res_dict:
            break
        global COUNT
        COUNT += 1
        new_web_crawl = {}  # 定义一个新的字典
        res_json = res_dict  # 解析之后的简历
        try:
            key_word = str(res_json["last_job_experience"]["position"])
        except:
            key_word = ""
        jx_resume_id = res_json["jx_resume_id"]
        url = "https://mapp-leiting.liepin.com/resume/detail/?res_id_encode={}".format(jx_resume_id)
        print(url)
        # todo 计算query哈希值
        query_sign = get_hashkey(res)
        # todo 计算哈希值
        url_sign = get_hashkey(url)
        # 开始重组
        new_web_crawl["content"] = json.dumps(res_dict)  # 文本格式
        new_web_crawl["crawl_user_info"] = "{\"account\": {\"username\": \"\", \"member\": \"\"}, \"status\": 0, \"identifier\": \"RTC_liepin_-610\"}"  # 文本格式
        new_web_crawl["error_code"] = 0  # 文本格式
        new_web_crawl["key_info"] = "{\"profile\": \"\", \"experience\": \"\", \"hashed_key\": %s}" % jx_resume_id  # 文本格式
        new_web_crawl["query"] = "{\"site\": \"zhipin\", \"page\": 4, \"keyword\": \"%s\", \"_resume\": {}}" % key_word  # 文本格式
        new_web_crawl["query_sign"] = query_sign  # 文本格式
        new_web_crawl["site"] = "liepin"  # 文本格式
        new_web_crawl["subscribe_id"] = 392  # 文本格式
        new_web_crawl["subscribe_info"] = "{\"job_description\": {\"name\": \"大数据1\", \"welfare\": [], \"category\": null, \"level\": null, \"salary\": {\"max\": 30000, \"min\": 10000}, \"location\": \"北京\"}, \"job_preference\": {\"product\": null, \"manage_experience\": false, \"school\": {\"special\": [], \"type\": [\"不限\"]}, \"keyword\": [], \"company\": {\"special\": [], \"type\": [\"不限\"]}}, \"exclude\": [], \"threshold\": 99.0, \"job_requirement\": {\"age\": {\"max\": null, \"min\": null}, \"sex\": null, \"skill\": [\"hive\", \"elasticsearch\"], \"requirement_detail\": null, \"education\": \"大专及以上\", \"work_experience\": {\"max\": 8, \"min\": 1}, \"area\": [{\"area_name\": \"数据\", \"year\": \"\"}]}}"  # 文本格式
        new_web_crawl["type"] = 2  # 文本格式
        new_web_crawl["url"] = url  # 文本格式
        new_web_crawl["url_sign"] = url_sign  # 文本格式
        new_web_crawl["user_id"] = -610  # 文本格式
        # todo 开始写入到新的文件---准备发送给mq
        msg_str = json.dumps(new_web_crawl, ensure_ascii=False)
        time.sleep(0.1)
        if publish(mq, msg_str):
            print("上传jx_resume_id:{}成功".format(jx_resume_id))
            break
        time.sleep(0.1)

def get_hashkey(resume):
    """计算哈希key"""

    hashed_key = hashlib.md5(json.dumps(resume, sort_keys=True, ensure_ascii=False).encode('utf8')).hexdigest()[8:-8]
    hashed_id = int(hashed_key, 16)
    return hashed_id


def rabbitmq_init():
    """实例化rebbit_mq"""

    rabbitmq_cfg = {
        "username": "spider",
        "password": "spider",
        "host": "47.93.240.129",
        "port": 6672
    }
    username = rabbitmq_cfg['username']
    password = rabbitmq_cfg['password']
    host = rabbitmq_cfg['host']
    port = rabbitmq_cfg['port']
    heartbeat_interval = 60

    credentials = pika.PlainCredentials(username=username, password=password)  # 主动连接mq
    tries = 0
    max_tries = 3
    while tries < max_tries:
        tries += 1
        try:
            # Establish connection
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=port,
                    credentials=credentials,
                    heartbeat_interval=heartbeat_interval or 200
                )
            )
            # Create a channel
            channel = connection.channel()
            print("连接mq成功")
            return channel
        except :
            time.sleep(5)
            continue

def publish(handle, msg: str) -> bool:
    """上传到web-crawl-queue"""

    exchange = "spider"
    routing_key = "web-crawler-queue"

    msg_type = type(msg)
    if not isinstance(msg, str):
        print(f'msg is not str. type: {msg_type}')
    if not msg:
        print(f'msg is negative. _{msg}_, type: {msg_type}')
    msg_len = len(msg)

    print('Publish a msg')

    tries = 0
    max_tries = 3
    while tries < max_tries:
        tries += 1
        try:
            a = time.time()
            # self.channel.basic_publish("spider", "web_crawl_queue", msg)
            handle.basic_publish(exchange, routing_key, msg)
            print(f'Published a msg (len: {msg_len:,d})')
            return True
        except:
            print(f'{tries}/{max_tries} RabbitMQ Connection Closed, re-connect')
            handle = rabbitmq_init()  # todo rebbitmq的操作对象
            continue
    print(f'{tries}/{max_tries} Exceed max tries, failed')


if __name__ == '__main__':

    # file_name = "out_file_2_{}.json".format(DATE)
    # file_name3 = "out_file_3_{}.json".format(DATE)
    # file_name2 = "out_file_{}.json".format(DATE)
    # read_file_to_webcrawl(file_name)
    # read_file_to_webcrawl(file_name2)
    # read_file_to_webcrawl(file_name3)
    # print("今天是：{}---成功插入：{}条数据".format(DATE, COUNT))
    pass
