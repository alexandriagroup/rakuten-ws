# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from collections import OrderedDict
from .compat import iteritems


def camelize_dict(data, uppercase_first_letter=False):
    """ Returns a dict with camel case keys.

    >>> d = {'a_simple_key': '1', 'Another_key': '2', 'CamelKey': '3'}
    >>> sorted(camelize_dict(d).keys())
    ['aSimpleKey', 'anotherKey', 'camelKey']
    >>> camelize_dict(d)['aSimpleKey']
    '1'
    """
    return {camelize(k, uppercase_first_letter):
            v for (k, v) in iteritems(data)}


def camelize(string, uppercase_first_letter=True):
    """
    Convert strings to CamelCase.

    From inflection package: https://github.com/jpvanhal/inflection

    Examples::

    >>> camelize("device_type")
    'DeviceType'
    >>> camelize("device_type", False)
    'deviceType'
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def sorted_dict(d):
    """ Sort dict by keys.

    Examples::

    >>> sorted_dict({'3': 3, '1': 10})
    OrderedDict([('1', 10), ('3', 3)])
    >>> sorted_dict({'1': 10, '3': 3})
    OrderedDict([('1', 10), ('3', 3)])
    """
    return OrderedDict(sorted(iteritems(d)))


def clean_python_variable_name(s):
    """ Convert a string to a valid python variable name.

    Examples::

    >>> clean_python_variable_name("    ")
    '____'
    >>> clean_python_variable_name("my 2@'(")
    'my_2___'
    >>> clean_python_variable_name("my superS@---variable")
    'my_superS____variable'
    """
    return re.sub('\W|^(?=\d)', '_', s)
