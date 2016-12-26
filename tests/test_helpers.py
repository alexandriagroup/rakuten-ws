# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
import types
from rakuten_ws.webservice import RakutenWebService
from rakuten_ws.baseapi import ApiResponse


@pytest.mark.online
def test_response(credentials):
    ws = RakutenWebService(**credentials)
    response = ws.ichiba.item.search(keyword="Naruto")
    assert isinstance(response, ApiResponse)


@pytest.mark.online
def test_single_item(credentials):
    ws = RakutenWebService(**credentials)
    response = ws.ichiba.item.search(keyword="Naruto")
    item = response['Items'][0]
    assert "naruto" in item['itemName'].lower()


@pytest.mark.online
def test_item_pages(credentials):
    ws = RakutenWebService(**credentials)
    response = ws.ichiba.item.search(keyword="Naruto")
    items = response.pages()

    # search should also allow to retrieve all the available responses
    # within a generator
    assert isinstance(items, types.GeneratorType)

    # test page count
    response.response['pageCount'] = 3
    pages = list(response.pages())
    assert len(pages) == 3
    for i, page in enumerate(pages):
        page['page'] == i + 1
