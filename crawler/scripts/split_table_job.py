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
        self.position_set = set()

    def get_old_record(self, offset, limit):
        return self.session.query(DailyHrCrawl).offset(offset).limit(limit).yield_per(1000)

    # @jit
    def extract_position_list(self, result_query):
        new_record = []
        for r in result_query:
            print(row2dict(r))
            positions = r.positions
            if positions:
                positions = positions.split('、')
                self.position_set.update(positions)
                for i in positions:
                    print(i)
                    new_record.append(
                        {
                            'jx_resume_id': '3133930034888820', 'position': '厨师/厨师长',
                            'positions': '厨师/厨师长',
                            'is_today_update': '1', 'status': '0', 'created': '2019-07-15 22:02:15',
                            'modified': '2019-07-15 22:02:15'
                        }
                    )

    def run(self):
        r2d = self.get_old_record(1, 1000)
        print(r2d)
        self.extract_position_list(r2d)
        pass


if __name__ == '__main__':
    t = TD()
    t.run()
