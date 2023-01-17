# coding: utf-8
def test_rakutenpay_order_search_order(ws):
    params = {
        "dateType": 1,
        "startDatetime": "2020-08-01T00:00:00+0900",
        "endDatetime": "2020-08-03T00:00:00+0900",
        "PaginationRequestModel": {
            "requestRecordsAmount": 1000,
            "requestPage": 1,
            "SortModelList": [{"sortColumn": 1, "sortDirection": 1}],
        },
    }
    result = ws.rms.rakutenpay_order.searchOrder(**params)
    assert (
        result["MessageModelList"][0]["messageCode"]
        == "ORDER_EXT_API_SEARCH_ORDER_INFO_101"
    )


def test_rakutenpay_order_get_order(ws):
    params = {"orderNumberList": ["375055-20200802-00000845"], "version": 1}
    result = ws.rms.rakutenpay_order.getOrder(**params)
    # ORDER_EXT_API_GET_ORDER_INFO_101
    # 受注情報取得に成功しました。: Successful order information acquisition.
    assert (
        result["MessageModelList"][0]["messageCode"]
        == "ORDER_EXT_API_GET_ORDER_INFO_101"
    )


def test_rakutenpay_order_confirm_order(ws):
    params = {
        "orderNumberList": ["375055-20200821-00002833"],
    }
    result = ws.rms.rakutenpay_order.confirmOrder(**params)
    # ORDER_EXT_API_CONFIRM_ORDER_INFO_101
    # 注文確認に成功しました。: 注文確認に成功しました。
    assert (
        result["MessageModelList"][0]["messageCode"]
        == "ORDER_EXT_API_CONFIRM_ORDER_INFO_101"
    )
