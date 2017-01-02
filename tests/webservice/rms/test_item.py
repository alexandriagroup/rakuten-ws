# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from ... import slugify


def cleanup(ws):
    try:
        for item_url in ('item test 02', ):
            ws.rms.item.delete(item={'itemUrl': slugify(item_url)}, raise_for_status=False)
    except:
        pass


def insert_item(ws, name):
    item_url = slugify(name)
    item = OrderedDict([
        ('itemUrl', '%s' % item_url),
        ('itemNumber', name),
        ('itemName', '%s' % name),
        ('itemPrice', '298000'),
        ('genreId', 409148),
        ('itemInventory', {'inventoryType': 1, 'inventories': {'inventory': {'inventoryCount': 11}}}),
    ])
    result = ws.rms.item.insert(item=item, raise_for_status=False)
    assert result.status['message'] == "OK"
    return result


def test_item_insert(ws):
    cleanup(ws)
    item = insert_item(ws, 'item test 02')['item']
    assert item['itemUrl'] == 'item-test-02'


def test_item_search(ws):
    item = insert_item(ws, 'item test 02')['item']
    assert ws.rms.item.search(itemUrl=item['itemUrl'])['numFound'] > 0


def test_item_delete(ws):
    item = insert_item(ws, 'item test 02')['item']
    result = ws.rms.item.delete(item=item, raise_for_status=False)
    assert result.status['message'] == 'OK'
