# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rakuten_ws.api import BaseWebService
from rakuten_ws.rms import RestClient, RestMethod, BaseRmsService


class SimpleRmsItemsAPI(RestClient):
    api_endpoint = '1.0/item'
    get = RestMethod()
    remove = RestMethod(http_method='POST', name='delete')


class SimpleRmsService(BaseRmsService):
    item = SimpleRmsItemsAPI()
    product = SimpleRmsItemsAPI(name="item_product")


class SimpleWebService(BaseWebService):
    rms = SimpleRmsService()


def test_rest_client():
    ws = SimpleWebService(application_id="AAAAA", license_key="BBBBB", secret_service="CCCCC")
    assert ws.rms.item.name == "item"
    assert ws.rms.product.name == "item_product"
    assert ws.rms.product.service == ws.rms

    assert isinstance(ws.rms.item.get, RestMethod)
    assert ws.rms.item.get.name == "get"
    assert ws.rms.item.get.http_method == "GET"
    assert ws.rms.item.remove.name == "delete"
