# coding: utf-8
from __future__ import unicode_literals


def test_rms_order(ws):
    assert ws.rms.order.getRequestId()['message'] == "正常終了"
