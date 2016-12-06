# coding: utf-8
from __future__ import unicode_literals
from .base import RakutenAPIEndpoint, RakutenAPI, BaseWebService, RmsSoapApi, RmsRestApi, WebServiceDescriptor


class IchibaAPI(RakutenAPI):
    api_version = "20140222"
    item = RakutenAPIEndpoint(methods=['search', 'ranking'])
    genre = RakutenAPIEndpoint(methods=['search'])
    tag = RakutenAPIEndpoint(methods=['search'])
    product = RakutenAPIEndpoint(methods=['search'], api_endpoint="Product")


class BooksAPI(RakutenAPI):
    api_version = "20130522"
    total = RakutenAPIEndpoint(methods=['search'])
    book = RakutenAPIEndpoint(methods=['search'])
    cd = RakutenAPIEndpoint(name='CD', methods=['search'])
    dvd = RakutenAPIEndpoint(name='DVD', methods=['search'])
    foreign_book = RakutenAPIEndpoint(methods=['search'])
    magazine = RakutenAPIEndpoint(methods=['search'])
    game = RakutenAPIEndpoint(methods=['search'])
    software = RakutenAPIEndpoint(methods=['search'])
    genre = RakutenAPIEndpoint(methods=['search'])


class TravelAPI(RakutenAPI):
    api_version = "20131024"
    hotel = RakutenAPIEndpoint(methods={'simple_search': 'simple_hotel_search',
                                        'detail_search': 'hotel_detail_search',
                                        'search_vacant': 'vacant_hotel_search',
                                        'ranking': 'hotel_ranking',
                                        'get_chain_list': 'get_hotel_chain_list',
                                        'keyword_search': 'keyword_hotel_search'}, api_endpoint="Travel")
    area = RakutenAPIEndpoint(methods={'get_class': 'get_area_class'}, api_endpoint="Travel")


class AuctionAPI(RakutenAPI):
    api_version = "20120927"
    genre_id = RakutenAPIEndpoint(methods=['search'])
    genre_keyword = RakutenAPIEndpoint(methods=['search'])
    item = RakutenAPIEndpoint(methods=['search'])
    item_code = RakutenAPIEndpoint(methods=['search'])


class KoboAPI(RakutenAPI):
    api_version = "20131010"
    genre = RakutenAPIEndpoint(methods={'search': 'genre_search'}, api_endpoint="Kobo")
    ebook = RakutenAPIEndpoint(methods={'search': 'ebook_search'}, api_endpoint="Kobo")


class GoraAPI(RakutenAPI):
    api_version = "20131113"
    golf = RakutenAPIEndpoint(methods={'search': 'gora_golf_course_search',
                                       'detail': 'gora_golf_course_detail'}, api_endpoint="Gora")
    plan = RakutenAPIEndpoint(methods={'search': 'gora_plan_search'}, api_endpoint="Gora")


class RecipeAPI(RakutenAPI):
    api_version = "20121121"
    category = RakutenAPIEndpoint(methods={'ranking': 'category_ranking',
                                           'list': 'category_list'}, api_endpoint="Recipe")


class OtherAPI(RakutenAPI):
    api_version = "20131205"
    high_comission_shop = RakutenAPIEndpoint(methods=['list'], api_endpoint="HighComissionShop")


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
