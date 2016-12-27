# coding: utf-8
from __future__ import unicode_literals

import pytest

from .. import idfn, assert_eq, assert_in
from rakuten_ws.compat import callable


def assert_response(callback, params, result):
    assert 'error' not in result, result['error_description']
    if callable(callback):
        assert len(result['Items']) > 0
        callback(params, result, result['Items'][0])


total_search_parameters = [
    ({'keyword': "ドン・キホーテ"}, lambda p, r, i: assert_in(p['keyword'], i['title'])),
    ({'booksGenreId': '001025'}, lambda p, r, i: assert_eq(i['booksGenreId'], p['booksGenreId'])),
    ({'isbnjan': '2100010283771'}, lambda p, r, i: assert_eq(i['isbn'], p['isbnjan'])),
    ({'isbnjan': '4988021149594'}, lambda p, r, i: assert_eq(i['jan'], p['isbnjan'])),
    ({'booksGenreId': '001025', 'page': '2'}, lambda p, r, i: assert_eq(r['page'], 2)),
    ({'availability': '1'}, lambda p, r, i: assert_eq(i['availability'], p['availability'])),
    ({'availability': '3'}, lambda p, r, i: assert_eq(i['availability'], p['availability'])),
    ({'outOfStockFlag': '0'}, lambda p, r, i: assert_eq(i['availability'], '1')),
    ({'chirayomiFlag': '1'}, lambda *args: True),
    ({'sort': 'standard'}, lambda *args: True),
    ({'sort': 'sales'}, lambda *args: True),
    ({'sort': '+itemPrice'}, lambda *args: True),
    ({'sort': '-itemPrice'}, lambda *args: True),
    ({'limitedFlag': 1}, lambda *args: True),
    ({'field': '1'}, lambda *args: True),
    ({'carrier': '1'}, lambda *args: True),
    ({'genreInformationFlag': 1}, lambda p, r, i: assert_in('GenreInformation', r)),
]


@pytest.mark.parametrize('params,check', total_search_parameters, ids=idfn)
def test_total_search(ws, params, check):
    if all(key not in params for key in ('keyword', 'booksGenreId', 'isbnjan')):
        params.update({'keyword': 'ドン・キホーテ'})
    assert_response(check, params, ws.books.total.search(**params))
