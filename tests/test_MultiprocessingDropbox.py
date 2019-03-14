# Tai Sakuma <tai.sakuma@gmail.com>
import time
import functools

import pytest

from mantichora.hub import MultiprocessingDropbox

##__________________________________________________________________||
def test_init_raise():
    with pytest.raises(ValueError):
        MultiprocessingDropbox(nprocesses=0)

def test_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.close()

def test_open_open_close():
    obj = MultiprocessingDropbox()
    obj.open()
    obj.open() # don't create workers again
    obj.close()

def test_repr():
    obj = MultiprocessingDropbox()
    repr(obj)

##__________________________________________________________________||
def task(sleep, ret):
    time.sleep(sleep)
    return ret

##__________________________________________________________________||
@pytest.fixture()
def obj():
    ret = MultiprocessingDropbox()
    ret.open()
    yield ret
    ret.terminate()
    ret.close()

##__________________________________________________________________||
def test_put(obj):
    assert 0 == obj.put(functools.partial(task, 0.010, 'result1'))
    assert 1 == obj.put(functools.partial(task, 0.001, 'result2'))

def test_put_multiple(obj):
    assert [0, 1] == obj.put_multiple([
        functools.partial(task, 0.010, 'result1'),
        functools.partial(task, 0.001, 'result2'),
    ])

def test_put_receive(obj):
    idx1 = obj.put(functools.partial(task, 0.010, 'result1'))
    idx2 =obj.put(functools.partial(task, 0.001, 'result2'))

    expected = [
        (idx1, 'result1'),
        (idx2, 'result2'),
    ]

    actual = obj.receive()
    assert expected == actual

def test_receive_order(obj):
    # results of tasks are sorted in the order in which the tasks are put.
    idx1 = obj.put(functools.partial(task, 0.010, 'result1'))
    idx2 = obj.put(functools.partial(task, 0.001, 'result2'))
    idx3 = obj.put(functools.partial(task, 0.005, 'result3'))

    expected = [
        (idx1, 'result1'),
        (idx2, 'result2'),
        (idx3, 'result3'),
    ]

    actual = obj.receive()
    assert expected == actual

def test_put_receive_repeat(obj):
    idx1 = obj.put(functools.partial(task, 0.010, 'result1'))
    idx2 = obj.put(functools.partial(task, 0.001, 'result2'))
    expected = [
        (idx1, 'result1'),
        (idx2, 'result2'),
    ]
    actual = obj.receive()
    assert expected == actual

    idx3 = obj.put(functools.partial(task, 0.005, 'result3'))
    idx4 = obj.put(functools.partial(task, 0.002, 'result4'))
    expected = [
        (idx3, 'result3'),
        (idx4, 'result4'),
    ]
    actual = obj.receive()
    assert expected == actual


def test_begin_put_recive_end_repeat(obj):
    obj.put(functools.partial(task, 0.010, 'result1'))
    obj.receive()
    obj.close()
    obj.open()
    obj.put(functools.partial(task, 0.001, 'result2'))
    obj.receive()

def test_terminate(obj):
    obj.put(functools.partial(task, 0.010, 'result1'))
    obj.put(functools.partial(task, 0.001, 'result2'))
    obj.terminate()

def test_terminate_close(obj):
    obj.put(functools.partial(task, 0.010, 'result1'))
    obj.put(functools.partial(task, 0.001, 'result2'))
    obj.terminate()
    obj.close()

def test_receive_without_put(obj):
    assert [ ] == obj.receive()

##__________________________________________________________________||
