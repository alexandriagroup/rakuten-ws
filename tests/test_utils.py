# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from rakuten_ws.utils import xml2dict, dict2xml, sorted_dict, camelize_dict
from rakuten_ws.compat import to_unicode, is_py3


def test_sorted_dict():
    test_dict = {
        "thirdKey": 3,
        "myDict": {
            "c": 2,
            "b": 2,
            "a": "one"
        },
        "firstKey": [
            "simple_value",
            {
                "twoValue": 2,
                "oneKey": "one"
            }
        ],
        "zzzz": 2,
        "aaaa": 1
    }
    expected_dict = OrderedDict([
        ('aaaa', 1),
        ('firstKey', ["simple_value", OrderedDict([('oneKey', 'one'), ('twoValue', 2)])]),
        ('myDict', OrderedDict([('a', 'one'), ('b', 2), ('c', 2)])),
        ('thirdKey', 3),
        ('zzzz', 2)
    ])
    assert sorted_dict(test_dict) == expected_dict


def test_camelize_dict():
    test_dict = {
        "my_list": [{"one_key": "one", "Two_key": 2, "NGKeyword": 3}, 2, "three"],
        "my_dict": {"one_key": "one", "Two_key": 2, "NGKeyword": 3},
        "first_key": 1,
        "SecondKey": 2,
        "thirdKey": 3,
    }
    expected_dict = {
        "thirdKey": 3,
        "myDict": {
            "Two_key": 2,
            "NGKeyword": 3,
            "oneKey": "one"
        },
        "myList": [
            {
                "Two_key": 2,
                "NGKeyword": 3,
                "oneKey": "one"
            }
        ],
        "SecondKey": 2,
        "firstKey": 1
    }
    assert camelize_dict(test_dict) == expected_dict


def test_xml2dict():
    xml_string = """<request>
    <cast>
        <actor>
            <firstname>Rami</firstname>
            <lastname>Malek</lastname>
            <age>35</age>
        </actor>
        <actor>
            <firstname>Carly</firstname>
            <lastname>Chaikin</lastname>
            <age>26</age>
        </actor>
    </cast>
</request>"""
    data = xml2dict(xml_string)
    assert data['cast']['actor'][1]['firstname'] == 'Carly'
    assert data['cast']['actor'][0]['age'] == 35

    class MyDictClass(dict):
        pass

    data = xml2dict(xml_string, dict_type=MyDictClass)
    assert isinstance(data, MyDictClass)


def test_dict2xml():
    expected_xml_string = """<?xml version='1.0' encoding='utf-8'?>
<request>
  <itemUpdateRequest>
    <item>
      <itemPrice>198000</itemPrice>
      <categories>
        <categoryInfo>
          <categoryId>123</categoryId>
        </categoryInfo>
      </categories>
      <itemUrl>test123</itemUrl>
    </item>
  </itemUpdateRequest>
</request>"""
    categories = OrderedDict([('categoryInfo', OrderedDict([('categoryId', 123)]))])
    item = OrderedDict([('item', OrderedDict([('itemPrice', 198000),
                                              ('categories', categories),
                                              ('itemUrl', 'test123')]))])
    data = OrderedDict([('itemUpdateRequest', item)])

    xml_string = dict2xml(data, root="request", pretty_print=True)
    assert expected_xml_string == xml_string.strip()
    expected_no_pretty_xml_string = expected_xml_string.replace('  ', '')\
                                                       .replace('\n', '')\
                                                       .replace('?>', '?>\n')
    assert expected_no_pretty_xml_string == dict2xml(data, root="request", pretty_print=False)


def test_to_unicode():
    assert to_unicode('à tester') == 'à tester'
    assert to_unicode('à tester'.encode('utf-8')) == 'à tester'
    assert to_unicode('à tester'.encode('iso-8859-1'), encoding='iso-8859-1') == 'à tester'
    assert to_unicode(352) == '352'
    assert to_unicode(bytearray([104, 101, 108, 108, 111])) == "hello"
    assert to_unicode(memoryview(b"abc")) == "abc"
    assert to_unicode(memoryview("abc".encode('iso-8859-1')), 'iso-8859-1') == "abc"
    if is_py3:
        assert to_unicode(bytes([104, 101, 108, 108, 111])) == "hello"
    else:
        assert to_unicode(buffer("Hello world", 6, 5))  # noqa
