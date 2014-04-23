#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.

from trytond.pool import Pool
from .task import *

def register():
    Pool.register(
        WorkType,
        Work,
        module='project_tracker', type_='model')
