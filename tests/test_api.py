# coding: utf-8
from __future__ import unicode_literals

import pytest

from rakuten_ws import RakutenWebService


@pytest.mark.online
def test_ichiba_seach(credentials, request):
    print(credentials)
    ws = RakutenWebService(**credentials)
    item = ws.ichiba.item.search(item_code="book:17924463")['Items'][0]
    assert item['itemName'] == 'NARUTO THE BEST (期間生産限定盤) [ (アニメーション) ]'  # noqa


@pytest.mark.online
def test_fake_credentials(fake_credentials, request):
    print(fake_credentials)
    ws = RakutenWebService(**fake_credentials)
    result = ws.ichiba.item.search(item_code="book:17924463")
    assert result['error_description'] == 'specify valid applicationId'
    assert result['error'] == 'wrong_parameter'
