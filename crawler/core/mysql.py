from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

engine = create_engine("mysql+pymysql://spider:huntcoder$2014@rencaiyunguanjia.rwlb.rds.aliyuncs.com:3306/liepin")
Session = sessionmaker(bind=engine)  # 没做处理的session
SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


@contextmanager
def session_scope():
    session = SessionType()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
