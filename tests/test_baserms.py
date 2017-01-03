# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

import pytest
import lxml
import requests

from rakuten_ws.baseapi import BaseWebService
from rakuten_ws.baserms import RestClient, RestMethod, BaseRmsService, RMSInvalidResponse
from rakuten_ws.utils import dict2xml

from . import assert_raises


delete_params = [
    'item.args',
    'item.args.arg2',
    'item.args.arg1',
]


class ItemsAPI(RestClient):
    get = RestMethod()
    remove = RestMethod(http_method='POST', name='delete', params=delete_params)
    search = RestMethod(http_method='GET')


class ProductAPI(RestClient):
    api_version = '2.0'
    get_tag = RestMethod(name='genre/tag/get')
    remove = RestMethod(http_method='POST')


class OrderAPI(RestClient):
    api_url = 'https://orderapi.rms.rakuten.co.jp'

    api_endpoint = 'myorders'
    api_version = '1.0'
    get = RestMethod()
    remove = RestMethod(http_method='POST', name='delete')


class SimpleRmsService(BaseRmsService):
    item = ItemsAPI()
    product = ProductAPI(name="item_product")
    order = OrderAPI()


class SimpleWebService(BaseWebService):
    rms = SimpleRmsService()


def test_fake_credentials():
    assert SimpleWebService.rms == SimpleRmsService
    assert SimpleRmsService.item == ItemsAPI
    assert ItemsAPI.get == RestMethod

    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC", shop_url="shop_url")
    assert ws.rms.soap_user_auth_model == {'authKey': 'ESA Q0NDQ0M6QkJCQkI=', 'shopUrl': 'shop_url', 'userName': ''}
    assert ws.rms.item.name == "item"
    assert ws.rms.product.name == "item_product"
    assert ws.rms.product.service == ws.rms

    assert isinstance(ws.rms.item.get, RestMethod)
    assert ws.rms.item.get.name == "get"
    assert ws.rms.item.get.http_method == "GET"
    assert ws.rms.item.remove.name == "delete"
    assert ws.rms.product.remove.name == "remove"


def test_params_order(httpretty):
    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC", shop_url="shop_url")

    # check with valid params
    item = {'args': {'arg1': 'value1', 'arg2': 'value2'}}
    xml_post = ws.rms.item.remove.prepare_xml_post({'item': item})
    expected_body = """<?xml version='1.0' encoding='utf-8'?>
<request>
  <itemDeleteRequest>
    <item>
      <args>
        <arg2>value2</arg2>
        <arg1>value1</arg1>
      </args>
    </item>
  </itemDeleteRequest>
</request>"""
    assert xml_post == expected_body

    # check with valid+invalid params
    item = {'args': {'arg1': 'value1', 'arg2': 'value2', 'arg3': 'value3'}}
    with pytest.warns(SyntaxWarning):
        xml_post = ws.rms.item.remove.prepare_xml_post({'item': item})
    expected_body = """<?xml version='1.0' encoding='utf-8'?>
<request>
  <itemDeleteRequest>
    <item>
      <args>
        <arg2>value2</arg2>
        <arg1>value1</arg1>
        <arg3>value3</arg3>
      </args>
    </item>
  </itemDeleteRequest>
</request>"""
    assert xml_post == expected_body


def test_rest_client():
    assert SimpleWebService.rms == SimpleRmsService
    assert SimpleRmsService.item == ItemsAPI
    assert ItemsAPI.get == RestMethod

    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC", shop_url="shop_url")
    ws.rms.soap_user_auth_model == {'authKey': 'ESA Q0NDQ0M6QkJCQkI=', 'shopUrl': 'shop_url', 'userName': ''}
    assert ws.rms.item.name == "item"
    assert ws.rms.product.name == "item_product"
    assert ws.rms.product.service == ws.rms

    assert isinstance(ws.rms.item.get, RestMethod)
    assert ws.rms.item.get.name == "get"
    assert ws.rms.item.get.http_method == "GET"
    assert ws.rms.item.remove.name == "delete"
    assert ws.rms.product.remove.name == "remove"


def test_rest_client_get_request():
    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    prepped_request = ws.rms.item.get.prepare_request()
    assert prepped_request.url == 'https://api.rms.rakuten.co.jp/es/1.0/item/get'
    assert prepped_request.headers['Authorization'] == 'ESA Q0NDQ0M6QkJCQkI='
    assert 'Authorization' in prepped_request.headers
    assert prepped_request.body is None

    assert ws.rms.product.get_tag.prepare_request().url == \
        'https://api.rms.rakuten.co.jp/es/2.0/item_product/genre/tag/get'
    assert ws.rms.order.get.prepare_request().url == 'https://orderapi.rms.rakuten.co.jp/1.0/myorders/get'


def test_rest_client_post_request():
    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    item = OrderedDict([
        ('item_url', 'http://item_url'),
        ('itemPrice', 2000),
        ('genre_id', 32),
    ])
    prepped_request = ws.rms.order.remove.prepare_request(dict(item=item))

    assert prepped_request.url == 'https://orderapi.rms.rakuten.co.jp/1.0/myorders/delete'
    expected_body = """<?xml version='1.0' encoding='utf-8'?>
<request>
  <orderDeleteRequest>
    <item>
      <itemUrl>http://item_url</itemUrl>
      <itemPrice>2000</itemPrice>
      <genreId>32</genreId>
    </item>
  </orderDeleteRequest>
</request>"""
    assert prepped_request.body == expected_body


def test_rest_client_get_response(httpretty):

    get_xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<result>
    <status>
        <interfaceId>item.get</interfaceId>
        <systemStatus>OK</systemStatus>
        <message>OK</message>
        <requestId>714a4983-555f-42d9-aeea-89dae89f2f55</requestId>
        <requests>
            <itemUrl>aaa</itemUrl>
        </requests>
    </status>
    <itemGetResult>
        <code>N000</code>
        <item>
            <itemUrl>aaa</itemUrl>
            <itemName>test</itemName>
            <itemPrice>1000</itemPrice>
        </item>
    </itemGetResult>
</result>"""
    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    httpretty.register_uri(httpretty.GET, 'https://api.rms.rakuten.co.jp/es/1.0/item/get',
                           body=get_xml_response,
                           content_type='application/xml')

    result = ws.rms.item.get(item_url="aaa")
    assert result.status['interfaceId'] == 'item.get'
    assert result.status['systemStatus'] == 'OK'
    assert result.status['message'] == 'OK'
    assert result['code'] == 'N000'
    assert result['item']['itemUrl'] == 'aaa'
    assert result['item']['itemName'] == 'test'
    assert result['item']['itemPrice'] == 1000

    expected_json = """{
    "result": {
        "code": "N000",
        "item": {
            "itemName": "test",
            "itemPrice": 1000,
            "itemUrl": "aaa"
        }
    },
    "status": {
        "interfaceId": "item.get",
        "message": "OK",
        "requestId": "714a4983-555f-42d9-aeea-89dae89f2f55",
        "requests": {
            "itemUrl": "aaa"
        },
        "systemStatus": "OK"
    }
}"""
    assert result.json == expected_json
    assert result.xml == get_xml_response


def test_rest_client_get_404_response(httpretty):

    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    httpretty.register_uri(httpretty.GET, 'https://api.rms.rakuten.co.jp/es/1.0/item/get',
                           body="指定されたページが見つかりません（エラー404）: 楽天",
                           status=404)

    with assert_raises(requests.exceptions.HTTPError, "404 Client Error"):
        ws.rms.item.get(item_url="aaa")


def test_rest_client_get_invalid_xml(httpretty):

    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    httpretty.register_uri(httpretty.GET, 'https://api.rms.rakuten.co.jp/es/1.0/item/get',
                           body='<?xml ssversion="1.0"? encoding="UTF-8"?>',
                           status=200)
    with assert_raises(lxml.etree.XMLSyntaxError):
        ws.rms.item.get(item_url="aaa")


def test_rest_client_get_invalid_response(httpretty):

    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    httpretty.register_uri(httpretty.GET, 'https://api.rms.rakuten.co.jp/es/1.0/item/get',
                           body=dict2xml({'error': 400}),
                           content_type='application/xml')

    with assert_raises(RMSInvalidResponse):
        ws.rms.item.get(item_url="aaa")
