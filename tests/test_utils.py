# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from rakuten_ws.utils import xml2dict, dict2xml


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
