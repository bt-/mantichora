# Tai Sakuma <tai.sakuma@gmail.com>
import time

import pytest

from mantichora import mantichora

##__________________________________________________________________||
def task(sleep, ret):
    time.sleep(sleep)
    return ret

##__________________________________________________________________||
def test_end():
    mcore = mantichora()
    mcore.run(task, 0.05, 'result 1')
    mcore.run(task, 0.01, 'result 2')
    mcore.run(task, 0.02, 'result 3')
    returns = mcore.returns()
    assert ['result 1', 'result 2', 'result 3'] == returns
    mcore.end()

##__________________________________________________________________||
def test_with():
    with mantichora() as mcore:
        mcore.run(task, 0.05, 'result 1')
        mcore.run(task, 0.01, 'result 2')
        mcore.run(task, 0.02, 'result 3')
        returns = mcore.returns()
        assert ['result 1', 'result 2', 'result 3'] == returns

def test_with_terminate():
    with mantichora() as mcore:
        mcore.run(task, 10, 'result 1')
        mcore.run(task, 12, 'result 2')
        mcore.run(task, 15, 'result 3')

        # Since `mcore.returns()` or any methods that wait for the
        # tasks to finish are called, the `with` statement will exit
        # quickly, at which the tasks will be terminated.

##__________________________________________________________________||
class MyException(Exception):
    pass

def test_with_raise():
    with pytest.raises(MyException):
        with mantichora() as mcore:
            mcore.run(task, 0.05, 'result 1')
            mcore.run(task, 0.01, 'result 2')
            mcore.run(task, 0.02, 'result 3')
            raise MyException

##__________________________________________________________________||
def test_receive_one():
    with mantichora() as mcore:
        runids = [
            mcore.run(task, 0.05, 'result 1'),
            mcore.run(task, 0.01, 'result 2'),
            mcore.run(task, 0.02, 'result 3'),
        ]
        pairs = [ ]
        while True:
            p = mcore.receive_one()
            if p is None:
                break
            pairs.append(p)
    expected = [
        (runids[0], 'result 1'),
        (runids[1], 'result 2'),
        (runids[2], 'result 3'),
    ]
    assert sorted(expected) == sorted(pairs)

##__________________________________________________________________||
## what to test
## - atpbar

##__________________________________________________________________||
