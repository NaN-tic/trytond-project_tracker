#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['WorkType', 'Work']
__metaclass__ = PoolMeta


class WorkType(ModelSQL, ModelView):
    'Task Tracker'
    __name__ = 'project.work.tracker'

    name = fields.Char('Name', required=True, select=True)
    comment = fields.Text('comment')


class Work:
    __name__ = 'project.work'

    tracker = fields.Many2One('project.work.tracker', 'Tracker',
        depends=['type'])
