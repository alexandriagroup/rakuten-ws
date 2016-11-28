# coding: utf-8
from __future__ import unicode_literals
import base64

import requests
import zeep
import zeep.transports

from furl import furl

from .utils import camelize, camelize_dict, sorted_dict
from .compat import to_unicode


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


class WebServiceDescriptor(object):
    def __get__(self, webservice_obj, cls):
        if webservice_obj is not None:
            self.webservice_obj = webservice_obj
            return self
        return self.__class__


class RakutenAPIRequest(object):

    def __init__(self, endpoint, method_name, **kwargs):
        self.endpoint = endpoint
        self.method_name = method_name
        for key in dict(kwargs).keys():
            setattr(self, key, kwargs[key])

    def build_url(self, *args, **kwargs):
        # creating new instance of url request
        api_request = furl(self.endpoint.api_obj.api_url)
        api_endpoint = self.endpoint.api_endpoint
        method_endpoint = camelize(self.method_name)

        api_request.path.segments.append(api_endpoint)
        api_request.path.segments.append(method_endpoint)
        api_request.path.segments.append(self.endpoint.api_obj.api_version)
        api_request.path.normalize()

        application_id = self.endpoint.api_obj.webservice_obj.application_id
        format_version = self.endpoint.api_obj.format_version

        request_params = {
            'applicationId': application_id,
            'formatVersion': format_version
        }

        request_params.update(camelize_dict(kwargs))
        api_request.add(sorted_dict(request_params))
        return api_request.url

    def __call__(self, *args, **kwargs):
        url = self.build_url(*args, **kwargs)
        return self.endpoint.api_obj.webservice_obj.session.get(url).json()


class RakutenAPIEndpoint(object):

    def __new__(cls, *args, **kwargs):
        instance = super(RakutenAPIEndpoint, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RakutenAPIEndpoint) \
                    and getattr(attr, 'name', None) is None:
                setattr(attr, 'name', name)
        return instance

    def __init__(self, name=None, methods=None, api_endpoint=None, **kwargs):
        self.api_obj = None
        self.name = name
        self.methods = methods or []
        self.api_endpoint = api_endpoint
        for key in dict(kwargs).keys():
            setattr(self, key, kwargs[key])

    def __get__(self, api_obj, cls):
        if api_obj is not None:
            self.api_obj = api_obj
            if getattr(self, 'api_endpoint', None) is None:
                self.api_endpoint = \
                    camelize("%s_%s" % (self.api_obj.name, self.name))
            for name in self.methods:
                setattr(self, name, RakutenAPIRequest(self, name))
            return self
        return self.__class__


class RakutenAPI(WebServiceDescriptor):
    api_url = "https://app.rakuten.co.jp/services/api"
    format_version = 2

    def __new__(cls, *args, **kwargs):
        instance = super(RakutenAPI, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RakutenAPIEndpoint):
                if getattr(attr, 'name', None) is None:
                    setattr(attr, 'name', name)
        return instance

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.webservice_obj = None
        for key in dict(kwargs).keys():
            setattr(self, key, kwargs[key])


class BaseWebService(object):

    def __new__(cls, *args, **kwargs):
        instance = super(BaseWebService, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RakutenAPI) \
                    and getattr(attr, 'name', None) is None:
                setattr(attr, 'name', name)
        return instance

    def __init__(self, application_id, **kwargs):
        for key in dict(kwargs).keys():
            setattr(self, key, kwargs[key])
        self.application_id = application_id
        self.session = requests.Session()


class RmsApi(object):

    @property
    def esa_key(self):
        key = b"ESA " + base64.b64encode(("SECRET_SERVICE" + ":" + "LICENSE_KEY").encode('utf-8'))
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
        session = requests.Session()
        session.headers['Authorization'] = self.esa_key
