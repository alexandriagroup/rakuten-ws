# -*- coding: utf-8 -*-
import base64

import requests
import zeep
import zeep.transports


SECRET_SERVICE = ""
LICENSE_KEY = ""


class Transport(zeep.transports.Transport):

    def create_session(self):
        self.http_headers = requests.Session().headers.copy()
        return super(Transport, self).create_session()

    # Patch Zeep methods to send custom headers
    def get(self, address, params, headers):
        headers.update(self.http_headers.copy())
        return super(Transport, self).get(address, params, headers)

    def post(self, address, params, headers):
        headers.update(self.http_headers.copy())
        return super(Transport, self).post(address, params, headers)


class RmsApi(object):

    @property
    def esa_key(self):
        return "ESA " + base64.b64encode(SECRET_SERVICE + ":" + LICENSE_KEY)

    def __get__(self, client_instance, cls):
        if client_instance is not None:
            self.client_instance = client_instance
            return self
        return self.__class__


class RmsSoapApi(RmsApi):
    wsdl_url = None

    @property
    def user_auth_model(self):
        return {
            "authKey": self.esa_key,
            "shopUrl": "",
            "userName": ""
        }

    def __init__(self, **kwargs):
        self.zeep_client = zeep.Client(wsdl=self.wsdl_url, transport=Transport())

    def __send_request(self, name, **proxy_kwargs):
        kwargs = {'arg0': self.user_auth_model}
        if proxy_kwargs:
            kwargs['arg1'] = kwargs
        return getattr(self.zeep_client.service, name)(**kwargs)

    def __getattr__(self, name):
        return lambda **proxy_kwargs: self.__send_request(name, **proxy_kwargs)


class RmsRestApi(RmsApi):

    def __init__(self, **kwargs):
        session = requests.Session()
        session.headers['Authorization'] = self.esa_key


class RmsOrderAPI(RmsSoapApi):
    wsdl_url = "https://api.rms.rakuten.co.jp/es/1.0/order/ws?WSDL"


class RmsClient(object):
    order = RmsOrderAPI()
