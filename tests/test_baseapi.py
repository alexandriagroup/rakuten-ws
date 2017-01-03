# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rakuten_ws.baseapi import ApiService, ApiEndpoint, BaseWebService, ApiRequest, ApiMethod


class SimpleAPI(ApiService):
    api_url = "https://testapi"
    api_version = "20140222"
    format_version = 2

    item = ApiEndpoint(ApiMethod('search'), ApiMethod('ranking'))
    product = ApiEndpoint(ApiMethod('get'), api_endpoint="Product")
    order = ApiEndpoint(ApiMethod('get'), name='orders')


class SimpleWebService(BaseWebService):

    test_api = SimpleAPI()


def test_class_api_description():
    assert SimpleWebService.test_api == SimpleAPI
    assert SimpleAPI.item == ApiEndpoint
    ws = SimpleWebService(application_id="4K95553C260362")
    assert ws.test_api.name == "test_api"
    assert ws.test_api.api_version == "20140222"
    assert ws.test_api.api_url == "https://testapi"

    assert isinstance(ws.test_api.item.search, ApiRequest)
    assert ws.test_api.item.search.build_url(item_id=23) == 'https://testapi/TestApiItem/Search/20140222?applicationId=4K95553C260362&formatVersion=2&itemId=23'  # noqa

    assert ws.test_api.product.get.build_url(product_id=23) == 'https://testapi/Product/Get/20140222?applicationId=4K95553C260362&formatVersion=2&productId=23'  # noqa

    assert ws.test_api.order.name == "orders"


def test_multiple_credentials():
    ws = SimpleWebService(application_id="4K95553C260362")
    assert ws.test_api.item.search.build_url(item_id=23) == 'https://testapi/TestApiItem/Search/20140222?applicationId=4K95553C260362&formatVersion=2&itemId=23'  # noqa
    ws = SimpleWebService(application_id="TOTOOTOTOTO")
    assert ws.test_api.item.search.build_url(item_id=23) == 'https://testapi/TestApiItem/Search/20140222?applicationId=TOTOOTOTOTO&formatVersion=2&itemId=23'  # noqa


def test_aliases_methods():

    class AnotherAPI(ApiService):
        api_version = "20131024"
        endpoint = ApiEndpoint(ApiMethod('simple_search', 'simple_hotel_search'),
                               ApiMethod('detail_search', 'hotel_detail_search'),
                               api_endpoint="Custom")

    class SimpleWebService(BaseWebService):
        api = AnotherAPI()

    ws = SimpleWebService(application_id="4K9")
    assert isinstance(ws.api.endpoint.simple_search, ApiRequest)
    assert isinstance(ws.api.endpoint.detail_search, ApiRequest)
    assert ws.api.endpoint.simple_search.build_url(item_id=23) == 'https://app.rakuten.co.jp/services/api/Custom/SimpleHotelSearch/20131024?applicationId=4K9&formatVersion=2&itemId=23'  # noqa
    assert ws.api.endpoint.detail_search.build_url(item_id=23) == 'https://app.rakuten.co.jp/services/api/Custom/HotelDetailSearch/20131024?applicationId=4K9&formatVersion=2&itemId=23'  # noqa
