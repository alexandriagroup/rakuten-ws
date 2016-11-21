# coding: utf-8
from __future__ import unicode_literals

from rakuten_ws.api import RakutenWebservice


def test_ichiba(credentials):
    ws = RakutenWebservice(**credentials)
    item = ws.ichiba.item.search(item_code="book:17924463")['Items'][0]
    assert item['itemName'] == 'NARUTO THE BEST (期間生産限定盤) [ (アニメーション) ]'  # noqa
