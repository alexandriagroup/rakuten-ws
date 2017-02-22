# coding: utf-8
from __future__ import unicode_literals


def test_get_genre(ws):
    result = ws.rms.navigation.get_genre(genre_id=0)
    assert 'genre' in result


def test_get_tag(ws):
    result = ws.rms.navigation.get_tag(genre_id=101240)
    assert 'tagLastUpdateDate' in result


def test_get_header(ws):
    result = ws.rms.navigation.get_header()
    assert "genreLastUpdateDate" in result
    assert "status" in result
    assert "tagLastUpdateDate" in result

    assert result['status'] == "Success"
