# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from collections import OrderedDict, MutableMapping
from shutil import copyfileobj
from mimetypes import guess_type
from io import BytesIO, open

import requests

from xmljson import Parker
from lxml.etree import Element, fromstring, tostring

from .compat import iteritems, to_unicode, is_py2, str, urlparse, pathname2url


parker = Parker(dict_type=dict)


class PrettyStringRepr(str):
    # Useful for debug
    def __repr__(self):
        if is_py2:
            return to_unicode(self.replace(' \n', '\n').strip()).encode('utf-8')
        else:
            return to_unicode(self.replace(' \n', '\n').strip())


def camelize_dict(data, uppercase_first_letter=False):
    """ Returns a dict with camel case keys.

    >>> d = {'a_simple_key': '1', 'Another_key': '2', 'CamelKey': '3'}
    >>> sorted(camelize_dict(d).keys())
    ['Another_key', 'CamelKey', 'aSimpleKey']
    >>> camelize_dict(d)['aSimpleKey']
    '1'
    """
    new_dict = data.__class__()
    for k, v in iteritems(data):
        new_v = v
        if isinstance(v, dict):
            new_v = camelize_dict(v, uppercase_first_letter)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                if isinstance(x, dict):
                    new_v.append(camelize_dict(x, uppercase_first_letter))
                else:
                    camelize(k, uppercase_first_letter)
        new_dict[camelize(k, uppercase_first_letter)] = new_v
    return new_dict


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
    if not string.islower():
        return string
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def sorted_dict(d, key=None):
    """ Sort dict by keys.

    Examples::

    >>> sorted_dict({'3': 3, '1': 10})
    OrderedDict([('1', 10), ('3', 3)])
    >>> sorted_dict({'1': 10, '3': 3})
    OrderedDict([('1', 10), ('3', 3)])
    """
    new_dict = OrderedDict()
    for k, v in sorted(iteritems(d), key=key):
        new_v = v
        if isinstance(v, dict):
            new_v = sorted_dict(v)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                if isinstance(x, dict):
                    new_v.append(sorted_dict(x))
                else:
                    new_v.append(x)
        new_dict[k] = new_v
    return new_dict


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


def xml2dict(xml_string, encoding="utf-8", dict_type=None):
    """ Convert an xml string to a python dictionary."""
    string = to_unicode(xml_string).encode((encoding))
    if dict_type is not None:
        return Parker(dict_type=dict_type).data(fromstring(string))
    return parker.data(fromstring(string))


def dict2xml(data, root='request', pretty_print=True, xml_declaration=True, encoding='utf-8'):
    """ Convert a dictionary to xml string."""
    root_element = Element(root)
    xml_element = parker.etree(data, root=root_element)

    xml_string = tostring(xml_element,
                          pretty_print=pretty_print,
                          xml_declaration=xml_declaration,
                          encoding=encoding)
    return to_unicode(xml_string, encoding=encoding).strip()


def flatten_dict(dictionary, parent_key='', sep='.'):
    items = []
    if isinstance(dictionary, list):
        for i, subdict in enumerate(dictionary):
            for k, v in flatten_dict(subdict).items():
                items.append(('%s.@%s.%s' % (parent_key, i, k), v))
    elif isinstance(dictionary, MutableMapping):
        for k, v in dictionary.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, (MutableMapping, list)):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)


def unflatten_dict(dictionary):
    unflat_dict = dictionary.__class__()
    for key, value in dictionary.items():
        parts = key.split(".")
        d = unflat_dict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dictionary.__class__()
            d = d[part]
        d[parts[-1]] = value

    def unflatten_list_dict(dictionary):
        unflat_list_dict = dictionary.__class__()
        for k, v in dictionary.items():
            if isinstance(v, dict):
                unflat_dict = unflatten_list_dict(v)
                if sorted(unflat_dict.keys())[0] == '@0':
                    unflat_list = []
                    for key in sorted(unflat_dict.keys()):
                        unflat_list.append(unflat_dict[key])
                    new_value = unflat_list
                else:
                    new_value = unflat_dict
                unflat_list_dict[k] = new_value
            else:
                unflat_list_dict[k] = v
        return unflat_list_dict

    return unflatten_list_dict(unflat_dict)


def load_file(url, session=None, timeout=None):
    """Load the content from the given URL and return it as a `BytesIO`"""
    scheme = urlparse(url).scheme
    if scheme in ('http', 'https'):
        if session is None:
            session = requests.Session()
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content), response.headers['Content-Type']
    elif scheme in ('', 'file'):
        if url.startswith('file://'):
            url = url[7:]
        fileobj = BytesIO()
        with open(url, 'rb') as fd:
            copyfileobj(fd, fileobj)
        fileobj.seek(0)
        return fileobj, guess_type(pathname2url(url))[0]
    raise ValueError("Invalid url given to load")
