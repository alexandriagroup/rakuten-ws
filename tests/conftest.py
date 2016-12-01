# coding: utf-8
from __future__ import unicode_literals

import re
import os
import sys

import mock
import pytest

from vcr import VCR


VCR_CASSETTE_DIR = os.path.join(os.path.dirname(__file__), 'cassettes')
VCR_RECORD_MODE = os.environ.get('VCR_RECORD_MODE', 'once')


def before_record_cb(request):
    if request.body:
        request.body = re.sub('<authKey>.+</authKey>', '<authKey>XXXXXX</authKey>', request.body.decode('utf-8'))
    return request


vcr = VCR(
    cassette_library_dir=VCR_CASSETTE_DIR,
    record_mode=VCR_RECORD_MODE,
    before_record=before_record_cb,
)


def pytest_configure(config):
    # register the online marker
    config.addinivalue_line('markers',
                            'online: mark a test that goes online. VCR will automatically be used.')


def pytest_runtest_setup(item):
    # Add the online marker to tests that will go online
    if item.get_marker('online'):
        item.fixturenames.append('use_vcr')
    else:
        item.fixturenames.append('no_requests')


@pytest.yield_fixture()
def use_vcr(request, monkeypatch):
    """
    This fixture is applied automatically to any test using the `online` mark. It will record and playback network
    sessions using VCR.
    The record mode of VCR can be set using the VCR_RECORD_MODE environment variable when running tests.
    """
    if VCR_RECORD_MODE == 'off':
        yield None
    else:
        cassette_name = ""
        if request.module is not None:
            cassette_name += request.module.__name__.split('tests.')[-1] + '.'
        if request.cls is not None:
            cassette_name += request.cls.__name__ + '.'
        cassette_name += request.function.__name__ + '.yaml'

        cassette_path = os.path.join(VCR_CASSETTE_DIR, cassette_name)

        filter_query = [('applicationId', 'XXXXXX')]
        filter_headers = []
        filter_post = []

        online = True
        if vcr.record_mode == 'none':
            online = False
        elif vcr.record_mode == 'once':
            online = not os.path.exists(cassette_path)
        # If we are going online, check the credentials
        if online:
            if os.environ.get("RAKUTEN_APP_ID", None) is None:
                pytest.skip('need credentials to run this test')

        with vcr.use_cassette(path=cassette_path,
                              filter_query_parameters=filter_query,
                              filter_headers=filter_headers,
                              filter_post_data_parameters=filter_post) as cassette:
            yield cassette


@pytest.fixture()
def no_requests(monkeypatch):
    online_funcs = [
        'requests.sessions.Session.request',
    ]

    if sys.version_info[0] == 2:
        online_funcs.extend(['httplib.HTTPConnection.request',
                             'httplib.HTTPSConnection.request'])
    else:
        online_funcs.extend(['http.client.HTTPConnection.request',
                             'http.client.HTTPSConnection.request'])

    for func in online_funcs:
        monkeypatch.setattr(func, mock.Mock(side_effect=Exception('Online tests should use @pytest.mark.online')))


@pytest.fixture
def credentials():
    return {
        'application_id': os.environ.get('RAKUTEN_APP_ID', '<RAKUTEN_APP_ID>'),
        'license_key': os.environ.get('RMS_LICENSE_KEY', '<RMS_LICENSE_KEY>'),
        'secret_service': os.environ.get('RMS_SECRET_SERVICE', '<RMS_SECRET_SERVICE>'),
    }


@pytest.fixture
def fake_credentials():
    return {
        'application_id': '<RAKUTEN_APP_ID>',
        'license_key': '<RMS_LICENSE_KEY>',
        'secret_service': '<RMS_SECRET_SERVICE>',
    }
