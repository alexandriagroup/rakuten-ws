# -*- coding: utf-8 -*-
import re
from .compat import iteritems


def camelize_dict(data):
    """ Returns a dict with camel case keys.

    >>> d = {'a_simple_key': '1', 'Another_key': '2', 'CamelKey': '3'}
    >>> sorted(camelize_dict(d).keys())
    ['ASimpleKey', 'AnotherKey', 'CamelKey']
    >>> camelize_dict(d)['ASimpleKey']
    '1'
    """
    return {camelize(k): v for (k, v) in iteritems(data)}


def camelize(string, uppercase_first_letter=True):
    """
    Convert strings to CamelCase.

    From inflection lib: https://github.com/jpvanhal/inflection

    Examples::

    >>> camelize("device_type")
    'DeviceType'
    >>> camelize("python_version", False)
    'pythonVersion'

    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]
