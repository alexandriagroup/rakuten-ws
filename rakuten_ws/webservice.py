# coding: utf-8
import os.path as op
import json

from .baseapi import ApiEndpoint, ApiService, BaseWebService, ApiMethod
from .baserms import (
    BaseRmsService,
    ZeepClient,
    RestClient,
    RestMethod,
    RmsServiceClient,
)
from . import parameters

# Third-party imports
import requests


class IchibaAPI(ApiService):
    item = ApiEndpoint(
        ApiMethod("search", api_version="20170706"),
        ApiMethod("ranking", api_version="20170628"),
    )
    genre = ApiEndpoint(ApiMethod("search", api_version="20120723"))
    tag = ApiEndpoint(ApiMethod("search", api_version="20140222"))
    product = ApiEndpoint(
        ApiMethod("search", api_version="20170426"), api_endpoint="Product"
    )


class BooksAPI(ApiService):
    api_version = "20170404"

    total = ApiEndpoint(ApiMethod("search"))
    book = ApiEndpoint(ApiMethod("search"))
    cd = ApiEndpoint(ApiMethod("search"), api_endpoint="BooksCD")
    dvd = ApiEndpoint(ApiMethod("search"), api_endpoint="BooksDVD")
    foreign_book = ApiEndpoint(ApiMethod("search"))
    magazine = ApiEndpoint(ApiMethod("search"))
    game = ApiEndpoint(ApiMethod("search"))
    software = ApiEndpoint(ApiMethod("search"))
    genre = ApiEndpoint(ApiMethod("search", api_version="20121128"))


class TravelAPI(ApiService):
    api_version = "20170426"

    hotel = ApiEndpoint(
        ApiMethod("simple_search", "simple_hotel_search"),
        ApiMethod("detail_search", "hotel_detail_search"),
        ApiMethod("search_vacant", "vacant_hotel_search"),
        ApiMethod("ranking", "hotel_ranking"),
        ApiMethod("get_chain_list", "get_hotel_chain_list"),
        ApiMethod("keyword_search", "keyword_hotel_search"),
        api_endpoint="Travel",
        api_version="20170426",
    )
    area = ApiEndpoint(
        ApiMethod("get_class", "get_area_class"),
        api_endpoint="Travel",
        api_version="20131024",
    )


class AuctionAPI(ApiService):
    api_version = "20120927"

    genre_id = ApiEndpoint(ApiMethod("search"))
    genre_keyword = ApiEndpoint(ApiMethod("search"))
    item = ApiEndpoint(ApiMethod("search"))
    item_code = ApiEndpoint(ApiMethod("search"))


class KoboAPI(ApiService):
    api_version = "20131010"

    genre = ApiEndpoint(
        ApiMethod("search", "genre_search"), api_endpoint="Kobo", api_version="20131010"
    )
    ebook = ApiEndpoint(
        ApiMethod("search", "ebook_search"), api_endpoint="Kobo", api_version="20170426"
    )


class GoraAPI(ApiService):
    api_version = "20170623"

    golf = ApiEndpoint(
        ApiMethod("search", "gora_golf_course_search"),
        ApiMethod("detail", "gora_golf_course_detail"),
        api_endpoint="Gora",
    )
    plan = ApiEndpoint(ApiMethod("search", "gora_plan_search"), api_endpoint="Gora")


class RecipeAPI(ApiService):
    api_version = "20170426"

    category = ApiEndpoint(
        ApiMethod("ranking", "category_ranking"),
        ApiMethod("list", "category_list"),
        api_endpoint="Recipe",
    )


class OtherAPI(ApiService):
    high_commission_shop = ApiEndpoint(
        ApiMethod("list", api_version="20131205"), api_endpoint="HighCommissionShop"
    )


class RmsInventoryAPI(ZeepClient):
    # Documentation : https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/inventoryapi  # noqa
    # Code Reference : https://webservice.rms.rakuten.co.jp/merchant-portal/view?contents=/en/common/1-1_service_index/inventoryApi/inventoryApiCodeReference  # noqa
    wsdl = "file://%s" % op.abspath(
        op.join(op.dirname(__file__), "wsdl", "inventoryapi.wsdl")
    )

    def getInventoryExternal(self, inventorySearchRange=None, itemUrl=None):
        GetRequestExternalModelType = self.xsd_types["GetRequestExternalModel"]  # noqa
        if isinstance(itemUrl, (list, tuple)):
            ArrayOfString = self.zeep_client.get_type("ns0:ArrayOfString")  # noqa
            itemUrl = ArrayOfString(itemUrl)  # noqa
        request = GetRequestExternalModelType(
            inventorySearchRange=inventorySearchRange, itemUrl=itemUrl
        )
        return self._send_request(
            "getInventoryExternal", getRequestExternalModel=request
        )

    def _create_update_request(
        self,
        itemUrl,
        inventoryType,
        restTypeFlag=0,
        HChoiceName=None,
        VChoiceName=None,
        orderFlag=0,
        nokoriThreshold=0,
        inventoryUpdateMode=1,
        inventory=None,
        inventoryBackFlag=0,
        normalDeliveryDeleteFlag=False,
        normalDeliveryId=0,
        lackDeliveryDeleteFlag=False,
        lackDeliveryId=0,
        orderSalesFlag=0,
    ):
        UpdateRequestExternalItemType = self.xsd_types[
            "UpdateRequestExternalItem"
        ]  # noqa
        return UpdateRequestExternalItemType(
            itemUrl=itemUrl,
            inventoryType=inventoryType,
            restTypeFlag=restTypeFlag,
            HChoiceName=HChoiceName,
            VChoiceName=VChoiceName,
            orderFlag=orderFlag,
            nokoriThreshold=nokoriThreshold,
            inventoryUpdateMode=inventoryUpdateMode,
            inventory=inventory,
            inventoryBackFlag=inventoryBackFlag,
            normalDeliveryDeleteFlag=normalDeliveryDeleteFlag,
            normalDeliveryId=normalDeliveryId,
            lackDeliveryDeleteFlag=lackDeliveryDeleteFlag,
            lackDeliveryId=lackDeliveryId,
            orderSalesFlag=orderSalesFlag,
        )

    def updateInventoryExternal(self, args):
        UpdateRequestExternalModelType = self.xsd_types[
            "UpdateRequestExternalModel"
        ]  # noqa
        ArrayOfUpdateRequestExternalItemType = self.xsd_types[
            "ArrayOfUpdateRequestExternalItem"
        ]  # noqa
        if not isinstance(args, (list, tuple)):
            args = [args]
        assert len(args) <= 400, "The maximum number of items (400) has been exceeded"
        update_request_list = []
        for kwargs in args:
            update_request_list.append(self._create_update_request(**kwargs))
        data = UpdateRequestExternalModelType(
            ArrayOfUpdateRequestExternalItemType(update_request_list)
        )
        return self._send_request(
            "updateInventoryExternal", updateRequestExternalModel=data
        )


class RmsOrderAPI(ZeepClient):
    wsdl = "file://%s" % op.abspath(
        op.join(op.dirname(__file__), "wsdl", "orderapi.wsdl")
    )

    def getOrder(self, **kwargs):
        request = {
            "isOrderNumberOnlyFlg": kwargs.get("isOrderNumberOnlyFlg", False),
        }
        order_search_model_keys = [
            "asuraku",
            "cardSearchModel",
            "comment",
            "coupon",
            "dateType",
            "delivery",
            "drug",
            "enclosureStatus",
            "endDate",
            "itemName",
            "itemNumber",
            "mailAddressType",
            "modify",
            "orderSite",
            "orderType",
            "ordererKana",
            "ordererMailAddress",
            "ordererName",
            "ordererPhoneNumber",
            "overseas",
            "pointStatus",
            "pointUsed",
            "rbankStatus",
            "reserveNumber",
            "senderName",
            "senderPhoneNumber",
            "settlement",
            "startDate",
            "status",
        ]
        order_search_model_kwargs = {
            k: kwargs[k] for k in kwargs if k in order_search_model_keys
        }
        if order_search_model_kwargs:
            OrderSearchModelType = self.xsd_types["orderSearchModel"]  # noqa
            request["orderSearchModel"] = OrderSearchModelType(
                **order_search_model_kwargs
            )

        order_number = kwargs.get("orderNumber", None)
        if order_number is not None:
            if isinstance(order_number, (list, tuple)):
                ArrayOfString = self.zeep_client.get_type("ns0:ArrayOfString")  # noqa
                request["orderNumber"] = ArrayOfString(order_number)  # noqa
            else:
                request["orderNumber"] = order_number
        return self._send_request("getOrder", **request)

    def updateOrder(self, requestId, orderModel=None):
        request = {"requestId": requestId}
        OrderModelType = self.xsd_types["orderModel"]  # noqa
        if orderModel is not None:
            if not isinstance(orderModel, (list, tuple)):
                request["orderModel"] = OrderModelType(**orderModel)
            else:
                request["orderModel"] = []
                for model_kwargs in orderModel:
                    request["orderModel"].append(OrderModelType(**model_kwargs))

        return self._send_request("updateOrder", **request)


class RmsProductAPI(RestClient):
    api_version = "2.0"
    search = RestMethod(http_method="GET")


class RmsItemAPI(RestClient):
    get = RestMethod(http_method="GET")
    insert = RestMethod(http_method="POST", params=parameters.item_insert)
    update = RestMethod(http_method="POST", params=parameters.item_update)
    delete = RestMethod(http_method="POST", params=parameters.item_delete)
    search = RestMethod(http_method="GET")


class RmsItemsAPI(RestClient):
    update = RestMethod(http_method="POST", params=parameters.items_update)


class RmsCabinetAPI(RestClient):
    get_usage = RestMethod(http_method="GET", name="usage/get")
    get_folders = RestMethod(http_method="GET", name="folders/get")
    get_files = RestMethod(http_method="GET", name="folder/files/get")
    search_files = RestMethod(http_method="GET", name="files/search")
    get_trash_files = RestMethod(http_method="GET", name="trashbox/files/get")
    delete_file = RestMethod(
        http_method="POST", name="file/delete", root_xml_key="fileDelete"
    )
    revert_trash_file = RestMethod(
        http_method="POST", name="trashbox/file/revert", root_xml_key="fileRevert"
    )
    insert_file = RestMethod(
        http_method="POST",
        name="file/insert",
        form_data="file",
        root_xml_key="fileInsert",
        params=parameters.cabinet_insert_file,
    )
    update_file = RestMethod(
        http_method="POST",
        name="file/update",
        form_data="file",
        root_xml_key="folderUpdate",
    )
    insert_folder = RestMethod(
        http_method="POST", name="folder/insert", root_xml_key="folderInsert"
    )


class RmsNavigationAPI(RestClient):
    get_genre = RestMethod(http_method="GET", name="genre/get")
    get_tag = RestMethod(http_method="GET", name="genre/tag/get")
    get_header = RestMethod(
        http_method="GET", name="genre/header/get", root_xml_key="navigationHeaderGet"
    )


class RmsCategoryAPI(RestClient):
    api_endpoint = "categoryapi"
    get_categorysets = RestMethod(
        http_method="GET", name="shop/categorysets/get", root_xml_key="categorysetsGet"
    )
    get_categories = RestMethod(
        http_method="GET", name="shop/categories/get", root_xml_key="categoriesGet"
    )
    get_category = RestMethod(
        http_method="GET", name="shop/category/get", root_xml_key="categoryGet"
    )
    insert_category = RestMethod(
        http_method="POST",
        name="shop/category/insert",
        params=parameters.category_insert,
        root_xml_key="categoryInsert",
    )
    update_category = RestMethod(
        http_method="POST",
        name="shop/category/update",
        params=parameters.category_update,
        root_xml_key="categoryUpdate",
    )
    delete_category = RestMethod(
        http_method="POST", name="shop/category/delete", root_xml_key="categoryDelete"
    )
    move_category = RestMethod(
        http_method="POST",
        name="shop/category/move",
        params=parameters.category_move,
        root_xml_key="categoryMove",
    )


# Documentation:
# https://webservice.rms.rakuten.co.jp/merchant-portal/
# view?contents=/en/common/1-1_service_index/rakutenpayorderapi/
class RmsRakutenPayOrderAPI(RmsServiceClient):
    endpoint = "https://api.rms.rakuten.co.jp/es/2.0/order"
    session = requests.Session()

    def prepare_request(self, name, data):
        headers = {
            "Authorization": self.service.esa_key,
            "Content-Type": "application/json; charset=utf-8",
        }
        req = requests.Request(
            "POST", self.endpoint + "/" + name, json=data, headers=headers
        )
        return req.prepare()

    def send_request(self, name, data):
        response = self.session.send(self.prepare_request(name, data))
        return json.loads(response.text)

    def searchOrder(self, **kwargs):
        return self.send_request("searchOrder", kwargs)

    def getOrder(self, orderNumberList, version=1):
        """
        Retrieve the orders specified by `orderNumberList`

        Usage:
        orders = rws.rms.order.getOrder(orderNumberList=orderNumberList, version=version)
        """
        return self.send_request(
            "getOrder", {"orderNumberList": orderNumberList, "version": version}
        )

    def confirmOrder(self, orderNumberList):
        return self.send_request("confirmOrder", {"orderNumberList": orderNumberList})


class RmsService(BaseRmsService):
    item = RmsItemAPI()
    items = RmsItemsAPI()
    product = RmsProductAPI()
    cabinet = RmsCabinetAPI()
    navigation = RmsNavigationAPI()
    category = RmsCategoryAPI()

    order = RmsOrderAPI()
    rakutenpay_order = RmsRakutenPayOrderAPI()
    inventory = RmsInventoryAPI()


class RakutenWebService(BaseWebService):

    rms = RmsService()

    ichiba = IchibaAPI()
    books = BooksAPI()
    travel = TravelAPI()
    auction = AuctionAPI()
    kobo = KoboAPI()
    gora = GoraAPI()
    recipe = RecipeAPI()
    other = OtherAPI()
