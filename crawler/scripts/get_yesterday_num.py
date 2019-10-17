import time, sys, os

import requests

sys.path.append(os.path.abspath('../'))
from sqlalchemy import func
from core.schema import DailyHrCrawl, DailyJobCrawl
from core.mysql import session_scope
import datetime


def send_ftqq_msg(text, desp):
    """
    :param text: 消息标题，最长为256，必填。
    :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
    :return:
    """
    server_url = 'http://sooko.club:8888/notice'
    data = {'title': text, 'content': desp, 'way': 'SinaEmail', 'key': 'spider_c:TFvkD9enEkvkVUyMVJUYmN'}
    return requests.post(url=server_url, data=data).content.decode()


def get_yesterday_crawled_num():
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    print(yesterday)

    with session_scope() as s:
        hr58_total = s.query(func.count(DailyHrCrawl.id)).filter(
            DailyHrCrawl.created >= '%s 00:00:00' % yesterday,
            DailyHrCrawl.created <= '%s 23:59:59' % yesterday,
        ).scalar() or 0
        print('hr58_total', hr58_total)

        job58_total = s.query(func.count(DailyJobCrawl.id)).filter(
            DailyJobCrawl.created >= '%s 00:00:00' % yesterday,
            DailyJobCrawl.created <= '%s 23:59:59' % yesterday,
        ).scalar() or 0
        print('job58_total', job58_total)

        return hr58_total, job58_total, yesterday


def send():
    hr58_total, job58_total, yesterday = get_yesterday_crawled_num()
    title = '58hr: %s 58job: %s [%s]' % (hr58_total, job58_total, yesterday)
    print(send_ftqq_msg(title, title))


if __name__ == '__main__':
    # get_yesterday_crawled_num()
    send()
