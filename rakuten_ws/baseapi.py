# coding: utf-8
from __future__ import unicode_literals

import requests

from furl import furl

from .utils import camelize, camelize_dict, sorted_dict, clean_python_variable_name


class ApiMethod(object):
    def __init__(self, name, alias=None, api_version=None):
        self.name = name
        self.alias = alias or name
        self.api_version = api_version


class ApiResponse(dict):
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.response = self.session.get(self.url).json()
        super(ApiResponse, self).__init__(self.response)

    def pages(self):
        yield self.response
        page_number = int(self.response['page']) + 1
        while page_number <= self.response['pageCount']:
            api_request = furl(self.url)
            api_request.args['page'] = page_number
            page_number += 1
            yield self.session.get(api_request.url).json()


class ApiRequest(object):

    def __init__(self, endpoint, method):
        self.endpoint = endpoint
        self.method = method

    @property
    def application_id(self, *args, **kwargs):
        app_id = self.endpoint.service.webservice.application_id
        if app_id is None:
            raise Exception("An 'application_id' must be provided")
        return app_id

    def build_url(self, *args, **kwargs):
        # creating new instance of url request
        api_request = furl(self.endpoint.service.api_url)
        api_endpoint = self.endpoint.api_endpoint
        method_endpoint = camelize(self.method.alias)
        api_version = self.method.api_version or self.endpoint.api_version or self.endpoint.service.api_version

        api_request.path.segments.append(api_endpoint)
        api_request.path.segments.append(method_endpoint)
        api_request.path.segments.append(api_version)
        api_request.path.normalize()

        request_params = {
            'applicationId': self.application_id,
            'formatVersion': self.endpoint.service.format_version,
        }
        if 'page' in kwargs:
            request_params.update(page=kwargs['page'])

        request_params.update(camelize_dict(kwargs))
        api_request.add(sorted_dict(request_params))
        return api_request.url

    def __call__(self, *args, **kwargs):
        url = self.build_url(*args, **kwargs)
        session = self.endpoint.service.webservice.session
        return ApiResponse(session, url)


class ApiEndpoint(object):
    api_version = None

    def __init__(self, *methods, **kwargs):
        self.service = None
        self.name = kwargs.get('name', None)
        self.api_endpoint = kwargs.get('api_endpoint', None)

        for method in methods:
            method_name = clean_python_variable_name(method.name)
            setattr(self, method_name, ApiRequest(self, method))

    def __get__(self, service, cls):
        if service is not None:
            self.service = service
            if getattr(self, 'api_endpoint', None) is None:
                self.api_endpoint = camelize("%s_%s" % (self.service.name, self.name))
            return self
        return self.__class__


class ApiService(object):
    api_url = "https://app.rakuten.co.jp/services/api"
    format_version = 2

    def __new__(cls, *args, **kwargs):
        instance = super(ApiService, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, ApiEndpoint):
                if getattr(attr, 'name', None) is None:
                    setattr(attr, 'name', name)
        return instance

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.webservice = None

    def __get__(self, webservice, cls):
        if webservice is not None:
            self.webservice = webservice
            return self
        return self.__class__


class BaseWebService(object):

    def __new__(cls, *args, **kwargs):
        instance = super(BaseWebService, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, ApiService) \
                    and getattr(attr, 'name', None) is None:
                setattr(attr, 'name', name)
        return instance

    def __init__(self, application_id=None, license_key=None, secret_service=None, shop_url=None):
        self.application_id = application_id
        self.license_key = license_key
        self.secret_service = secret_service
        self.shop_url = shop_url
        self.session = requests.Session()
        self.session.headers = {"User-Agent": self.session.headers['User-Agent']}
