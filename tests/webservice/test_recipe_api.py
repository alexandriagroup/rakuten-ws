# coding: utf-8
from __future__ import unicode_literals


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


def test_category_ranking(ws):
    assert_no_error(ws.recipe.category.ranking())


def test_category_list(ws):
    assert_no_error(ws.recipe.category.list())
