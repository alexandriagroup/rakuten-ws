# coding: utf-8
from __future__ import unicode_literals


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


def test_genre_search(ws):
    params = {'koboGenreId': '101901'}
    assert_no_error(ws.kobo.genre.search(**params))


def test_ebook_search(ws):
    params = {'author': '村上春樹', 'hits': 3}
    assert_no_error(ws.kobo.ebook.search(**params))
