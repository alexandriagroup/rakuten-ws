# coding: utf-8
from __future__ import unicode_literals

from freezegun import freeze_time

import pytz
import datetime


def test_get_request_id(ws):
    # N00-000 => Successfully completed.
    assert ws.rms.order.getRequestId()['errorCode'] == "N00-000"


@freeze_time("2017-03-28")
def test_get_order(ws):
    now_tokyo = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
    # N00-000 => Successfully completed.
    kwargs = {
        'dateType': 1,
        'startDate': now_tokyo - datetime.timedelta(days=30),
        'endDate': now_tokyo - datetime.timedelta(days=0)
    }
    result = ws.rms.order.getOrder(**kwargs)
    # E10-001   検索結果が0件です   The number of search results is zero.
    result['errorCode'] == "E10-001"
