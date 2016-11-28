# coding: utf-8
from __future__ import unicode_literals

import pytest

from rakuten_ws import RakutenWebService


@pytest.mark.online
def test_rms(credentials):
    ws = RakutenWebService(**credentials)
    assert ws.rms.order.getRequestId()['message'] == "正常終了"
