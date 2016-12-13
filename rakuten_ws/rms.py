# coding: utf-8
from __future__ import unicode_literals
import base64

import requests
import zeep
import zeep.transports

from .compat import to_unicode


class RmsServiceDescriptor(object):
    def __get__(self, rms_service, cls):
        if rms_service is not None:
            self.rms_service = rms_service
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


class ZeepClient(RmsServiceDescriptor):

    def __init__(self, wsdl):
        self.zeep_client = zeep.Client(wsdl=wsdl, transport=ZeepTransport())

    def __send_request(self, name, **proxy_kwargs):
        kwargs = {'arg0': self.rms_service.soap_user_auth_model}
        if proxy_kwargs:
            kwargs['arg1'] = kwargs
        return getattr(self.zeep_client.service, name)(**kwargs)

    def __getattr__(self, name):
        return lambda **proxy_kwargs: self.__send_request(name, **proxy_kwargs)


class SoapClient(RmsServiceDescriptor):

    def __init__(self, **kwargs):
        pass


class RestClient(RmsServiceDescriptor):

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
    def soap_user_auth_model(self):
        return {
            "authKey": self.esa_key,
            "shopUrl": "",
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
