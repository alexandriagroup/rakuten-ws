===============================
Python Rakuten Web Service
===============================



.. image:: https://img.shields.io/pypi/v/rakuten-ws.svg
    :target: https://pypi.python.org/pypi/rakuten-ws

.. image:: https://travis-ci.org/alexandriagroup/rakuten-ws.svg?branch=master
    :target: https://travis-ci.org/alexandriagroup/rakuten-ws
    :alt: CI Status

.. image:: http://codecov.io/github/alexandriagroup/rakuten-ws/coverage.svg?branch=master
    :target: http://codecov.io/github/alexandriagroup/rakuten-ws?branch=master
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/python-rakuten-web-service/badge/?version=latest
    :target: http://python-rakuten-web-service.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Unofficial Python Client for Rakuten Web Service


* Free software: MIT license
* Documentation: https://rakuten-ws.readthedocs.io.


Supported APIs
--------------

-  `Rakuten Ichiba API`_
-  `Rakuten Ichiba RMS Item API`_
-  `Rakuten Ichiba RMS Product API`_
-  `Rakuten Ichiba RMS Order API`_
-  `Rakuten Ichiba RMS Inventory API`_
-  `Rakuten Books API`_
-  `Rakuten Travel API`_
-  `Rakuten Auction API`_
-  `Rakuten Kobo API`_
-  `Rakuten GORA API`_
-  `Rakuten Recipe API`_
-  `Rakuten Other APIs`_


.. _Rakuten Ichiba API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=1
.. _Rakuten Ichiba RMS Item API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?page=document0002
.. _Rakuten Ichiba RMS Product API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?page=document0009
.. _Rakuten Ichiba RMS Order API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?page=document0046
.. _Rakuten Ichiba RMS Inventory API: https://webservice.rms.rakuten.co.jp/merchant-portal/view?page=document0076
.. _Rakuten Books API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=2
.. _Rakuten Travel API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=4
.. _Rakuten Auction API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=4
.. _Rakuten Kobo API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=7
.. _Rakuten GORA API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=8
.. _Rakuten Recipe API: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=6
.. _Rakuten Other APIs: https://rakuten-api-documentation.antoniotajuelo.com/rakuten/service/view?rakuten_service_id=9


Installation
------------

Requirements:
  - python >= 2.7
  - python-lxml

You can install, upgrade, uninstall rakuten-ws with these commands::

  $ pip install [--user] rakuten-ws
  $ pip install [--user] --upgrade rakuten-ws
  $ pip uninstall rakuten-ws
