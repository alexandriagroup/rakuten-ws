# coding: utf-8
from __future__ import unicode_literals
from .api import ApiEndpoint, ApiService, BaseWebService, ApiMethod

from .rms import BaseRmsService, ZeepClient


class IchibaAPI(ApiService):
    item = ApiEndpoint(ApiMethod('search', api_version='20140222'),
                       ApiMethod('ranking', api_version='20120927'))
    genre = ApiEndpoint(ApiMethod('search', api_version='20120723'))
    tag = ApiEndpoint(ApiMethod('search', api_version='20140222'))
    product = ApiEndpoint(ApiMethod('search', api_version='20140305'), api_endpoint='Product')


class BooksAPI(ApiService):
    api_version = "20130522"

    total = ApiEndpoint(ApiMethod('search'))
    book = ApiEndpoint(ApiMethod('search'))
    cd = ApiEndpoint(ApiMethod('search'), name='CD', )
    dvd = ApiEndpoint(ApiMethod('search'), name='DVD')
    foreign_book = ApiEndpoint(ApiMethod('search'))
    magazine = ApiEndpoint(ApiMethod('search'))
    game = ApiEndpoint(ApiMethod('search'))
    software = ApiEndpoint(ApiMethod('search'))
    genre = ApiEndpoint(ApiMethod('search'),
                        ApiMethod('ranking', api_version="20121128"))


class TravelAPI(ApiService):
    api_version = "20131024"

    hotel = ApiEndpoint(ApiMethod('simple_search', 'simple_hotel_search'),
                        ApiMethod('detail_search', 'hotel_detail_search'),
                        ApiMethod('search_vacant', 'vacant_hotel_search'),
                        ApiMethod('ranking', 'hotel_ranking'),
                        ApiMethod('get_chain_list', 'get_hotel_chain_list'),
                        ApiMethod('keyword_search', 'keyword_hotel_search'),
                        api_endpoint="Travel")
    area = ApiEndpoint(ApiMethod('get_class', 'get_area_class'), api_endpoint="Travel")


class AuctionAPI(ApiService):
    api_version = "20120927"

    genre_id = ApiEndpoint(ApiMethod('search'))
    genre_keyword = ApiEndpoint(ApiMethod('search'))
    item = ApiEndpoint(ApiMethod('search'))
    item_code = ApiEndpoint(ApiMethod('search'))


class KoboAPI(ApiService):
    api_version = "20131010"

    genre = ApiEndpoint(ApiMethod('search', 'genre_search'), api_endpoint="Kobo")
    ebook = ApiEndpoint(ApiMethod('search', 'ebook_search'), api_endpoint="Kobo")


class GoraAPI(ApiService):
    api_version = "20131113"

    golf = ApiEndpoint(ApiMethod('search', 'gora_golf_course_search'),
                       ApiMethod('detail', 'gora_golf_course_detail'),
                       api_endpoint="Gora")
    plan = ApiEndpoint(ApiMethod('search', 'gora_plan_search'),
                       api_endpoint="Gora")


class RecipeAPI(ApiService):
    api_version = "20121121"

    category = ApiEndpoint(ApiMethod('ranking', 'category_ranking'),
                           ApiMethod('list', 'category_list'),
                           api_endpoint="Recipe")


class OtherAPI(ApiService):
    api_version = "20131205"

    high_comission_shop = ApiEndpoint(ApiMethod('list'), api_endpoint="HighComissionShop")


class RmsOrderAPI(ZeepClient):
    wsdl = "https://api.rms.rakuten.co.jp/es/1.0/order/ws?WSDL"
class RmsService(BaseRmsService):
    # item = RmsRestEndpoint(RmsRestMethod('get', type='GET'),
    #                        RmsRestMethod('insert', type='POST'),
    #                        RmsRestMethod('update', type='POST'),
    #                        RmsRestMethod('delete', type='POST'),
    #                        RmsRestMethod('search', type='GET'))
    # items = RmsRestEndpoint(RmsRestMethod('update', type='POST'))
    order = RmsOrderAPI()


class RakutenWebService(BaseWebService):

    rms = RmsService()

    ichiba = IchibaAPI()
    books = BooksAPI()
    travel = TravelAPI()
    auction = AuctionAPI()
    kobo = KoboAPI()
    gora = GoraAPI()
    recipe = RecipeAPI()
    other = OtherAPI()
