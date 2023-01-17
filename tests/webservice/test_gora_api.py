# coding: utf-8
import pytest


def assert_no_error(result):
    assert "error" not in result, result["error_description"]


def test_golf_search(ws):
    params = {"hits": 3}
    assert_no_error(ws.gora.golf.search(**params))


def test_golf_detail(ws):
    params = {"golfCourseId": 80004}
    assert_no_error(ws.gora.golf.detail(**params))


@pytest.mark.skip(reason="Stand by")
def test_plan_detail(ws):
    params = {"playDate": "2017-03-05", "hits": 3}
    assert_no_error(ws.gora.plan.search(**params))
