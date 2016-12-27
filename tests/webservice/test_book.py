# coding: utf-8
from __future__ import unicode_literals

import pytest

from .. import idfn, assert_eq, assert_in
from rakuten_ws.compat import callable


def assert_response(params, result, callback=None):
    assert 'error' not in result, result['error_description']
    assert len(result['Items']) > 0
    if callable(callback):
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
    params.update({'hits': 3})
    if all(key not in params for key in ('keyword', 'booksGenreId', 'isbnjan')):
        params.update({'keyword': 'ドン・キホーテ'})
    assert_response(params, ws.books.total.search(**params), callback=check)


book_search_parameters = [
    ({'title': "ワンピース"}, lambda p, r, i: assert_in(p['title'], i['title'])),
    ({'author': "尾田・栄一郎"}, lambda p, r, i: assert_eq(i['author'], i['author'])),
    ({'isbn': "9784088701752"}, lambda p, r, i: assert_in(p['isbn'], i['isbn'])),
    ({'size': "9"}, lambda p, r, i: assert_in(i['size'], 'コミック')),
    ({'sort': 'standard'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': 'sales'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': '+releaseDate'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': '-releaseDate'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': '+itemPrice'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': '-itemPrice'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': 'reviewCount'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'sort': 'reviewAverage'}, lambda p, r, i: assert_eq(len(r['Items']), p['hits'])),
    ({'booksGenreId': '001001001008'}, lambda p, r, i: assert_eq(i['booksGenreId'], p['booksGenreId'])),
    ({'elements': 'title,author'}, lambda p, r, i: assert_eq(set(i.keys()), set(p['elements'].split(',')))),
]


@pytest.mark.parametrize('params,check', book_search_parameters, ids=idfn)
def test_book_search(ws, params, check):
    params.update({'hits': 3})
    assert_response(params, ws.books.book.search(**params), callback=check)


def test_cd_search(ws):
    params = {'artistName': "Speed", 'hits': 3}
    assert_response(params, ws.books.cd.search(**params))


def test_dvd_search(ws):
    params = {'title': "ワンピース", 'hits': 3}
    assert_response(params, ws.books.dvd.search(**params))


def test_foreign_book_search(ws):
    params = {'author': "cervantes", 'hits': 3}
    assert_response(params, ws.books.foreign_book.search(**params))


def test_magazine_search(ws):
    params = {'title': "ファミ通", 'hits': 3}
    assert_response(params, ws.books.magazine.search(**params))


def test_game_search(ws):
    params = {'title': "mario", 'hits': 3}
    assert_response(params, ws.books.game.search(**params))


def test_software_search(ws):
    params = {'os': "windows", 'hits': 3}
    assert_response(params, ws.books.software.search(**params))


def test_genre_search(ws):
    params = {'booksGenreId': "001", 'hits': 3}
    result = ws.books.genre.search(**params)
    assert len(result["children"]) > 0
    assert len(result["parents"]) == 0
