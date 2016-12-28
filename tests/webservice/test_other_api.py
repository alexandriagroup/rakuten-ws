# coding: utf-8
from __future__ import unicode_literals


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


def test_high_comission_shop_list(ws):
    params = {'hits': 3}
    assert_no_error(ws.other.high_commission_shop.list(**params))
