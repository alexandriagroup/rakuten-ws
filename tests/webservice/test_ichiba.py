# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from rakuten_ws.webservice import RakutenWebService, IchibaAPI
from rakuten_ws.base import RakutenAPIResponse 


# TODO Be more precise on the differences between the 2 sets of keys
def assert_response_is_valid(response, endpoint_method):
    valid_keys = {}
    valid_keys['IchibaItem/Search'] = [u'count', u'hits', u'last',
                                       u'pageCount', u'Items', u'carrier',
                                       u'TagInformation',
                                       u'GenreInformation', u'page',
                                       u'first']
    valid_keys['IchibaItem/Ranking'] = [u'lastBuildDate', u'title', u'Items']
    valid_keys['IchibaGenre/Search'] = [u'current', u'parents', u'children']
    valid_keys['IchibaTag/Search'] = [u'tagGroups']
    valid_keys['IchibaProduct/Search'] = [u'count', u'hits', u'last',
                                          u'pageCount', u'GenreInformation',
                                          u'Products', u'page', u'first']
    assert set(response.keys()) == set(valid_keys[endpoint_method])


def assert_responses_are_valid(responses, endpoint_method):
    for i in range(1, 3):
        response = next(responses)
        assert response['page'] == i
        assert_response_is_valid(response, endpoint_method)


# TODO Test all the other parameters
def test_item_search(ws):
    assert_response_is_valid(ws.ichiba.item.search(keyword="Naruto"),
                             'IchibaItem/Search')


def test_item_search_pages(ws):
    responses = ws.ichiba.item.search(keyword="Naruto").pages()
    assert_responses_are_valid(responses, 'IchibaItem/Search')


def test_item_ranking(ws):
    assert_response_is_valid(ws.ichiba.item.ranking(carrier=0),
                             'IchibaItem/Ranking')


def test_genre_search(ws):
    assert_response_is_valid(ws.ichiba.genre.search(genreId=0, genrePath=1),
                             'IchibaGenre/Search')


def test_tag_search(ws):
    assert_response_is_valid(ws.ichiba.tag.search(tagId=1000943),
                             'IchibaTag/Search')


def test_product_search(ws):
    assert_response_is_valid(ws.ichiba.product.search(keyword='Naruto'),
                             'IchibaProduct/Search')


def test_product_search_pages(ws):
    responses = ws.ichiba.product.search(keyword="Naruto").pages()
    assert_responses_are_valid(responses, 'IchibaProduct/Search')

