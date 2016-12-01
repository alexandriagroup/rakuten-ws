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
