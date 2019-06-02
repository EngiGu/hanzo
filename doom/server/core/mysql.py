from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


mysql_options = {
    'pool_size': 64,
    'pool_recycle': 3599,
    'echo': 0 and options.DEBUG,
    'max_overflow': 0,
}

engines = {}


def get_engine_by_name(name):
    if name not in engines:
        engines[name] = create_engine(options.MYSQL[name], **mysql_options)
    return engines.get(name)


# TODO 根据自己需要在这个地方配置不同的Session
Session = sessionmaker(bind=get_engine_by_name('master'))



