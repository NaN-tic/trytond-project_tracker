# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import task


def register():
    Pool.register(
        task.WorkTracker,
        task.Work,
        module='project_tracker', type_='model')
