# coding: utf-8
from __future__ import unicode_literals


def test_rms_inventory(ws):
    # E02-101: User authentication failed.
    assert ws.rms.inventory.getInventoryExternal()['errCode'] != 'E02-101'
