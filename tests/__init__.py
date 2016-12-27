# coding: utf-8
from __future__ import unicode_literals, print_function

import re

import unidecode
import pytest

from contextlib import contextmanager

from rakuten_ws.compat import to_unicode


@contextmanager
def assert_raises(exception_class, msg=None):
    """Check that an exception is raised and its message contains `msg`."""
    with pytest.raises(exception_class) as exception:
        yield
    if msg is not None:
        message = '%s' % exception
        assert msg.lower() in message.lower()


def slugify(string):
    ''' Remove special char in string '''
    string = unidecode.unidecode(to_unicode(string)).lower()
    return re.sub(r'\W+', '-', string).strip('-')


def idfn(val):
    if isinstance(val, dict):
        clean_val = dict([(k, slugify(val[k])) for k in val.keys()])
        return '_with_{}'.format('_'.join(sorted(["%s[%s]" % (k, v) for k, v in clean_val.items()])))
    return ""


def assert_eq(left, right):
    assert left == right


def assert_in(left, right):
    assert left in right
