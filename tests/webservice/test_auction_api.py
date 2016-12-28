# coding: utf-8
from __future__ import unicode_literals

import pytest


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


@pytest.mark.skip(reason="This endpoint is experiencing some technical difficulties")
def test_genre_id_search(ws):
    params = {'auctionGenreId': '1150000000'}
    assert_no_error(ws.auction.genre_id.search(**params))


@pytest.mark.skip(reason="This endpoint is experiencing some technical difficulties")
def test_genre_keyword_search(ws):
    params = {'keyword': '硬貨'}
    assert_no_error(ws.auction.genre_keyword.search(**params))


@pytest.mark.skip(reason="This endpoint is experiencing some technical difficulties")
def test_item_search(ws):
    params = {'keyword': '郵便切手', 'hits': 3}
    assert_no_error(ws.auction.item.search(**params))


@pytest.mark.skip(reason="This endpoint is experiencing some technical difficulties")
def test_item_code_search(ws):
    params = {'itemCode': 'a:10959536:10024189'}
    assert_no_error(ws.auction.item_code.search(**params))
