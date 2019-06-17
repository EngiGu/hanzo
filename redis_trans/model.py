import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_ , distinct
from contextlib import contextmanager
# from core.func import is_online_server

Base = declarative_base()


class KaMi(Base):  # 必须继承declaraive_base得到的那个基类
    __tablename__ = "data58"  # 必须要有__tablename__来指出这个类对应什么表，这个表可以暂时在库中不存在，SQLAlchemy会帮我们创建这个表
    id = Column(Integer, primary_key=True, autoincrement=True)  # Column类创建一个字段
    rds_key = Column(VARCHAR(255))  # nullable就是决定是否not null，unique就是决定是否unique。。这里假定没人重名，设置index可以让系统自动根据这个字段为基础建立索引
    num = Column(Integer)
    date = Column(DATETIME)
    site = Column(Integer)


# engine = create_engine("mysql+pymysql://root:Gq19940507+****+@sooko.ml:3306/other")
engine = create_engine("mysql+pymysql://spider:huntcoder$2014@rencaiyunguanjia.rwlb.rds.aliyuncs.com:3306/liepin")


session = sessionmaker(bind=engine)



SessionType = scoped_session(sessionmaker(bind=engine,expire_on_commit=False))
def GetSession():
    return SessionType()

from contextlib import contextmanager
@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# # k = KaMi(order_no='fafdasfas',order_info='xxxxxxxxxxxxx',money='0.011', date=datetime.datetime.now(), kami='kkkkk', url='http://', key='123')
# s = session()
# # print(1 in [i.id for i in s.query(KaMi.id).all()])
# query = s.query(KaMi.key).group_by(KaMi.key).all()
# print(len(query))
# for i in query:
#     print(i.key)
# print(query)
# print(query.id)
# # a= s.execute(
#             query.with_labels().statement.with_only_columns([func.count(1)])
#         ).scalar()
# print(a)
# for i in s.query(KaMi.id).all():
#     print(i.id)
    # print(i.order_no)
    # print(i.kami)
    # print(i.date)
    # print('*'*50)
# print(s.add(k))
# print(s.commit())
