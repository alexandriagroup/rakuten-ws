# coding: utf-8
from __future__ import unicode_literals
from .base import (RakutenAPIEndpoint, RakutenAPI, BaseWebService, RmsSoapApi,
                   RmsRestApi, WebServiceDescriptor, ApiMethod)


class IchibaAPI(RakutenAPI):
    item = RakutenAPIEndpoint(methods=[
        ApiMethod('search', api_version='20140222'),
        ApiMethod('ranking', api_version='20120927')]
    )
    genre = RakutenAPIEndpoint(
        methods=[ApiMethod('search', '20120723')]
    )
    tag = RakutenAPIEndpoint(methods=[
        ApiMethod('search', '20140222')]
    )
    product = RakutenAPIEndpoint(methods=[
        ApiMethod('search', '20140305')], 
        api_endpoint='Product'
    )


class BooksAPI(RakutenAPI):
    api_version = "20130522"
    total = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    book = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    cd = RakutenAPIEndpoint(name='CD', methods=[ApiMethod('search')])
    dvd = RakutenAPIEndpoint(name='DVD', methods=[ApiMethod('search')])
    foreign_book = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    magazine = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    game = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    software = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    genre = RakutenAPIEndpoint(methods=[ApiMethod('search'), ApiMethod('ranking')])


class TravelAPI(RakutenAPI):
    api_version = "20131024"
    hotel = RakutenAPIEndpoint(methods=[ApiMethod('simple_search', 'simple_hotel_search', api_version),
                                 ApiMethod('detail_search', 'hotel_detail_search', api_version),
                                 ApiMethod('search_vacant', 'vacant_hotel_search', api_version),
                                 ApiMethod('ranking', 'hotel_ranking', api_version),
                                 ApiMethod('get_chain_list', 'get_hotel_chain_list', api_version),
                                 ApiMethod('keyword_search', 'keyword_hotel_search', api_version)],
                                 api_endpoint="Travel")
    area = RakutenAPIEndpoint(methods=[ApiMethod('get_class', 'get_area_class')], 
                       api_endpoint="Travel")


class AuctionAPI(RakutenAPI):
    api_version = "20120927"
    genre_id = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    genre_keyword = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    item = RakutenAPIEndpoint(methods=[ApiMethod('search')])
    item_code = RakutenAPIEndpoint(methods=[ApiMethod('search')])


class KoboAPI(RakutenAPI):
    api_version = "20131010"
    genre = RakutenAPIEndpoint(methods=[ApiMethod('search', 'genre_search')], 
                        api_endpoint="Kobo")
    ebook = RakutenAPIEndpoint(methods=[ApiMethod('search', 'ebook_search')], 
                        api_endpoint="Kobo")


class GoraAPI(RakutenAPI):
    api_version = "20131113"
    golf = RakutenAPIEndpoint(methods=[ApiMethod('search', 'gora_golf_course_search'),
                                       ApiMethod('detail', 'gora_golf_course_detail')],
                              api_endpoint="Gora")
    plan = RakutenAPIEndpoint(methods=[ApiMethod('search', 'gora_plan_search')], 
                              api_endpoint="Gora")


class RecipeAPI(RakutenAPI):
    api_version = "20121121"
    category = RakutenAPIEndpoint(methods=[ApiMethod('ranking', 'category_ranking'),
                                           ApiMethod('list', 'category_list')], 
                                  api_endpoint="Recipe")


class OtherAPI(RakutenAPI):
    api_version = "20131205"
    high_comission_shop = RakutenAPIEndpoint(methods=[ApiMethod('list')], 
                                             api_endpoint="HighComissionShop")


class RmsOrderAPI(RmsSoapApi):
    wsdl_url = "https://api.rms.rakuten.co.jp/es/1.0/order/ws?WSDL"


class RmsItemAPI(RmsRestApi):
    wsdl_url = "https://api.rms.rakuten.co.jp/es/1.0/order/ws?WSDL"


class RmsClient(WebServiceDescriptor):
    order = RmsOrderAPI()
    item = RmsItemAPI()


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
