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

    def get_position_tag_id(self, tag):
        query = self.session.query(PositionTag.id).filter(PositionTag.position == tag).first()
        if not bool(query):
            position_tag = PositionTag(position=tag)
            self.session.add(position_tag)
            self.session.commit()
            return position_tag.id
        return query.id

    @jit
    def update_position_tag(self, tag_list):
        # self.position_set.update(tag_list)
        for tag in tag_list:
            if tag not in self.position_map:
                self.position_map[tag] = self.get_position_tag_id(tag)
        return

    @jit
    def extract_position_list(self, result_query):
        new_record = []
        for r in result_query:
            # print(row2dict(r))
            positions = r.positions
            if positions:
                tag_list = positions.split('、')
                # self.position_set.update(tag_list)
                self.update_position_tag(tag_list)
                for i in tag_list:
                    print(i)
                    new_record.append(
                        {
                            'jx_resume_id': r.jx_resume_id, 'tag_id': '',
                            'is_excepted': 1 if i == r.position else 0,
                            'is_today_update': r.is_today_update, 'status': r.status, 'created': r.created,
                            'modified': r.modified, '__position__': i
                        }
                    )
        return new_record

    @jit
    def rebuild_list(self, r_list):
        tmp = []
        for i  in r_list:
            i['tag_id'] = self.position_map[i['__position__']]
            i.pop('__position__')
            tmp.append(i)
        return tmp

    def run(self):
        r2d = self.get_old_record(1, 1000)
        # print(r2d)
        r_list = self.extract_position_list(r2d)
        r_list = self.rebuild_list(r_list)
        print(r_list)
        print(self.position_map)

        pass


if __name__ == '__main__':
    t = TD()
    t.run()
