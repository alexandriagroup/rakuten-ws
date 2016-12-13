# coding: utf-8
from __future__ import unicode_literals
import base64

import requests
import zeep
import zeep.transports

from .compat import to_unicode


class ApiMethod(object):
    def __init__(self, name, alias=None, api_version=None):
        self.name = name
        self.alias = alias or name
        self.api_version = api_version


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


class BaseRmsClient(object):

    @property
    def esa_key(self):
        if hasattr(self, 'webservice_obj'):
            license_key = self.webservice_obj.license_key
            secret_service = self.webservice_obj.secret_service
            if license_key is None or secret_service is None:
                raise Exception("An 'license_key' and 'secret_service' must be provided")
            key = b"ESA " + base64.b64encode((secret_service + ":" + license_key).encode('utf-8'))
            return to_unicode(key)

    def __get__(self, webservice_obj, cls):
        if webservice_obj is not None:
            self.webservice_obj = webservice_obj
            return self
        return self.__class__


class RmsApi(object):

    @property
    def esa_key(self):
        if hasattr(self, 'client'):
            license_key = self.client.webservice_obj.license_key
            secret_service = self.client.webservice_obj.secret_service
            if license_key is None or secret_service is None:
                raise Exception("An 'license_key' and 'secret_service' must be provided")
            key = b"ESA " + base64.b64encode((secret_service + ":" + license_key).encode('utf-8'))
            return to_unicode(key)

    def __get__(self, client_instance, cls):
        if client_instance is not None:
            self.client = client_instance
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
        self.zeep_client = zeep.Client(wsdl=self.wsdl_url, transport=ZeepTransport())

    def __send_request(self, name, **proxy_kwargs):
        kwargs = {'arg0': self.user_auth_model}
        if proxy_kwargs:
            kwargs['arg1'] = kwargs
        return getattr(self.zeep_client.service, name)(**kwargs)

    def __getattr__(self, name):
        return lambda **proxy_kwargs: self.__send_request(name, **proxy_kwargs)


class RmsRestApi(RmsApi):

    def __init__(self, **kwargs):
        pass
        # session = requests.Session()

