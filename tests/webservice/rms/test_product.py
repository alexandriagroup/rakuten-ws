# coding: utf-8
from __future__ import unicode_literals


def test_product_search(ws):
    result = ws.rms.product.search(keyword="Tokyo Tower")
    assert result.status['systemStatus'] == "OK"
    assert result.status['message'] == "OK"
    assert 'TOKYO TOWER' in result['products']['product'][0]['productName'].upper()
