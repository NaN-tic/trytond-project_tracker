#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['WorkTracker', 'Work']


class WorkTracker(ModelSQL, ModelView):
    'Task Tracker'
    __name__ = 'project.work.tracker'

    name = fields.Char('Name', required=True, translate=True, select=True)
    comment = fields.Text('comment')
    group = fields.Many2One('res.group', 'User Group')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    tracker = fields.Many2One('project.work.tracker', 'Tracker', states={
            'required': Eval('type') == 'task',
            }, depends=['type'])

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
                raise UserError(gettext('project_tracker.invalid_user_tracker',
                        tracker=record.tracker.rec_name,
                        task=record.rec_name))
