# coding: utf-8
from __future__ import unicode_literals

from . import TestAPI


class TestRMS(TestAPI):

    def test_rms_order(self):
        assert self.ws.rms.order.getRequestId()['message'] == "正常終了"
