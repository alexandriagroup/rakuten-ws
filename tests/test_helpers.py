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


def idfn(val):
    return '_with_{}'.format('_'.join(sorted(["%s%s" % (k, v) for k, v in val.items()])))


item_pages_parameters = [
    {'page': 1, 'num': 3},
    {'page': 4, 'num': 2},
    {'num': 1},
]


@pytest.mark.parametrize('params', item_pages_parameters, ids=idfn)
def test_item_pages(ws, request, params):
    search_params = {'keyword': "Naruto"}

    if 'page' in params:
        search_params.update({'page': params.get('page')})

    start_page = params.get('page', 1)
    num_pages = params.get('num')

    response = ws.ichiba.item.search(**search_params)

    items = response.pages()

    # search should also allow to retrieve all the available responses
    # within a generator
    assert isinstance(items, types.GeneratorType)

    # test page count
    response.response['pageCount'] = start_page + (num_pages - 1)

    pages = list(response.pages())
    assert len(pages) == num_pages

    for i, page in enumerate(pages):
        page['page'] == i + start_page

    assert len(request.node.funcargs['use_vcr'].requests) == num_pages
