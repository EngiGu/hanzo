from collections import namedtuple

from sqlalchemy import func, sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from core.mysql import get_engine_by_name
from core.redisdb import redis_cli, aredis_cli

Context = namedtuple("HandlerContext", "current_user")  # example


class ContextMaker:
    """example：model需要的上下文，与RequertHandler解耦"""

    def __call__(self, *args, **kwargs):
        return Context(current_user=None)


class HandlerContextMaker(ContextMaker):
    """接收一个RequertHandler实例，生成用于model的上下文"""

    def __call__(self, handler):
        return Context(current_user=handler.current_user)


# default handler context for model
HandlerContext = HandlerContextMaker()


class BaseModel(object):
    """model基类，约定上下文"""

    def __init__(self, *args, context: Context = None, **kwargs):
        self.context = context
        if context and context.current_user:
            setattr(self, 'current_user', context.current_user)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear(self):
        """释放资源"""


class MysqlModel(BaseModel):
    """用于连接mysql的model"""

    def __init__(self, *args, engine='master', **kwargs):
        self.session = scoped_session(sessionmaker(
            bind=get_engine_by_name(engine),
            expire_on_commit=False,
            autocommit=True,
        ), scopefunc=lambda: self)
        super().__init__(*args, **kwargs)

    def query_one_page(self, query, page, size):
        """查询一页"""
        if size <= 0:
            return []
        offset = (page - 1) * size
        return query.offset(offset if offset > 0 else 0).limit(size if size < 100 else 100).all()

    def query_total(self, query):
        """查询总数"""
        if query._limit:
            return query.with_entities(
                sql.literal_column('1')
            ).count() or 0
        if query._group_by:
            return query.with_entities(
                sql.literal_column('1')
            ).order_by(None).count() or 0
        return self.session.execute(
            query.with_labels().statement.with_only_columns(
                [func.count(1)]
            ).order_by(None)
        ).scalar() or 0

    def clear(self):
        """释放连接"""
        self.session.remove()
        super().clear()


class RedisModel(BaseModel):
    """用于连接 redis 的 model"""

    def __init__(self, *args, **kwargs):
        self.redis_client = redis_cli()
        super().__init__(*args, **kwargs)

class ARedisModel(BaseModel):
    """用于连接 redis 的 model"""

    def __init__(self, *args, **kwargs):
        self.redis_client = aredis_cli()
        super().__init__(*args, **kwargs)


