# -*- coding: utf-8 -*-
import sys

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

#: Python 3.3.x
is_py33 = (is_py3 and _ver[1] == 3)

#: Python 3.4.x
is_py34 = (is_py3 and _ver[1] == 4)

#: Python 3.5.x
is_py35 = (is_py3 and _ver[1] == 5)

#: Python 2.7.x
is_py27 = (is_py2 and _ver[1] == 7)


if is_py3:
    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)

    def iteritems(d):
        return iter(d.items())

    def is_bytes(x):
        return isinstance(x, (bytes, memoryview, bytearray))

    from collections import Callable

    def callable(obj):
        return isinstance(obj, Callable)

else:
    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring

    def iteritems(d):
        return d.iteritems()

    def is_bytes(x):
        return isinstance(x, (buffer, bytearray, memoryview))

    callable = callable


def to_unicode(obj, encoding='utf-8'):
    """
    Convert ``obj`` to unicode"""
    # unicode support
    if isinstance(obj, str):
        return obj

    # string support
    if isinstance(obj, basestring):
        return str(obj, encoding)

    # bytes support
    if is_bytes(obj):
        if hasattr(obj, 'tobytes'):
            return str(obj.tobytes(), encoding)
        try:
            return str(obj, encoding)
        except:
            pass

    return str(obj)
