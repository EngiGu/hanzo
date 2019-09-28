from core.schema import *
from core.mysql import Session, engine, session_scope
from numba import jit


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


class TD:

    def __init__(self):
        self.session = Session()
        self.position_map = {}

    def get_old_record(self, offset, limit):
        query = self.session.query(DailyHrCrawl)
        for i in query.offset(offset).limit(limit).yield_per(1000):
            r2d = row2dict(i)
            return r2d

    # @jit
    def extract_position_list(self, result_dict):
        position_set = set()
        new_record = []
        for r in result_dict:
            positions = r['positions']
            if positions:
                positions = positions.split('、')
                position_set.update(positions)
                for i in positions:
                    new_record.append(
                        {'jx_resume_id': '3133930034888820', 'position': '厨师/厨师长',
                         'positions': '厨师/厨师长',
                         'is_today_update': '1', 'status': '0', 'created': '2019-07-15 22:02:15',
                         'modified': '2019-07-15 22:02:15'
                         }
                    )

    def run(self):
        r2d = self.get_old_record(1, 1000)

        pass


if __name__ == '__main__':
    t = TD()
    t.run()
