from sqlalchemy import (
    Column,
    TIMESTAMP,
    Integer,
    String,
    text,
    BINARY,
    DATE
)
from sqlalchemy.dialects.mysql import FLOAT
# from sqlalchemy import select, func, and_, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CookieStore(Base):
    """58cookies存储表"""
    __tablename__ = 'cookies_store'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    tag = Column(String(64), nullable=False, server_default=text("''"))  # cookies tag 爬虫会根据这个来取出cookies
    cookies = Column(String(8192), nullable=False, default='', server_default=text("''"))

    status = Column(TINYINT, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class DailyJobCrawl(Base):
    """58job每日job抓取"""
    __tablename__ = 'daily_crawl_job_58'
    id = Column(Integer(), primary_key=True, autoincrement=True)

    jx_resume_id = Column(BIGINT, nullable=False)  # cookies tag 爬虫会根据这个来取出cookies
    position = Column(String(512), nullable=False, default='', server_default=text("''"))
    is_today_update = Column(TINYINT, nullable=False, server_default=text("0"))  # 0 不是 1 是

    status = Column(TINYINT, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class DailyHrCrawl(Base):
    """58job每日job抓取"""
    __tablename__ = 'daily_crawl_hr_58'
    id = Column(Integer(), primary_key=True, autoincrement=True)

    jx_resume_id = Column(BIGINT, nullable=False)  # cookies tag 爬虫会根据这个来取出cookies
    position = Column(String(512), nullable=False, default='', server_default=text("''"))  # api的指定职位
    positions = Column(String(512), nullable=False, default='', server_default=text("''"))  # 多个期望职位
    is_today_update = Column(TINYINT, nullable=False, server_default=text("0"))  # 0 不是 1 是

    status = Column(TINYINT, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


if __name__ == '__main__':
    from mysql import Session, engine, session_scope

    s = Session()
    Base.metadata.create_all(engine)  # 创建表
    # d = DailyHrCrawl(
    #     jx_resume_id=14564564564564564,
    #     position='厨师',
    #     positions='厨师、配菜',
    # )
    # with session_scope() as s:
    #     s.add(d)
