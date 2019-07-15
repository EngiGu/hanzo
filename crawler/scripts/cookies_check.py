import time,sys,os

import requests
from yima_api import Yima
sys.path.append(os.path.abspath('../core'))
from core.schema import CookieStore
from core.mysql import session_scope

headers = {
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,it;q=0.8',
    'cache-control': 'no-cache',
    'cookie': 'commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; sessionid=8a9675fa-4e41-423c-bf28-96eeecbb70d3; param8616=1; param8716kop=1; id58=e87rZl0EuzCoPyC3CISqAg==; 58tj_uuid=a22f6c49-35ff-4270-bb98-d2019ec09be9; new_uv=1; utm_source=; spm=; init_refer=; jl_list_left_banner=1; als=0; wmda_uuid=b6470035d30409766e3ee91a34134b88; wmda_new_uuid=1; wmda_session_id_1731916484865=1560591154559-d9fea39d-51e4-d60a; wmda_visited_projects=%3B1731916484865; xxzl_deviceid=OaoMjiA0nALhIk8zQgyEqqC3l8WbqPO7tnnsBGKfNsq48JuDusI4uvBUV2tTaT1r; PPU="UID=63814192696597&UN=xvhjzdghyhlg&TT=7de63ccc32a8e06f75c3e53d361f507b&PBODY=RBW5dnfz1XND4QF10hm9wBOmrFc22q_0pTJ1YZOLJlFocLYgeC5QLQuPr05KE7ZzWeo58JMSzD030OzjTl62MjUvFARQi0ucSQ-Gibgnl7lWVYYSqQHG60I4BCIceOkdUZFtwP1c-hziWZ_4iJ3BqPYfu2I-T9KrpKDTC7d6qRo&VER=1"; www58com="UserID=63814192696597&UserName=xvhjzdghyhlg"; 58cooper="userid=63814192696597&username=xvhjzdghyhlg"; 58uname=xvhjzdghyhlg; new_session=0; showPTTip=1; ljrzfc=1',
    'pragma': 'no-cache',
    'referer': 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-0f7d-5880-bbccd08216eb&ClickID=104',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    # 'x-requested-with': 'XMLHttpRequest',
}


def send_ftqq_msg(text, desp):
    """
    :param text: 消息标题，最长为256，必填。
    :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
    :return:
    """
    url = 'http://sc.ftqq.com/SCU30620T7f7c14060cb17921326cbe6eb83344f25b70f4f1e24ab.send'
    content = desp + '\n\nDate:  ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    r = requests.post(url, data={'text': text, 'desp': content})
    print(r.content.decode())
    pass


class COOKIES_STATUS:
    ok = 0  # 可以用
    broken = 1  # 被封需要更换
    updating = 2  # 正在更换


def check_cookies_is_ok(cookies):
    h = headers
    h['cookie'] = cookies
    url = 'https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29'
    r = requests.get(url=url, headers=headers).content.decode()
    if '<title>用户登录-58同城</title>' in r:
        return False
    return True


def main():
    f = 0
    while True:
        with session_scope() as s:
            query = s.query(CookieStore).filter(CookieStore.status == COOKIES_STATUS.ok).all()
            if not query:
                print('暂时没有要更新的cookies')
                time.sleep(10)
                continue
            notice = ''
            for q in query:
                # print(q)
                if not check_cookies_is_ok(q.cookies):
                    notice += q.tag + ' '
                time.sleep(1.5)
            if notice:
                f += 1
                if f > 3:
                    raise SystemExit('超过推送消息限制')
                send_ftqq_msg(notice, 'cookies 过期')
        print('暂时没有要更新的cookies')
        time.sleep(10)


if __name__ == '__main__':
    main()
