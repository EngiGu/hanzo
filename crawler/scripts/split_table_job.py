from core.schema import *
from core.mysql import Session, engine, session_scope


class TD:

    def __init__(self):

        pass

    def get_old_record(self, offset, limit):
        query.offset(offset).limit(limit).yield_per(1000)

    def trans(self):
        pass


if __name__ == '__main__':
