# coding: utf-8
from __future__ import unicode_literals


def test_rms_order(ws):
    assert ws.rms.order.getRequestId()['message'] == "正常終了"


def test_rms_inventory(ws):
    # E02-101: User authentication failed.
    assert ws.rms.inventory.getInventoryExternal()['errCode'] != 'E02-101'


# def test_insert_url(ws):
#     from collections import OrderedDict
#     item = OrderedDict([
#         ('item_url', 'test001'),
#         ('item_name', 'test001')
#     ])
#     result = ws.rms.item.insert(item=item)
#     assert result.status['message'] == 'AuthError'


def test_product_search(ws):
    result = ws.rms.product.search(keyword="Tokyo Tower")
    assert result.status['systemStatus'] == "OK"
    assert result.status['message'] == "OK"
    assert result['products']['product'][0]['productName'] == 'TOKYO TOWER／SHYLOCKCDアルバム／邦楽'
