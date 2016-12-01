# coding: utf-8
from __future__ import unicode_literals

import pytest

from rakuten_ws import RakutenWebService


@pytest.mark.online
class TestAPI(object):

    @pytest.fixture(autouse=True)
    def setup_webservice(self, credentials):
        self.ws = RakutenWebService(**credentials)
