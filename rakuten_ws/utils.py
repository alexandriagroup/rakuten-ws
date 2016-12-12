# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from collections import OrderedDict

from xml.dom import minidom
from xmljson import parker, Parker

try:
    from lxml.etree import Element, fromstring, tostring
    LXML_ENABLED = True
except ImportError:
    from xml.etree.ElementTree import Element, fromstring, tostring  # noqa
    LXML_ENABLED = False

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


def xml2dict(xml_string, dict_type=None):
    """ Convert an xml string to a python dictionary."""
    if dict_type is not None:
        return Parker(dict_type=dict_type).data(fromstring(xml_string))
    return parker.data(fromstring(xml_string))


def xml_prettify(elem, encoding='utf-8'):
    if LXML_ENABLED:
        return tostring(elem, pretty_print=True, xml_declaration=True, encoding=encoding)
    else:
        return minidom.parseString(tostring(elem)).toprettyxml(encoding=encoding, indent="  ")


def dict2xml(data, root='request', pretty_print=True, encoding='utf-8'):
    """ Convert a dictionary to xml string."""
    root_element = Element(root)
    xml_element = parker.etree(data, root=root_element)

    if not pretty_print:
        return '<?xml version="1.0" encoding="UTF-8"?>' % tostring(xml_element)
    else:
        return xml_prettify(xml_element, encoding=encoding)
