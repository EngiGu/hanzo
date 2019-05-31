import importlib
import inspect
import os
import socket
import requests
from spiders.base import Base
from config import ROOT_PATH


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


def load_module(module_path, prefix):
    """
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

    module_name = '.'.join(module_path.split(os.sep)[len(ROOT_PATH.split(os.sep)):]) # 模块目录
    files = [i for i in os.listdir(module_path) if i.startswith(prefix)]
    modules = {get_site_name(i): importlib.import_module('{}.{}'.format(module_name, i.split('.py')[0]))
               for i in files}
    spiders_dicts = {k: getattr(v, '__dict__') for k, v in modules.items()}
    return {k: i for k, v in spiders_dicts.items() for i in v.values() if valid(i)}



if __name__ == '__main__':
    host = 'sooko.ml'
    print(SynResolve(host))
    print(is_online_server(host))
