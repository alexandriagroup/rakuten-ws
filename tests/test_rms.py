# coding: utf-8
from __future__ import unicode_literals

import pytest

from rakuten_ws.rms import RmsClient


@pytest.mark.online
def test_rms():
    rms = RmsClient()
    assert rms.order.getRequestId()['message'] == "正常終了"
