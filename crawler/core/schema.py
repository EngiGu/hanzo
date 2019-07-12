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
from sqlalchemy.dialects.mysql import TINYINT
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


if __name__ == '__main__':
    from mysql import Session, engine

    # s = Session()
    Base.metadata.create_all(engine)  # 创建表
