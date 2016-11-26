# -*- coding: utf-8 -*-
from furl import furl
from requests import Session


from .utils import camelize, camelize_dict, sorted_dict


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
        format_version = self.endpoint.api_obj.webservice_obj.format_version

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


class RakutenAPI(object):
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

    def __get__(self, webservice_obj, cls):
        if webservice_obj is not None:
            self.webservice_obj = webservice_obj
            self.api_url = self.webservice_obj.api_url
            return self
        return self.__class__


class BaseWebservice(object):

    def __new__(cls, *args, **kwargs):
        instance = super(BaseWebservice, cls).__new__(cls)
        for name, attr in sorted(list(cls.__dict__.items())):
            if isinstance(attr, RakutenAPI) \
                    and getattr(attr, 'name', None) is None:
                setattr(attr, 'name', name)
        return instance

    api_url = None
    api_version = None
    format_version = 2

    def __init__(self, application_id, **kwargs):
        for key in dict(kwargs).keys():
            setattr(self, key, kwargs[key])
        self.application_id = application_id
        self.session = Session()
