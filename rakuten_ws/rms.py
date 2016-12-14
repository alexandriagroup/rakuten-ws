# coding: utf-8
from __future__ import unicode_literals
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

    def __init__(self, **kwargs):
        pass


class BaseRmsService(object):

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

    def __init__(self, **kwargs):
        pass
        # session = requests.Session()

    def __get__(self, webservice_obj, cls):
        if webservice_obj is not None:
            self.webservice_obj = webservice_obj
            return self
        return self.__class__
