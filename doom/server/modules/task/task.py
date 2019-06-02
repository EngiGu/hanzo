import json
import logging
from core.base_handler import BaseHandler, arguments
from .model import TaskModel
from core.exception import ParametersError

maps = {
    1: 'import task',
    2: 'parse to type2',
    3: 'parse to type1',
    4: 'parse type1 error',
    5: 'parse type2 error'
}

class TaskHandler(BaseHandler):
    @arguments
    async def get(self, site: str = None, model: TaskModel = None):
        # http://127.0.0.1:3333/task?site=dajie
        if not site:
            self.finish({
                'code': -3,
                'msg': 'success',
                'task': 'no site received',
            })
            return

        res = await model.get(site)
        logging.info('get %r task: %r' % (site, res))

        if not res:
            self.finish({
                'code': -2,
                'msg': 'success',
                'task': 'task none',
            })
            return

        self.finish({
            'code': 0,
            'msg': 'success',
            'task': str(res.decode()),
        })

    @arguments
    async def post(self, task: str = None, model: TaskModel = None):
        # http://127.0.0.1:3333/task
        # body={'site': 'dajie', 'task': 'task', 'type': 1}
        if not task:
            raise ParametersError('task none.')
        _task = json.loads(task)
        site = _task.get('site', None)
        if not site:
            raise ParametersError('site none.')
        type = _task.get('type', None)
        if not type:
            raise ParametersError('type none.')
        if type not in [1, 2, 3, 4, 5]:  # 1：导入的任务 2: 解析的type2 3：解析的type1 4：失败的type1 5：失败的type2
            raise ParametersError('type: {} error.'.format(type))
        logging.info('push site: %r, type: %r, reason: %r, task: %r' % (site, type, maps.get(type),task))

        await model.push(site, type, task)
        self.finish({
            'code': 0,
            'msg': 'success'
        })
