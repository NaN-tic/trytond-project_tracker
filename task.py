#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval

__all__ = ['WorkType', 'Work']
__metaclass__ = PoolMeta


class WorkType(ModelSQL, ModelView):
    'Task Tracker'
    __name__ = 'project.work.tracker'

    name = fields.Char('Name', required=True, select=True)
    comment = fields.Text('comment')
    group = fields.Many2One('res.group', 'User Group')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True


class Work:
    __name__ = 'project.work'

    tracker = fields.Many2One('project.work.tracker', 'Tracker', states={
            'required': Eval('type') == 'task',
            }, depends=['type'])

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls._error_messages.update({
                'invalid_user_tracker': ('You do not have permissions for '
                    'setting tracker "%(tracker)s" on a task "%(task)s".'),
                })

    @classmethod
    def create(cls, vlist):
        res = super(Work, cls).create(vlist)
        cls.check_group(res)
        return res

    @classmethod
    def write(cls, *args):
        super(Work, cls).write(*args)
        actions = iter(args)
        all_records = []
        for records, values in zip(actions, actions):
            if 'tracker' in values:
                all_records += records
        if all_records:
            cls.check_group(all_records)

    @classmethod
    def check_group(cls, records):
        user = Transaction().user
        if not user:
            return
        for record in records:
            group = record.tracker.group if record.tracker else None
            if not group:
                continue
            if user not in [x.id for x in group.users]:
                cls.raise_user_error('invalid_user_tracker', {
                        'tracker': record.tracker.rec_name,
                        'task': record.rec_name,
                        })
