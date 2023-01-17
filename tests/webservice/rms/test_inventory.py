SKUS = ["83620_098235830x", "81611_907930400x"]


def test_get_inventory_external(ws):
    result = ws.rms.inventory.getInventoryExternal(itemUrl=SKUS[0])
    # 'N00-000' => Successfully completed
    assert result["errCode"] == "N00-000"


def get_inventory_count(ws, sku):
    unique = False
    if not isinstance(sku, (list, tuple)):
        unique = True
        sku = [sku]
    result = ws.rms.inventory.getInventoryExternal(itemUrl=sku)
    inventory_counts = {}
    for info in result["getResponseExternalItem"]["GetResponseExternalItem"]:
        count = info["getResponseExternalItemDetail"]["GetResponseExternalItemDetail"][
            0
        ]["inventoryCount"]
        item_url = info["itemUrl"]
        inventory_counts[item_url] = count
    if unique:
        return inventory_counts[sku[0]]
    else:
        return inventory_counts


def test_update_inventory_external(ws):
    count = get_inventory_count(ws, SKUS[0])
    update_request = {
        "itemUrl": SKUS[0],
        "inventoryType": 2,
        "inventoryUpdateMode": 1,
        "inventory": count + 1,
    }
    result = ws.rms.inventory.updateInventoryExternal(update_request)
    # 'N00-000' => Successfully completed
    assert result["errCode"] == "N00-000"

    new_count = get_inventory_count(ws, SKUS[0])
    assert new_count == count + 1


def test_multiple_update_inventory_external(ws):
    item_url_list = SKUS
    counts = get_inventory_count(ws, item_url_list)
    update_request = [
        {
            "itemUrl": SKUS[0],
            "inventoryType": 2,
            "inventoryUpdateMode": 1,
            "inventory": counts[SKUS[0]] + 10,
        },
        {
            "itemUrl": SKUS[1],
            "inventoryType": 2,
            "inventoryUpdateMode": 1,
            "inventory": counts[SKUS[1]] + 10,
        },
    ]
    result = ws.rms.inventory.updateInventoryExternal(update_request)
    # 'N00-000' => Successfully completed
    assert result["errCode"] == "N00-000"

    new_counts = get_inventory_count(ws, item_url_list)

    for item_url in item_url_list:
        assert new_counts[item_url] == counts[item_url] + 10
