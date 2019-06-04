import logging  # 引入logging模块
import os
import time
from logging.handlers import TimedRotatingFileHandler
from config import ROOT_PATH

SAVE_LOG = True
LEVEL = 'INFO'

maps = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'CRITICAL': logging.CRITICAL,
}

if not SAVE_LOG:
    def Logger(set_name=None):
        logging.basicConfig(level=maps.get(LEVEL),
                            format='%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')
        logger = logging
        return logger

else:
    def Logger(set_name=None):
        format = '%(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s'
        logger = logging.getLogger("{}.log".format(set_name + str(int(time.time() * 1000))))
        format_str = logging.Formatter(format)  # 设置日志格式
        logger.setLevel(maps.get(LEVEL))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        fn = os.path.join(ROOT_PATH, "logs/{}.log".format(set_name))
        th = TimedRotatingFileHandler(filename=fn, when='midnight', backupCount=3,
                                      encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        logger.addHandler(sh)  # 把对象加到logger里
        logger.addHandler(th)
        return logger

if __name__ == '__main__':
    # logger = Logger('fsd')
    # logger.info('fasdddfa')
    # print(os.path.split(os.path.abspath(__file__))[1].split('.')[0])

    print(ROOT_PATH)
