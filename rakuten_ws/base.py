# -*- coding: utf-8 -*-
from furl import furl
from requests import Session


class RakutenWebservice(object):

    def __init__(self, application_id, api_root_url=None):
        self.api_root_url = furl(api_root_url or "https://app.rakuten.co.jp/services/api")
        self.application_id = application_id
        self.session = Session()


class RakutenAPI(object):
    pass


class RakutenEndpoint(object):
    pass
