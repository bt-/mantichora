# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import time
import logging

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from mantichora.hub import MultiprocessingDropbox
from mantichora.main import TaskPackage

##__________________________________________________________________||
class MockProgressReporter(object):
    pass

@pytest.fixture()
def obj():
    ret = MultiprocessingDropbox()
    ret.open()
    yield ret
    ret.close()

##__________________________________________________________________||
@pytest.fixture()
def logger():
    ret = logging.getLogger(__name__)
    ret.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    ret.addHandler(handler)
    return ret

def mocktask(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info('{}(args={!r}, kwargs={!r})'.format(
            'mocktask', args, kwargs
        ))

@pytest.fixture()
def package1():
    args = (111, 222)
    kwargs = dict(A='abc', B='def')
    return TaskPackage(task=mocktask, args=args, kwargs=kwargs)

##__________________________________________________________________||
def test_put(obj, package1, logger, caplog):
    ## caplog doesn't catch logging with obj from fixture
    ## so recreate it here
    obj = MultiprocessingDropbox()
    obj.open()
    with caplog.at_level(logging.INFO, logger=__name__):
        obj.put(package1)
    obj.close()

    assert len(caplog.records) == 1

##__________________________________________________________________||
