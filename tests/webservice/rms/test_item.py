# coding: utf-8
from ... import slugify


URLS = {
    "insert": slugify("item test 01"),
    "search": slugify("item test 02"),
    "update1": slugify("item test 03"),
    "update2": slugify("item test 04"),
}


def cleanup(ws):
    for label in URLS:
        result = ws.rms.item.delete(item={"itemUrl": URLS[label]})
        # N000  Successful completion
        # C001  Specified Item ID does not exist
        assert result["code"] in ("C001", "N000")


def insert_item(ws, item_url):
    item = {
        "itemUrl": "%s" % item_url,
        "itemNumber": item_url,
        "itemName": "%s name" % item_url,
        "itemPrice": "999999999",
        "genreId": 409148,
        "catalogId": "9784088820811",
        "itemInventory": {
            "inventoryType": 1,
            "inventories": {"inventory": {"inventoryCount": 11}},
        },
    }
    result = ws.rms.item.insert(item=item, raise_for_status=False)
    assert result.status["message"] == "OK"
    assert result["code"] == "N000"
    return result


def test_item_insert(ws):
    cleanup(ws)
    result = insert_item(ws, URLS["insert"])
    item = result["item"]
    assert item["itemUrl"] == URLS["insert"]


def test_item_search(ws):
    cleanup(ws)
    result = insert_item(ws, URLS["search"])
    # item = result['item']
    result = ws.rms.item.search(itemUrl=URLS["insert"])
    # 200-00: successful completion
    assert result["code"] == "200-00"
    # assert result['numFound'] > 0
    # if result['numFound'] > 1:
    #     assert result['items']['item'][0]['itemUrl'] == item['itemUrl']
    # else:
    #     assert result['items']['item']['itemUrl'] == item['itemUrl']


def test_update_items(ws):
    cleanup(ws)
    insert_item(ws, URLS["update1"])
    insert_item(ws, URLS["update2"])

    items = {
        "item": [
            {"itemUrl": URLS["update1"], "itemPrice": 380000},
            {"itemUrl": URLS["update2"], "itemPrice": 480000},
        ]
    }

    result = ws.rms.items.update(items=items)
    for item_result in result["itemUpdateResult"]:
        assert item_result["code"] == "N000"


def test_delete(ws):
    cleanup(ws)
