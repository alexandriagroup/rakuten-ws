# coding: utf-8
import re
import os
import sys
import json

import mock
import pytest
import httpretty as httpretty_module

from vcr import VCR
from rakuten_ws import RakutenWebService


VCR_CASSETTE_DIR = os.path.join(os.path.dirname(__file__), "cassettes")
VCR_RECORD_MODE = os.environ.get("VCR_RECORD_MODE", "once")


def before_record_cb(request):
    if request.body:
        request.body = re.sub(
            b"<authKey>.+</authKey>", b"<authKey>XXXXXX</authKey>", request.body
        )
        request.body = re.sub(
            b"<shopUrl>.+</shopUrl>", b"<shopUrl>XXXXXX</shopUrl>", request.body
        )
        request.body = re.sub(
            b"<shopId>.+</shopId>", b"<shopId>XXXXXX</shopId>", request.body
        )
        request.body = re.sub(b">_shop.+<", b"<shopUrl>XXXXXX</shopUrl>", request.body)
        request.body = re.sub(b">ESA *.+<", b">ESA XXXXXX<>", request.body)
        request.body = re.sub(
            b"<userName>*.+</userName>", b"<userName>XXXXXX</userName>", request.body
        )
    return request


def before_record_response(response):
    # Used mainly for RakutenPayOrder.getOrder
    if (
        response["body"]["string"]
        and "application/json;charset=UTF-8" in response["headers"]["Content-Type"]
    ):
        data = json.loads(response["body"]["string"])

        if "OrderModelList" in data:
            for order_model in data["OrderModelList"]:
                for k in order_model["OrdererModel"]:
                    order_model["OrdererModel"][k] = "XXXXXX"

                for package_model in order_model["PackageModelList"]:
                    for k in package_model["SenderModel"]:
                        package_model["SenderModel"][k] = "XXXXXX"

                for k in order_model["SettlementModel"]:
                    order_model["SettlementModel"][k] = "XXXXXX"

            response["body"]["string"] = json.dumps(data, ensure_ascii=False).encode()
    return response


vcr = VCR(
    cassette_library_dir=VCR_CASSETTE_DIR,
    record_mode=VCR_RECORD_MODE,
    before_record_request=before_record_cb,
    before_record_response=before_record_response,
)


def pytest_configure(config):
    # register the online marker
    config.addinivalue_line(
        "markers",
        "online: mark a test that goes online. VCR will automatically be used.",
    )


def pytest_addoption(parser):
    parser.addoption(
        "--ws-debug", action="store_true", help="Allow webservice debugging"
    )


def pytest_runtest_setup(item):
    # Add the online marker to tests that will go online
    if "httpretty" not in item.fixturenames:
        if item.get_closest_marker("online") or ("ws" in item.fixturenames):
            item.fixturenames.append("use_vcr")
        else:
            item.fixturenames.append("no_requests")


@pytest.fixture()
def httpretty():
    httpretty_module.reset()
    httpretty_module.enable()
    yield httpretty_module
    httpretty_module.disable()


@pytest.fixture()
def use_vcr(request, monkeypatch):
    """
    This fixture is applied automatically to any test using the `online` mark. It will record and playback network
    sessions using VCR.
    The record mode of VCR can be set using the VCR_RECORD_MODE environment variable when running tests.
    """
    if VCR_RECORD_MODE == "off":
        yield None
    else:
        path_segments = [VCR_CASSETTE_DIR]
        if request.module is not None:
            path_segments.extend(request.module.__name__.split("tests.")[-1].split("."))
        if request.cls is not None:
            path_segments.append(request.cls.__name__)

        # Take into account the parametrization set by pytest
        # to create many tests from a single function with many parameters.
        request_keywords = request.keywords.keys()
        if "parametrize" in request_keywords:
            try:
                param_name = [x for x in request_keywords if x.startswith("_with_")][0]
            except IndexError:
                param_name = ""
        else:
            param_name = ""

        path_segments.append(request.function.__name__ + param_name + ".yaml")

        cassette_path = os.path.join(*path_segments)

        filter_query = [("applicationId", "XXXXXX")]
        filter_headers = [("Authorization", "ESA XXXXXX")]
        filter_post = []

        online = True
        if vcr.record_mode == "none":
            online = False
        elif vcr.record_mode == "once":
            online = not os.path.exists(cassette_path)
        # If we are going online, check the credentials
        if online:
            if os.environ.get("RAKUTEN_APP_ID", None) is None:
                pytest.skip("need credentials to run this test")

        with vcr.use_cassette(
            path=cassette_path,
            filter_query_parameters=filter_query,
            filter_headers=filter_headers,
            filter_post_data_parameters=filter_post,
            decode_compressed_response=True,
        ) as cassette:
            yield cassette


@pytest.fixture()
def no_requests(monkeypatch):
    online_funcs = [
        "requests.sessions.Session.request",
    ]

    if sys.version_info[0] == 2:
        online_funcs.extend(
            ["httplib.HTTPConnection.request", "httplib.HTTPSConnection.request"]
        )
    else:
        online_funcs.extend(
            [
                "http.client.HTTPConnection.request",
                "http.client.HTTPSConnection.request",
            ]
        )

    for func in online_funcs:
        monkeypatch.setattr(
            func,
            mock.Mock(
                side_effect=Exception("Online tests should use @pytest.mark.online")
            ),
        )


@pytest.fixture
def credentials():
    return {
        "application_id": os.environ.get("RAKUTEN_APP_ID", "<RAKUTEN_APP_ID>"),
        "license_key": os.environ.get("RMS_LICENSE_KEY", "<RMS_LICENSE_KEY>"),
        "secret_service": os.environ.get("RMS_SECRET_SERVICE", "<RMS_SECRET_SERVICE>"),
        "shop_url": os.environ.get("RMS_SHOP_URL", "<RMS_SHOP_URL>"),
    }


@pytest.fixture
def fake_credentials():
    return {
        "application_id": "<RAKUTEN_APP_ID>",
        "license_key": "<RMS_LICENSE_KEY>",
        "secret_service": "<RMS_SECRET_SERVICE>",
        "shop_url": "<RMS_SHOP_URL>",
    }


@pytest.fixture
def ws(credentials, request):
    ws_debug = request.config.getoption("--ws-debug")
    return RakutenWebService(debug=ws_debug, **credentials)
