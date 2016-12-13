# coding: utf-8
from __future__ import unicode_literals
from .base import (RakutenAPIEndpoint, RakutenAPI, BaseWebService, ApiMethod)

from .rms import BaseRmsClient, RmsSoapApi


class IchibaAPI(RakutenAPI):
    item = RakutenAPIEndpoint(ApiMethod('search', api_version='20140222'),
                              ApiMethod('ranking', api_version='20120927'))
    genre = RakutenAPIEndpoint(ApiMethod('search', api_version='20120723'))
    tag = RakutenAPIEndpoint(ApiMethod('search', api_version='20140222'))
    product = RakutenAPIEndpoint(ApiMethod('search', api_version='20140305'), api_endpoint='Product')


class BooksAPI(RakutenAPI):
    api_version = "20130522"

    total = RakutenAPIEndpoint(ApiMethod('search'))
    book = RakutenAPIEndpoint(ApiMethod('search'))
    cd = RakutenAPIEndpoint(ApiMethod('search'), name='CD', )
    dvd = RakutenAPIEndpoint(ApiMethod('search'), name='DVD')
    foreign_book = RakutenAPIEndpoint(ApiMethod('search'))
    magazine = RakutenAPIEndpoint(ApiMethod('search'))
    game = RakutenAPIEndpoint(ApiMethod('search'))
    software = RakutenAPIEndpoint(ApiMethod('search'))
    genre = RakutenAPIEndpoint(ApiMethod('search'),
                               ApiMethod('ranking', api_version="20121128"))


class TravelAPI(RakutenAPI):
    api_version = "20131024"

    hotel = RakutenAPIEndpoint(ApiMethod('simple_search', 'simple_hotel_search'),
                               ApiMethod('detail_search', 'hotel_detail_search'),
                               ApiMethod('search_vacant', 'vacant_hotel_search'),
                               ApiMethod('ranking', 'hotel_ranking'),
                               ApiMethod('get_chain_list', 'get_hotel_chain_list'),
                               ApiMethod('keyword_search', 'keyword_hotel_search'),
                               api_endpoint="Travel")
    area = RakutenAPIEndpoint(ApiMethod('get_class', 'get_area_class'), api_endpoint="Travel")


class AuctionAPI(RakutenAPI):
    api_version = "20120927"

    genre_id = RakutenAPIEndpoint(ApiMethod('search'))
    genre_keyword = RakutenAPIEndpoint(ApiMethod('search'))
    item = RakutenAPIEndpoint(ApiMethod('search'))
    item_code = RakutenAPIEndpoint(ApiMethod('search'))


class KoboAPI(RakutenAPI):
    api_version = "20131010"

    genre = RakutenAPIEndpoint(ApiMethod('search', 'genre_search'), api_endpoint="Kobo")
    ebook = RakutenAPIEndpoint(ApiMethod('search', 'ebook_search'), api_endpoint="Kobo")


class GoraAPI(RakutenAPI):
    api_version = "20131113"

    golf = RakutenAPIEndpoint(ApiMethod('search', 'gora_golf_course_search'),
                              ApiMethod('detail', 'gora_golf_course_detail'),
                              api_endpoint="Gora")
    plan = RakutenAPIEndpoint(ApiMethod('search', 'gora_plan_search'),
                              api_endpoint="Gora")


class RecipeAPI(RakutenAPI):
    api_version = "20121121"

    category = RakutenAPIEndpoint(ApiMethod('ranking', 'category_ranking'),
                                  ApiMethod('list', 'category_list'),
                                  api_endpoint="Recipe")


class OtherAPI(RakutenAPI):
    api_version = "20131205"

    high_comission_shop = RakutenAPIEndpoint(ApiMethod('list'), api_endpoint="HighComissionShop")


class RmsOrderAPI(RmsSoapApi):
    wsdl_url = "https://api.rms.rakuten.co.jp/es/1.0/order/ws?WSDL"


class RmsClient(BaseRmsClient):
    order = RmsOrderAPI()
    # item = RmsRestEndpoint(RmsRestMethod('get', type='GET'),
    #                        RmsRestMethod('insert', type='POST'),
    #                        RmsRestMethod('update', type='POST'),
    #                        RmsRestMethod('delete', type='POST'),
    #                        RmsRestMethod('search', type='GET'))
    # items = RmsRestEndpoint(RmsRestMethod('update', type='POST'))


class RakutenWebService(BaseWebService):

    rms = RmsClient()

    ichiba = IchibaAPI()
    books = BooksAPI()
    travel = TravelAPI()
    auction = AuctionAPI()
    kobo = KoboAPI()
    gora = GoraAPI()
    recipe = RecipeAPI()
    other = OtherAPI()
