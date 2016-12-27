# coding: utf-8
from __future__ import unicode_literals

import pytest
import requests

from ... import assert_raises


product_ids = [
    "4943586953048", "4943586934344", "4943586934368", "4943586934337", "4943586934351",
    "4943586927957", "4943586933033", "4943586933040", "4943586948099", "4943586988033",
    "4943586998407", "4943586933026", "4943586988026", "4943586933057", "4943586988019",
    "4943586924819", "4943586948082", "4943586927926", "4943586998414", "4943586953031",
    "4943586927933", "4943586924802", "4943586927940", "4943586998391", "4943586988002",
    "4943586998384", "4908055660261", "6922017898781", "1001000004814135", "1001000004102447"
]

product_search_parameters = [
    {'productId': 4986773144973},
    {'productId': ','.join(product_ids)},
    {'keyword': 'ワンピース'},
    {'genreId': '/0/100371/110729/403839'},
    {'genreId': '/0/100371/110729/403839', 'sortBy': 'standardPriceAsc', 'offset': 0, 'limit': 15},
    {'makerName': 'ダイキサウンド'},
    {'makerName': '高電社'},
]


def idfn(val):
    return '_with_{}'.format('_'.join(sorted(val.keys())))


def assert_result_is_valid(result):
    assert result.status['systemStatus'] == "OK"
    assert result.status['message'] == "OK"
    keys = {'reviewUrlPC', 'productId', 'rankTargetGenreId', 'genreName', 'makerName', 'reviewUrlMobile', 'rank',
            'updateDate', 'detailInfo', 'genreId', 'reviewCount', 'reviewAverage', 'releaseDate', 'standardPrice',
            'productName', 'releaseDateDisp', 'rankTargetProductCount', 'productNo', 'brandName', 'isOpenPrice',
            'taxCategory'}
    if isinstance(result['products']['product'], dict):
        # One result
        product = result['products']['product']
    else:
        product = result['products']['product'][0]

    assert set(product.keys()) == keys


@pytest.mark.parametrize('params', product_search_parameters, ids=idfn)
def test_product_search(ws, params):
    assert_result_is_valid(ws.rms.product.search(**params))


def test_product_search_no_result(ws):
    result = ws.rms.product.search(keyword="djshfksdhgflhskdjdsfbhdezeeeeeeeee")
    assert dict(result) == {}


def test_product_search_wrong_params(ws):
    with assert_raises(requests.exceptions.HTTPError):
        ws.rms.product.search(keywordd="Tokyo", testWrongParameter="test")
