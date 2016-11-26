# coding: utf-8
from __future__ import unicode_literals, division, absolute_import


import os
import sys

import mock
import pytest

from vcr import VCR


VCR_CASSETTE_DIR = os.path.join(os.path.dirname(__file__), 'cassettes')
VCR_RECORD_MODE = os.environ.get('VCR_RECORD_MODE', 'once')


vcr = VCR(
    cassette_library_dir=VCR_CASSETTE_DIR,
    record_mode=VCR_RECORD_MODE
)


def pytest_configure(config):
    # register the online marker
    config.addinivalue_line('markers',
                            'online: mark a test that goes online. VCR will automatically be used.')



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
        filter_query = []
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

def credentials():
    return {'application_id': os.environ['RAKUTEN_APP_ID']}


@pytest.fixture
def fake_credentials():
    return {'application_id': "fake_app_id_V877461Q206195"}
