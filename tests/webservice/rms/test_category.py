# coding: utf-8
from __future__ import unicode_literals


def test_get_categorysets(ws):
    result = ws.rms.category.get_categorysets()
    assert result['code'] == 'N000'


def test_get_categories(ws):
    result = ws.rms.category.get_categories(categorySetManageNumber=0)
    assert result['code'] == 'N000'


def insert_category(ws, name):
    params = {
        'categorySetManageNumber': 0,
        'categoryId': 0,
        'category': {'name': name}
    }
    return ws.rms.category.insert_category(**params)


def test_category_api(ws):
    """ Tested get/insert/update/delete/move category. """
    parent_category_name = '[rakuten-ws test] Chocolate'
    category_name = '[rakuten-ws test] Chocolate Ice Cream'
    new_category_name = '[rakuten-ws test] Black Chocolat'

    # Tests insert
    result = insert_category(ws, category_name)
    assert result['code'] == 'N000'
    assert 'category' in result
    assert 'categoryId' in result['category']

    # Tests get
    result = ws.rms.category.get_category(categoryId=result['category']['categoryId'])
    assert result['category']['name'] == category_name

    # Tests update
    params = {
        'categoryId': result['category']['categoryId'],
        'category': {'name': new_category_name},
    }
    result = ws.rms.category.update_category(**params)
    assert result['code'] == 'N000'
    result = ws.rms.category.get_category(categoryId=params['categoryId'])
    assert result['category']['name'] == new_category_name

    # Tests move
    result = insert_category(ws, parent_category_name)
    parent_category_id = result['category']['categoryId']
    result = ws.rms.category.move_category(categoryId=params['categoryId'],
                                           destCategoryId=parent_category_id,
                                           categorySetManageNumber=0)
    assert result['code'] == 'N000'
    result = ws.rms.category.get_categories(categorySetManageNumber=0)
    assert result['categoryList']['category'][-1]['childCategories']['category']['categoryId'] == params['categoryId']

    # Tests delete
    for category_id in (params['categoryId'], parent_category_id):
        result = ws.rms.category.delete_category(categoryId=category_id)
        assert result['code'] == 'N000'
