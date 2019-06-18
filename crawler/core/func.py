import functools
import importlib
import inspect
import logging
import os
import socket
import time
from copy import deepcopy

import requests
from .base import Base


# from config import ROOT_PATH


def SynResolve(host):
    try:
        results = socket.getaddrinfo(host, None)
        for result in results:
            return result[4][0]
    except Exception as e:
        print(e)


def is_online_server(host):
    res = requests.get('http://pv.sohu.com/cityjson?ie=utf-8').content.decode()
    if SynResolve(host) in res:
        return True
    return False


def get_local_ip():
    local_ip = ""
    try:
        socket_objs = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ip_from_ip_port = [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in socket_objs][0][1]
        ip_from_host_name = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if
                             not ip.startswith("127.")][:1]
        local_ip = [l for l in (ip_from_ip_port, ip_from_host_name) if l][0]
    except Exception as e:
        print("get_local_ip found exception : %s" % e)
    return local_ip if ("" != local_ip and None != local_ip) else socket.gethostbyname(socket.gethostname())


def load_module(module_path, file_path, prefix):
    """
    module_path: 模块路径    foo.boo
    file_path: 导入文件的绝对路径作为基准 C:/user/a.py
    :return: 动态加载spider文件夹下的以sp_开头的模块
    """

    def get_site_name(file_name):
        """rtc_hr58.py"""
        if isinstance(file_name.split('.')[0].split('_'), str):
            return file_name.split('.')[0].split('_')[-1]
        elif isinstance(file_name.split('.')[0].split('_'), list):
            return '_'.join(file_name.split('.')[0].split('_')[1:])

    def valid(obj):
        if inspect.isclass(obj):
            if Base in obj.__bases__:
                return obj
        return False

    base_path = os.path.dirname(file_path)
    base_path = base_path.replace('\\', '/')  # windows可能一个路径中两种斜杠，统一

    module_file_path = os.path.join(base_path, os.sep.join(module_path.split('.')))
    files = [i for i in os.listdir(module_file_path) if i.startswith(prefix)]
    modules = {get_site_name(i): importlib.import_module('{}.{}'.format(module_path, i.split('.py')[0]))
               for i in files}
    spiders_dicts = {k: getattr(v, '__dict__') for k, v in modules.items()}
    return {k: i for k, v in spiders_dicts.items() for i in v.values() if valid(i)}


# def time_count(func):
#     def wrapper(*args, **kwargs):
#         logger = for
#         st = time.time()
#         res = func(*args, **kwargs)
#         logging.info(f'{func.__name__} time_count cost {(time.time() - st):.3f} s.')
#         return res
#
#     async def as_wrapper(*args, **kwargs):
#         st = time.time()
#         res = await func(*args, **kwargs)
#         logging.info(f'{func.__name__} time_count cost {(time.time() - st):.3f} s.')
#         return res
#
#     return as_wrapper if inspect.iscoroutinefunction(func) else wrapper

def mongo_time_count(log_flag):
    # log_flag 是要输出日志的标记信息，例如：position.position_name
    def _time_count(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = args[-1]
            resume = deepcopy(args[-2])
            st = time.time()
            res = func(*args, **kwargs)
            ex = time.time() - st
            for i in log_flag.split('.'):
                resume = resume.get(i, None)
                if not resume:
                    raise Exception(f'{log_flag} field error!!')
            logger.info(f'{func.__name__} mongo cost {ex:.3f} s. {log_flag}: {str(resume)}')
            return res
        return wrapper
    return _time_count


if __name__ == '__main__':
    # host = 'sooko.ml'
    # print(SynResolve(host))
    # print(is_online_server(host))
    print(get_local_ip())