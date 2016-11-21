# coding: utf-8
from __future__ import unicode_literals, print_function

import os

import pytest


ONLINE_TEST_ENABLED = os.environ.get("RAKUTEN_APP_ID", None) is not None


@pytest.fixture(params=[pytest.mark.skipif(not ONLINE_TEST_ENABLED,
                        reason='need credentials')('parameter')])
def credentials():
    return {'application_id': os.environ['RAKUTEN_APP_ID']}


@pytest.fixture
def fake_credentials():
    return {'application_id': "fake_app_id_V877461Q206195"}
