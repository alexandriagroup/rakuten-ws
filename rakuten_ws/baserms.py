# coding: utf-8
from __future__ import unicode_literals

import re
import json

from furl import furl

from collections import OrderedDict
from .utils import camelize

import warnings

import base64

import zeep
import zeep.transports

from lxml import etree
from requests import Request

from rakuten_ws.utils import xml2dict, dict2xml, unflatten_dict, sorted_dict, flatten_dict

from .utils import camelize_dict, PrettyStringRepr, load_file
from .compat import to_unicode


class RmsServiceClient(object):
    def __get__(self, service, cls):
        if service is not None:
            self.service = service
            return self
        return self.__class__


class RMSInvalidResponse(Exception):
    pass


class ZeepClient(RmsServiceClient):
    wsdl = None

    def __init__(self):
        self.zeep_client = zeep.Client(wsdl=self.wsdl, transport=zeep.transports.Transport())

    def __send_request(self, name, **proxy_kwargs):
        address = self.zeep_client.service._binding_options['address']
        arg0 = self.service.soap_user_auth_model
        method = getattr(self.zeep_client.service, name)

        if address.endswith('inventory/ws'):
            response = method(arg0, proxy_kwargs)
        # We assume the potential future methods will have the same form as the
        # order method (arg0, arg1...)
        else:
            kwargs = {'arg0': arg0}
            if proxy_kwargs:
                kwargs['arg1'] = proxy_kwargs
            response = method(**kwargs)
        return response

    def __getattr__(self, name):
        return lambda **proxy_kwargs: self.__send_request(name, **proxy_kwargs)


class RestMethodResult(OrderedDict):
    def __init__(self, method, response):
        self.method = method
        self.response = response
        self.request = response.request
        self.status, result_data = self.parse_result(response)
        super(RestMethodResult, self).__init__(result_data)

    def parse_result(self, response):
        xml = etree.fromstring(response.content)
        _status = xml.xpath('//status')
        _result = xml.xpath('//%s' % self.method.result_xml_key)
        result_data = {}
        if _status:
            status = xml2dict(etree.tostring(_status[0]))
        else:
            raise RMSInvalidResponse(response.text)
        if _result:
            result_data = xml2dict(etree.tostring(_result[0]))
        return status, result_data

    @property
    def xml(self):
        return PrettyStringRepr(self.response.text)

    @property
    def json(self):
        data = {'status': self.status, 'result': self}
        return PrettyStringRepr(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                           indent=4, separators=(',', ': ')))

    def __repr__(self):
        return "<RestMethodResult [%s]>" % self.status.get('systemStatus', 'Error')


class RestMethod(object):

    def __init__(self, name=None, http_method="GET", params=[], custom_headers={}, form_data=None, root_xml_key=None):
        self.name = name
        self.http_method = http_method
        self.custom_headers = custom_headers
        self.params = params
        self.client = None
        self.form_data = form_data
        self._root_xml_key = root_xml_key

    @property
    def root_xml_key(self):
        if self._root_xml_key:
            return camelize(self._root_xml_key, False)
        else:
            return camelize("%s_%s" % (self.client.name, '_'.join(self.name.split('/'))), False)

    @property
    def result_xml_key(self):
        return "%sResult" % self.root_xml_key

    @property
    def request_xml_key(self):
        return camelize("%sRequest" % self.root_xml_key, False)

    def prepare_xml_post(self, params):
        camelcase_params = camelize_dict(params)
        if self.params:
            def key(x):
                k = re.sub('.@\d+.', '.', x[0])
                try:
                    return self.params.index(k)
                except:
                    warnings.warn(
                        "Given invalid parameter '%s'." % k,
                        SyntaxWarning
                    )
                    return len(self.params) + 1

            sorted_params = unflatten_dict(sorted_dict(flatten_dict(camelcase_params), key=key))
        else:
            sorted_params = camelcase_params
        return dict2xml({self.request_xml_key: sorted_params}, root="request") + "\n"

    def prepare_request(self, params={}):
        api_request = furl(self.client.api_url)
        api_request.path.segments.append(self.client.api_version)
        api_request.path.segments.append(self.client.api_endpoint or self.client.name)
        api_request.path.segments.extend(self.name.split('/'))
        api_request.path.normalize()

        headers = self.client.service.webservice.session.headers.copy()
        headers['Authorization'] = self.client.service.esa_key
        if self.custom_headers:
            headers.update(self.custom_headers)

        filename = params.pop('filename', None)

        if self.http_method == "POST":
            data = self.prepare_xml_post(params)
            if filename:
                fileobj, mimetype = load_file(filename)
                files = {'xml': (None, data), 'file': ('filename', fileobj, mimetype)}
                req = Request(self.http_method, api_request.url, files=files, headers=headers)
            else:
                req = Request(self.http_method, api_request.url, data=data, headers=headers)
        else:
            req = Request(self.http_method, api_request.url, headers=headers, params=camelize_dict(params))

        prepped_request = req.prepare()
        return prepped_request

    def __call__(self, *args, **kwargs):
        raise_for_status = kwargs.pop('raise_for_status', not self.client.service.webservice.debug)
        prepped_request = self.prepare_request(kwargs)
        response = self.client.service.webservice.session.send(prepped_request)
        if raise_for_status:
            response.raise_for_status()
        return RestMethodResult(self, response)

    def __get__(self, client, cls):
        if client is not None:
            self.client = client
            return self
        return self.__class__


class RestClient(RmsServiceClient):
    api_url = "https://api.rms.rakuten.co.jp/es"
    api_endpoint = None
    api_version = '1.0'

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
        license_key = self.webservice.license_key
        secret_service = self.webservice.secret_service
        if license_key is None or secret_service is None:
            raise Exception("A 'license_key' and 'secret_service' must be provided")
        key = b"ESA " + base64.b64encode((secret_service + ":" + license_key).encode('utf-8'))
        return to_unicode(key)

    @property
    def shop_url(self):
        return self.webservice.shop_url or ""

    @property
    def soap_user_auth_model(self):
        return {
            "authKey": self.esa_key,
            "shopUrl": self.shop_url,
            "userName": ""
        }

    def __get__(self, webservice, cls):
        if webservice is not None:
            self.webservice = webservice
            return self
        return self.__class__
