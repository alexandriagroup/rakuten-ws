#!/usr/bin/env python
# coding: utf-8
import os

from rakuten_ws import RakutenWebService

credentials = {
    'application_id': os.environ.get('RAKUTEN_APP_ID', ''),
    'license_key': os.environ.get('RMS_LICENSE_KEY', ''),
    'secret_service': os.environ.get('RMS_SECRET_SERVICE', ''),
    'shop_url': os.environ.get('RMS_SHOP_URL', ''),
}

assert len(credentials['shop_url']) > 0

ws = RakutenWebService(**credentials)
