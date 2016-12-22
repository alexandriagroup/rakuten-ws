# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest


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


item_search_data = [
    {'keyword': 'Naruto'},
    {'genreId': 101240},
    {'shopCode': 'book'},
    {'itemCode': 'book:17924463'},
    {'tagId': 1000943},
    {'hits': 10},
    {'page': 2},
    {'sort': '+affiliateRate'},
    {'sort': '-affiliateRate'},
    {'sort': '+reviewCount'},
    {'sort': '-reviewCount'},
    {'sort': '+reviewAverage'},
    {'sort': '-reviewAverage'},
    {'sort': '+itemPrice'},
    {'sort': '-itemPrice'},
    {'sort': '+updateTimestamp'},
    {'sort': '-updateTimestamp'},
    {'sort': 'standard'},
    {'minPrice': 100000},
    {'maxPrice': 1000000},
    {'availability': 1},
    {'field': 1},
    {'carrier': 2},
    {'imageFlag': 1},
    {'orFlag': 1, 'maxPrice': 10000},
    {'NGKeyword': 'Ninja'},
    {'purchaseType': 1},
    {'shipOverseasFlag': 0},
    {'shipOverseasArea': 'ALL', 'shipOverseasFlag': 1},
    {'asurakuFlag': 1},
    {'pointRateFlag': 1},
    {'pointRateFlag': 1, 'pointRate': 2},
    {'postageFlag': 1},
    {'creditCardFlag': 1},
    {'giftFlag': 1},
    {'hasReviewFlag': 1},
    {'maxAffiliateRate': 10.0},
    {'minAffiliateRate': 5.0},
    {'hasMovieFlag': 1},
    {'pamphletFlag': 1},
    {'appointDeliveryDateFlag': 1},
    {'genreInformationFlag': 1},
    {'tagInformationFlag': 1},
]

item_ranking_data = [
    # {'genreId', ?}
    {'age': 20},
    {'sex': 1},
    {'carrier': 0},
    {'page': 2},
    {'period': 'realtime'},
]


genre_search_data = [
    {'genrePath': 1},
]

product_search_data = [
    {'genreId': 101240},
    {'hits': 15},
    {'page': 2},
    {'sort': '-releaseDate'},
    {'sort': '-seller'},
    {'sort': '-satisfied'},
    {'sort': 'standard'},
    {'minPrice': 10000},
    {'maxPrice': 100000},
    {'orFlag': 1, 'maxPrice': 10000},
    {'genreInformationFlag': 0},
]


def idfn(val):
    return '_with_{}'.format('_'.join(val.keys()))


@pytest.mark.parametrize('params', item_search_data, ids=idfn)
def test_item_search(ws, params):
    params.update(keyword='Naruto')
    assert_response_is_valid(ws.ichiba.item.search(**params), 'IchibaItem/Search')


def test_item_search_error_response_with_invalid_param(ws):
    assert 'error' in ws.ichiba.item.search(ninja='Naruto')


def test_item_search_error_response_without_required_param(ws):
    assert 'error' in ws.ichiba.item.search(page=1)


def test_item_search_pages(ws):
    responses = ws.ichiba.item.search(keyword="Naruto").pages()
    assert_responses_are_valid(responses, 'IchibaItem/Search')


@pytest.mark.parametrize('params', item_ranking_data, ids=idfn)
def test_item_ranking(ws, params):
    assert_response_is_valid(ws.ichiba.item.ranking(**params),
                             'IchibaItem/Ranking')


@pytest.mark.parametrize('params', genre_search_data, ids=idfn)
def test_genre_search(ws, params):
    params.update(genreId=0)
    assert_response_is_valid(ws.ichiba.genre.search(**params),
                             'IchibaGenre/Search')


def test_genre_search_error_response_without_required_param(ws):
    assert 'error' in ws.ichiba.genre.search(genrePath=1)


def test_tag_search(ws):
    assert_response_is_valid(ws.ichiba.tag.search(tagId=1000943),
                             'IchibaTag/Search')


@pytest.mark.parametrize('params', product_search_data, ids=idfn)
def test_product_search(ws, params):
    params.update(keyword='Naruto')
    assert_response_is_valid(ws.ichiba.product.search(**params),
                             'IchibaProduct/Search')


def test_product_search_pages(ws):
    responses = ws.ichiba.product.search(keyword="Naruto").pages()
    assert_responses_are_valid(responses, 'IchibaProduct/Search')


def test_product_search_error_response_without_required_param(ws):
    assert 'error' in ws.ichiba.product.search(page=1)
