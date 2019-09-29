import time, sys, os

sys.path.append(os.path.abspath('../'))
from core.schema import *
from core.mysql import Session, engine, session_scope
from numba import jit
from sqlalchemy import func


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

    def get_old_record(self, day):
        # return self.session.query(DailyHrCrawl).offset(offset).limit(limit).yield_per(1000)
        total = self.session.query(func.count(DailyHrCrawl.id)).filter(
            DailyHrCrawl.created >= '{} 00:00:00'.format(day),
            DailyHrCrawl.created <= '{} 23:59:59'.format(day),
        ).scalar()
        return total
        # print(total)
        # raise SystemExit
        return self.session.query(DailyHrCrawl).filter(
            DailyHrCrawl.created >= '{} 00:00:00'.format(day),
            DailyHrCrawl.created <= '{} 23:59:59'.format(day),
        ).offset(0).limit(total).yield_per(1000)

    def get_position_tag_id(self, tag):
        query = self.session.query(PositionTag.id).filter(PositionTag.position == tag).first()
        if not bool(query):
            position_tag = PositionTag(position=tag)
            self.session.add(position_tag)
            self.session.commit()
            return position_tag.id
        return query.id

    # @jit
    def save_crawled_record(self, r_list):
        all_to_insert = len(r_list)
        step = 2000
        for i in range(0, all_to_insert, step):
            print('saving', i, i + step, 'all:', all_to_insert)
            self.session.bulk_insert_mappings(DailyHrCrawlNew, r_list[i:i + step])
            self.session.commit()

    # @jit
    def update_position_tag(self, tag_list):
        # self.position_set.update(tag_list)
        for tag in tag_list:
            if tag not in self.position_map:
                self.position_map[tag] = self.get_position_tag_id(tag)
        return

    # @jit
    def extract_position_list(self, result_query):
        new_record = []
        for r in result_query:
            # print(row2dict(r))
            positions = r.positions
            # if positions:
            tag_list = positions.split('、')
            # self.position_set.update(tag_list)
            # print(tag_list)
            self.update_position_tag(tag_list)
            for i in tag_list:
                # print(i)
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
        for i in r_list:
            i['tag_id'] = self.position_map[i['__position__']]
            i.pop('__position__')
            tmp.append(i)
        return tmp

    def run(self):
        # 获取旧的简历
        days = [
            '2019-09-19',
            '2019-09-20',
            '2019-09-21',
            '2019-09-22',
            '2019-09-23',
            '2019-09-24',
            '2019-09-25',
            '2019-09-26',
            # '2019-09-27'
        ]
        days = ['2019-09-28']
        for day in days:
            to_total = self.get_old_record(day)
            # print(r2d)
            steps = 5000
            for i in range(0, to_total, steps):
                print(day, to_total, i, i + steps)
                r2d = self.session.query(DailyHrCrawl).filter(
                    DailyHrCrawl.created >= '{} 00:00:00'.format(day),
                    DailyHrCrawl.created <= '{} 23:59:59'.format(day),
                    # ).offset(i).limit(steps).yield_per(1000)
                ).offset(i).limit(steps)
                # 拆分处理
                r_list = self.extract_position_list(r2d)
                r_list = self.rebuild_list(r_list)

                # print(r_list)
                # print(self.position_map)
                # 插入新的数据表
                self.save_crawled_record(r_list)


if __name__ == '__main__':
    # all day
    """
    2019-07-15
2019-07-16
2019-07-17
2019-07-18
2019-07-19
2019-07-20
2019-07-21
2019-08-03
2019-08-04
2019-08-05
2019-08-06
2019-08-09
2019-08-14
2019-08-15
2019-08-16
2019-08-17
2019-08-18
2019-08-19
2019-08-20
2019-08-21
2019-08-22
2019-08-23
2019-08-24
2019-08-25
2019-08-26
2019-08-27
2019-08-28
2019-08-29
2019-09-19
2019-09-20
2019-09-21
2019-09-22
2019-09-23
2019-09-24
2019-09-25
2019-09-26
2019-09-27
    """
    t = TD()
    t.run()
