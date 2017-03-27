# coding: utf-8
from __future__ import unicode_literals


def test_get_inventory_external(ws):
    result = ws.rms.inventory.getInventoryExternal(itemUrl='SKU7EHDR72ZZ4TPSSS')
    # 'N00-000' => Successfully completed
    assert result['errCode'] == 'N00-000'


def test_update_inventory_external(ws):
    result = ws.rms.inventory.getInventoryExternal(itemUrl='SKU7EHDR72ZZ4TPSSS')
    count = (result['getResponseExternalItem']['GetResponseExternalItem'][0]['getResponseExternalItemDetail']
                   ['GetResponseExternalItemDetail'][0]['inventoryCount'])
    update_request = {
        'itemUrl': "SKU7EHDR72ZZ4TPSSS",
        'inventoryType': 2,
        'inventoryUpdateMode': 1,
        'inventory': count + 1
    }
    result = ws.rms.inventory.updateInventoryExternal(update_request)
    # 'N00-000' => Successfully completed
    assert result['errCode'] == 'N00-000'

    result = ws.rms.inventory.getInventoryExternal(itemUrl='SKU7EHDR72ZZ4TPSSS')
    new_count = (result['getResponseExternalItem']['GetResponseExternalItem'][0]['getResponseExternalItemDetail']
                       ['GetResponseExternalItemDetail'][0]['inventoryCount'])
    assert new_count == count + 1
