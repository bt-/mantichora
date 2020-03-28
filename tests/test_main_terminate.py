# Tai Sakuma <tai.sakuma@gmail.com>
import time

import pytest

from mantichora import mantichora

##__________________________________________________________________||
def task_perpetual(ret):
    while True:
        time.sleep(0.001)
    return ret

##__________________________________________________________________||
def test_with_terminate():
    with mantichora() as mcore:
        mcore.run(task_perpetual, 'result 1')
        mcore.run(task_perpetual, 'result 2')
        mcore.run(task_perpetual, 'result 3')

        # In multiprocessing mode, since `mcore.returns()` or any
        # methods that wait for the tasks to finish are called, the
        # `with` statement will exit quickly, at which the tasks will
        # be terminated.

        # In threading mode,it will get stuck.

##__________________________________________________________________||
