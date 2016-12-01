# coding: utf-8
from __future__ import unicode_literals
import base64

import requests
import zeep
import zeep.transports

from furl import furl

from .utils import camelize, camelize_dict, sorted_dict, clean_python_variable_name
from .compat import to_unicode, iteritems


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

    @property
    def application_id(self, *args, **kwargs):
        app_id = self.endpoint.api_obj.webservice_obj.application_id
        if app_id is None:
            raise Exception("An 'application_id' must be provided")
        return app_id

    def build_url(self, *args, **kwargs):
        # creating new instance of url request
        api_request = furl(self.endpoint.api_obj.api_url)
        api_endpoint = self.endpoint.api_endpoint
        method_endpoint = camelize(self.method_name)

        api_request.path.segments.append(api_endpoint)
        api_request.path.segments.append(method_endpoint)
        api_request.path.segments.append(self.endpoint.api_obj.api_version)
        api_request.path.normalize()

        request_params = {
            'applicationId': self.application_id,
            'formatVersion': self.endpoint.api_obj.format_version
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
            if isinstance(self.methods, dict):
                methods = dict((clean_python_variable_name(key), name) for key, name in iteritems(self.methods))
            elif isinstance(self.methods, (list, tuple)):
                methods = dict((clean_python_variable_name(name), name) for name in self.methods)
            else:
                raise Exception("'methods' parameter must be a list or a dictionary")
            for key, name in iteritems(methods):
                setattr(self, key, RakutenAPIRequest(self, name))
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

    def __init__(self, application_id=None, license_key=None, secret_service=None):
        self.application_id = application_id
        self.license_key = license_key
        self.secret_service = secret_service
        self.session = requests.Session()


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
