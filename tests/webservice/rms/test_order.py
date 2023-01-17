# coding: utf-8
from freezegun import freeze_time

import pytz
import datetime


def test_get_request_id(ws):
    # N00-000 => Successfully completed.
    assert ws.rms.order.getRequestId()["errorCode"] == "N00-000"


@freeze_time("2017-03-28")
def test_get_order(ws):
    now_tokyo = datetime.datetime.now(tz=pytz.timezone("Asia/Tokyo"))
    # N00-000 => Successfully completed.
    kwargs = {
        "dateType": 1,
        "startDate": now_tokyo - datetime.timedelta(days=30),
        "endDate": now_tokyo - datetime.timedelta(days=0),
    }
    result = ws.rms.order.getOrder(**kwargs)
    # E10-001   検索結果が0件です   The number of search results is zero.
    result["errorCode"] == "E10-001"


def test_update_order(ws):
    request_id = ws.rms.order.getRequestId()["requestId"]
    order_model = {"orderNumber": 333, "status": "processed"}
    result = ws.rms.order.updateOrder(requestId=request_id, orderModel=order_model)
    for unit_error in result["unitError"]:
        # E04-151   指定された受注番号の形式が不正です   Specified order number format is invalid.
        unit_error["errorCode"] == "E04-151"


def test_update_orders(ws):
    request_id = ws.rms.order.getRequestId()["requestId"]
    order_model = [
        {"orderNumber": 111, "status": "awaiting shipment"},
        {"orderNumber": 222, "status": "processed"},
    ]
    result = ws.rms.order.updateOrder(requestId=request_id, orderModel=order_model)
    for unit_error in result["unitError"]:
        # E04-151   指定された受注番号の形式が不正です   Specified order number format is invalid.
        unit_error["errorCode"] == "E04-151"
