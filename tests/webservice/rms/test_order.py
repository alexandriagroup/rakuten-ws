# coding: utf-8
from __future__ import unicode_literals


def test_rms_order(ws):
    # N00-000 => Successfully completed.
    assert ws.rms.order.getRequestId()['errorCode'] == "N00-000"
