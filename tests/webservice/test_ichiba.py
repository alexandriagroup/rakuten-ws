# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
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


testdata = [
    {'keyword': 'Naruto'},
    {'genreId': 101240},
    # {'shopCode': ?},
    # {'itemCode': ?},
    # {'tagId': ?},
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
    {'NGKeyword': 'Ninja', 'maxPrice': 10000},
    {'purchaseType': 1},
    {'shipOverseasFlag': 1},
    # {'shipOverseasArea': ?},
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
    # {'elements': ?},
    {'genreInformationFlag': 1},
    {'tagInformationFlag': 1},
    # {'affiliateId': ?},

]

def idfn(val):
    return '_with_{}'.format(val.keys()[0])


@pytest.mark.parametrize('params', testdata, ids=idfn)
def test_item_search(ws, params):
    params.update(keyword='Naruto')
    assert_response_is_valid(ws.ichiba.item.search(**params), 'IchibaItem/Search')


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
