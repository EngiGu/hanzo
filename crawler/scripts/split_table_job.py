from core.schema import *
from core.mysql import Session, engine, session_scope


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


class TD:

    def __init__(self):
        self.session = Session()
        pass

    def get_old_record(self, offset, limit):
        query = self.session.query(DailyHrCrawl)
        for i in query.offset(offset).limit(limit).yield_per(1000):
            print(row2dict(i))


    def run(self):
        self.get_old_record(1, 1000)
        pass


if __name__ == '__main__':
    t = TD()
    t.run()
