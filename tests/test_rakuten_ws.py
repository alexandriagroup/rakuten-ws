#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

test_rakuten_ws
----------------------------------

Tests for `rakuten_ws` module.
"""
import pytest

from rakuten_ws import rakuten_ws


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/alexandriagroup/rakuten-ws')
    pass


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    pass
