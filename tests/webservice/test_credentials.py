# coding: utf-8
from __future__ import unicode_literals

import pytest

from rakuten_ws import RakutenWebService

from .. import assert_raises


def test_no_application():
    ws = RakutenWebService()
    with assert_raises(Exception, "An 'application_id' must be provided"):
        ws.ichiba.item.search(item_code="book:17924463")


def test_no_rms_keys():
    ws = RakutenWebService()
    with assert_raises(Exception, "A 'license_key' and 'secret_service' must be provided"):
        ws.rms.order.getRequestId()
    ws = RakutenWebService(license_key="TOOTO")
    with assert_raises(Exception, "A 'license_key' and 'secret_service' must be provided"):
        ws.rms.order.getRequestId()
    ws = RakutenWebService(secret_service="TOOTO")
    with assert_raises(Exception, "A 'license_key' and 'secret_service' must be provided"):
        ws.rms.order.getRequestId()


@pytest.mark.online
def test_credentials(credentials):
    ws = RakutenWebService(**credentials)
    item = ws.ichiba.item.search(item_code="book:17924463")['Items'][0]
    assert item['itemName'] == 'NARUTO THE BEST (期間生産限定盤) [ (アニメーション) ]'  # noqa


@pytest.mark.online
def test_fake_credentials(fake_credentials):
    ws = RakutenWebService(**fake_credentials)
    result = ws.ichiba.item.search(item_code="book:17924463")
    assert result['error_description'] == 'specify valid applicationId'
    assert result['error'] == 'wrong_parameter'
