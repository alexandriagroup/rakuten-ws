# coding: utf-8
from __future__ import unicode_literals


from collections import OrderedDict


def test_rms_order(ws):
    assert ws.rms.order.getRequestId()['message'] == "正常終了"


def test_rms_inventory(ws):
    # E02-101: User authentication failed.
    assert ws.rms.inventory.getInventoryExternal()['errCode'] != 'E02-101'


def test_insert_url(ws):
    item = OrderedDict([
        ('item_url', 'test001'),
        ('item_name', 'test001')
    ])
    result = ws.rms.item.insert(item=item)
    assert result.status['message'] == 'AuthError'
