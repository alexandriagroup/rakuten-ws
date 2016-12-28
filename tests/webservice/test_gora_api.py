# coding: utf-8
from __future__ import unicode_literals


def assert_no_error(result):
    assert 'error' not in result, result['error_description']


def test_golf_search(ws):
    params = {'hits': 3}
    assert_no_error(ws.gora.golf.search(**params))


def test_golf_detail(ws):
    params = {'golfCourseId': 80004}
    assert_no_error(ws.gora.golf.detail(**params))


def test_plan_detail(ws):
    params = {'playDate': '2017-01-05', 'hits': 3}
    assert_no_error(ws.gora.plan.search(**params))
