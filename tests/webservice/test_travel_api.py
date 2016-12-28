# coding: utf-8
from __future__ import unicode_literals


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


def test_simple_search(ws):
    params = {'latitude': 125994.28, 'longitude': 488781.51, 'hits': 3}
    assert_no_error(ws.travel.hotel.simple_search(**params))


def test_detail_search(ws):
    params = {'hotel_no': 136197}
    assert_no_error(ws.travel.hotel.detail_search(**params))


def test_search_vacant(ws):
    params = {'latitude': '125994.28', 'longitude': '488781.51',
              'checkinDate': '2016-12-30', 'checkoutDate': '2017-01-10'}
    assert_no_error(ws.travel.hotel.search_vacant(**params))


def test_ranking(ws):
    params = {'hits': 3}
    assert_no_error(ws.travel.hotel.ranking(**params))


def test_get_chain_list(ws):
    assert_no_error(ws.travel.hotel.get_chain_list())


def test_keyword_search(ws):
    params = {'keyword': "Tokyo"}
    assert_no_error(ws.travel.hotel.keyword_search(**params))


def test_get_area_class(ws):
    assert_no_error(ws.travel.area.get_class())
