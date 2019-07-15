# 58 初始获取cookies存到mysql
# 目前存在 `liepin` `cookies_store`  线上阿里云


import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

import requests
from yima_api import Yima
from core.schema import CookieStore
from core.mysql import session_scope

yima = Yima(username="fbfbfbfb", password="jianxun1302", project_id=159, project_name=u"58同城")


def check_is_exists(phone):
    headers = {
        'authority': 'passport.58.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'origin': 'https://passport.58.com',
        'upgrade-insecure-requests': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'referer': 'https://passport.58.com/login/?path=https%3A//wh.58.com/&PGTID=0d100000-0009-e96c-3106-f98464aa467e&ClickID=2',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,it;q=0.8',
        # 'cookie': 'id58=c5/njVzAJMoIAfoXA3VlAg==; 58tj_uuid=329c9551-6862-43d4-9fbe-4cd1ed969770; als=0; xxzl_deviceid=cp3Mvh7aF0HWvoYmymkjF8hlRJrKFfKVoLB%2BJeerMqgmiahmSXbkf35ND%2BYmMc9Z; wmda_uuid=57aa741ccc8947f8344a4d1bd77f9113; wmda_new_uuid=1; gr_user_id=5d8d983a-96d9-431d-b81f-185f802c5695; mcity=wh; mcityName=%E6%AD%A6%E6%B1%89; nearCity=%5B%7B%22cityName%22%3A%22%E6%AD%A6%E6%B1%89%22%2C%22city%22%3A%22wh%22%7D%5D; Hm_lvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1556098240; cookieuid1=mgjwFVzALL4ODHp9A1s4Ag==; wmda_visited_projects=%3B1731916484865%3B6333604277682%3B2286118353409%3B3381039819650%3B4200524323842%3B4785068453378%3B7790950805815; showOrder=1; 58home=wh; city=wh; __utma=253535702.405960827.1559098468.1559098468.1559098468.1; __utmz=253535702.1559098468.1.1.utmcsr=wh.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/job/; hots=%5B%7B%22d%22%3A0%2C%22s1%22%3A%22%E6%AD%A6%E6%B1%89%E4%BA%BA%E7%91%9E%E4%BA%BA%E5%8A%9B%E8%B5%84%E6%BA%90%E6%9C%8D%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%EF%BC%88%E9%A6%99%E8%8D%89%E6%8B%9B%E8%81%98%EF%BC%89%22%2C%22s2%22%3A%22%22%2C%22n%22%3A%22sou%22%7D%5D; xxzl_smartid=3ea03942f455c5e049f95aea1abd1d85; param8616=1; param8716kop=1; isSmartSortTipShowed=true; show_zcm_banner=true; sessionid=33b39c53-0fe8-499a-8259-159dd0fe2618; resumeOrder=time; finger_session=OIGeShH2-mRwPOOJEreO-bH-rrdUOuyl; lastuname=13148304735; vip=vipusertype%3D11%26vipuserpline%3D0%26v%3D1%26vipkey%3Df7d0d4d3b7564abad39591acf41cb2cc%26masteruserid%3D59352683440914; crmvip=""; dk_cookie=""; new_uv=69; utm_source=; spm=; init_refer=https%253A%252F%252Fgraph.qq.com%252Foauth2.0%252Fshow%253Fwhich%253DLogin%2526display%253Dpc%2526autoLogin%253D0%2526response_type%253Dcode%2526client_id%253D200065%2526scope%253Dget_user_info%252Cget_qq_level%252Cget_info%252Clist_album%252Cget_fanslist%2526state%253DGUl4_H0pCUn7_jxJ5tnfN-alrxS0jJzm%2526redirect_uri%253Dhttps%25253A%25252F%25252Fpassport.58.com%25252Fthd%25252Foauthlogin%25252Fpc%25252Fqzone%25253Fpath%25253Dhttps%2525253A%2525252F%2525252Fwh.58.com%2525252F%2525253Fpts%2525253D1561010802256%252526source%25253D58-default-pc; ppStore_fingerprint=860F18A32617495B64C24011EAA3E9CC3C5F76C9BF0DD291%EF%BC%BF1561011415484; new_session=0',
    }

    data = {
        # 'fingerprint': 'OIGeShH2-mRwPOOJEreO-bH-rrdUOuyl',
        'callback': 'successFun',
        'username': phone,
        'password': '6eef7d44b9a374bfde2309b96d92a8303b41671954cacf10710df52b9e7f1e19c8b843466dbfceb14244000fd46558671c93d79cbc4ee1a8435720d4104db74c772c670e8a31f300dba21475f4a5fda7e3d729102523c060c60689f2ba2690d01fcd84d478eeeb315143215f6e3a9c0c42626f1ea8f41d3db0a92714eaf19362',
        # 'token': 'GlYcinGHn_kudlcr-9g-wXoYX5l2B-Hn',
        'source': '58-default-pc',
        'path': 'https%3A%2F%2Fwh.58.com%2F%3Fpts%3D1561011755558',
        'domain': '58.com',
        # 'finger2': 'zh-CN|24|1|8|1920_1080|1920_1040|-480|1|1|1|undefined|1|unknown|Win32|unknown|3|true|false|false|false|false|0_false_false|d41d8cd98f00b204e9800998ecf8427e|dbaff747fffe0586df0c750042298498',
        'psdk-d': 'jsdk',
        'psdk-v': '1.0.0'
    }
    response = requests.post('https://passport.58.com/58/login/pc/dologin', headers=headers, data=data)
    print(response.content.decode())
    # if '该用户不存在' in response.content.decode():
    #     return False
    # return True
    return False


def get_cookies():
    option = ChromeOptions()
    # option.add_argument('-headless')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(options=option)

    driver.get('https://passport.58.com/login')
    # print(driver.current_url)
    # sys.exit()
    driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[2]/div/img')[0].click()
    driver.find_elements_by_xpath('//*[@id="phonenum"]')[0].click()

    ele = driver.find_elements_by_xpath('//*[@id="phone"]')[0]

    phonenum = yima.generate_phone()
    for _ in range(100):
        phonenum = yima.generate_phone()
        print('phone:', phonenum)
        if not check_is_exists(phonenum):
            break
        yima.release_num(phonenum)
    #
    # sys.exit()

    for character in phonenum:
        ele.send_keys(character)
        time.sleep(0.1)

    driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/span')[0].click()

    code = yima.get_message(phone=phonenum)
    ele = driver.find_elements_by_xpath('//*[@id="mobilecode"]')[0]
    for character in code:
        ele.send_keys(character)
        time.sleep(0.1)

    time.sleep(1.1)
    driver.find_elements_by_xpath('//*[@id="btn_phonenum"]')[0].click()
    time.sleep(5)
    driver.get('https://employer.58.com/resumesearch?PGTID=0d000000-0000-02bf-9f94-8c7003dc986f&ClickID=29')
    time.sleep(10)
    driver.find_elements_by_xpath('/html/body/div[6]/div[1]/div[2]')[0].click()
    time.sleep(5)
    # driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[3]/div[2]/ul/li[1]/div[1]/div[3]/p[1]/span[1]')[
    #     0].click()
    cookie_str = driver.execute_script('return document.cookie')
    cookies = driver.get_cookies()
    yima.release_num(phonenum)
    print(cookies)
    cookies = {i['name']: i['value'] for i in cookies}
    print(cookies)
    print(cookie_str)
    driver.quit()
    return cookie_str


class COOKIES_STATUS:
    ok = 0  # 可以用
    broken = 1  # 被封需要更换
    updating = 2  # 正在更换


def get_cookies_and_store_to_mysql(all_num):
    _tag = 'cookies_{}'
    for i in range(all_num):
        with session_scope() as s:
            tag = _tag.format(i)
            q = s.query(CookieStore).filter(
                CookieStore.tag == tag,
                CookieStore.status == COOKIES_STATUS.broken
            ).first()
            if not q:
                print(_tag, '没有失效')
                continue

            cookies_str = get_cookies()
            # c = CookieStore(tag=tag, cookies=cookies_str)
            # s.add(c)
            q.update({'cookies': cookies_str})
            print('完成第', i, '个，等待10s')
            time.sleep(10)


if __name__ == '__main__':
    all_num = 4
    get_cookies_and_store_to_mysql(all_num)
