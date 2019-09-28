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


class DailyHrCrawlNew(Base):
    """58job每日job抓取"""
    __tablename__ = 'daily_crawl_hr_58_record'
    id = Column(Integer(), primary_key=True, autoincrement=True)

    jx_resume_id = Column(BIGINT, nullable=False)  # cookies tag 爬虫会根据这个来取出cookies
    tag_id = Column(Integer(), nullable=False)
    # position = Column(String(512), nullable=False, default='', server_default=text("''"))  # api的指定职位
    # positions = Column(String(512), nullable=False, default='', server_default=text("''"))  # 多个期望职位

    is_today_update = Column(TINYINT, nullable=False, server_default=text("0"))  # 0 不是 1 是

    status = Column(TINYINT, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class PositionTag(Base):
    """58job每日job抓取职位分类表"""
    __tablename__ = 'position_tag'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    position = Column(String(512), nullable=False)  # cookies tag 爬虫会根据这个来取出cookies

    status = Column(TINYINT, nullable=False, server_default=text("0"))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


if __name__ == '__main__':
    from mysql import Session, engine, session_scope

    # s = Session()
    # Base.metadata.create_all(engine)  # 创建表

    lod = '2019-07-15'
    to = '2019-08-13'

    with session_scope() as s:
        q = s.query(DailyHrCrawl).filter(
            DailyHrCrawl.created >= f'{lod} 00:00:00',
            DailyHrCrawl.created <= f'{lod} 23:59:59'
        ).all()
        j = 0
        for i in q:
            b = DailyHrCrawl(
                jx_resume_id=i.jx_resume_id,
                position=i.position,
                positions=i.positions,
                is_today_update=i.is_today_update,
                created=i.created.strftime('%Y-%m-%d %H:%M:%S').replace(lod, to),
            )
            j += 1
            s.add(b)
            # s.commit()
            print(j)

    # d = DailyHrCrawl(
    #     jx_resume_id=14564564564564564,
    #     position='厨师',
    #     positions='厨师、配菜',
    # )
    # with session_scope() as s:
    #     s.add(d)
