# -*- coding: utf-8 -*-
from .base import RakutenAPIEndpoint, RakutenAPI, BaseWebservice


class IchibaAPI(RakutenAPI):
    item = RakutenAPIEndpoint(methods=['search', 'ranking'])
    genre = RakutenAPIEndpoint(methods=['search'])
    tag = RakutenAPIEndpoint(methods=['search'])
    product = RakutenAPIEndpoint(methods=['search'], api_endpoint="Product")


class RakutenWebservice(BaseWebservice):
    api_url = "https://app.rakuten.co.jp/services/api"
    api_version = "20140222"

    ichiba = IchibaAPI()
