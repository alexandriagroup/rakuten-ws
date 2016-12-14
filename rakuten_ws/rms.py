# coding: utf-8
from __future__ import unicode_literals

from furl import furl

from .utils import camelize


import base64

import requests
import zeep
import zeep.transports

from .compat import to_unicode


class RmsServiceClient(object):
    def __get__(self, service, cls):
        if service is not None:
            self.service = service
            return self
        return self.__class__


class ZeepTransport(zeep.transports.Transport):

    def create_session(self):
        self.http_headers = requests.Session().headers.copy()
        return super(ZeepTransport, self).create_session()

    # Patch Zeep methods to send custom headers
    def get(self, address, params, headers):
        headers.update(self.http_headers.copy())
        return super(ZeepTransport, self).get(address, params, headers)

    def post(self, address, params, headers):
        headers.update(self.http_headers.copy())
        return super(ZeepTransport, self).post(address, params, headers)


class ZeepClient(RmsServiceClient):
    wsdl = None

    def __init__(self):
        self.zeep_client = zeep.Client(wsdl=self.wsdl, transport=ZeepTransport())

    def __send_request(self, name, **proxy_kwargs):
        kwargs = {'arg0': self.service.soap_user_auth_model}
        if proxy_kwargs:
            kwargs['arg1'] = kwargs
        return getattr(self.zeep_client.service, name)(**kwargs)

    def __getattr__(self, name):
        return lambda **proxy_kwargs: self.__send_request(name, **proxy_kwargs)


class SoapClient(RmsServiceClient):

    def __init__(self, **kwargs):
        pass


class RestMethod(object):

    def __init__(self, name=None, http_method="GET"):
        self.name = name
        self.http_method = http_method
        self.client = None

    def build_url(self, *args, **kwargs):
        api_request = furl(self.endpoint.api_obj.api_url)
        api_endpoint = self.endpoint.api_endpoint
        method_endpoint = camelize(self.method_name)

        api_request.path.segments.append(api_endpoint)
        api_request.path.segments.append(method_endpoint)
        api_request.path.segments.append(self.api_version)
        api_request.path.normalize()

        return "url"

    def build_request(self, *args, **kwargs):
        # creating new instance of url request
        return "<xml></xml>"

    def __call__(self, *args, **kwargs):
        pass

    def __get__(self, client, cls):
        if client is not None:
            self.client = client
            return self
        return self.__class__


class RestClient(RmsServiceClient):
    api_url = "https://api.rms.rakuten.co.jp/es"

    def __new__(cls, *args, **kwargs):
        instance = super(RestClient, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RestMethod):
                if getattr(attr, 'name', None) is None:
                    setattr(attr, 'name', name)
        return instance

    def __init__(self, name=None):
        self.name = name
        self.service = None


class BaseRmsService(object):
    def __new__(cls, *args, **kwargs):
        instance = super(BaseRmsService, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RmsServiceClient):
                if getattr(attr, 'name', None) is None:
                    setattr(attr, 'name', name)
        return instance

    @property
    def esa_key(self):
        license_key = self.webservice_obj.license_key
        secret_service = self.webservice_obj.secret_service
        if license_key is None or secret_service is None:
            raise Exception("An 'license_key' and 'secret_service' must be provided")
        key = b"ESA " + base64.b64encode((secret_service + ":" + license_key).encode('utf-8'))
        return to_unicode(key)

    @property
    def shop_url(self):
        return self.webservice_obj.shop_url or ""

    @property
    def soap_user_auth_model(self):
        return {
            "authKey": self.esa_key,
            "shopUrl": self.shop_url,
            "userName": ""
        }

    def __get__(self, webservice_obj, cls):
        if webservice_obj is not None:
            self.webservice_obj = webservice_obj
            return self
        return self.__class__
