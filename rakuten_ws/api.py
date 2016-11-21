# -*- coding: utf-8 -*-
from .base import RakutenAPIEndpoint, RakutenAPI, BaseWebservice


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


class RakutenWebservice(BaseWebservice):
    api_url = "https://app.rakuten.co.jp/services/api"

    ichiba = IchibaAPI()
    books = BooksAPI()
