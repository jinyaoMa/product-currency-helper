################################################################################
# ProductCurrencyHelperServices using Service Layer + Facade pattern
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

import json
from app_singleton import App
from model import *
from record_factory import RecordFactory
from api_strategy import ApiStrategy
from permission_decorator import *
import random
import re


class ProductCurrencyHelperServices():

    tag_api_currency = "API|CURRENCY"
    tag_api_exchange = "API|EXCHANGE"
    tag_act_service_ = "ACT|SERVICE_"

    def __init__(self):
        self.__token_model = TokenModel()
        self.__product_model = ProductModel()

    def check_token(self, token):
        if token == App().admin_token:
            App().log(self.tag_act_service_, "admin checks token (" + token + ") and pass")
            return AdvancedPermission(ManipulationPermission(BasicPermission(1), 1), 1).get_string()
        for t in self.__token_model.get_list():
            if token == t["access_token"] and t["active"] == 1:
                App().log(self.tag_act_service_, "a user checks token (" + token + ") and pass")
                return t["permission"]
        App().log(self.tag_act_service_, "a user's token (" + token + ") is invalid")
        return ""

    def get_token_list(self):
        json_token_list = self.__token_model.get_list()
        App().log(self.tag_act_service_, "a user gets token list: " + json.dumps(json_token_list))
        return json_token_list

    def create_token(self, permission_string):
        App().log(self.tag_act_service_,
                  "a user creates a token with permission: " + permission_string)
        permission = BasicPermission(1)
        if len(re.findall("m", permission_string)) > 0:
            permission = ManipulationPermission(permission, 1)
        else:
            permission = ManipulationPermission(permission, 0)
        if len(re.findall("a", permission_string)) > 0:
            permission = AdvancedPermission(permission, 1)
        else:
            permission = AdvancedPermission(permission, 0)

        token = App().record_factory.get_record(RecordFactory.table_token(), {
            "access_token": "".join(random.sample("0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f".split(","), 8)),
            "permission": permission.get_string()
        })
        self.__token_model.create(token)
        return token

    def deactivate_token(self, id):
        App().log(self.tag_act_service_, "a user deactivates a token with id: " + str(id))
        self.__token_model.deactivate(id)

    def activate_token(self, id):
        App().log(self.tag_act_service_, "a user activates a token with id: " + str(id))
        self.__token_model.activate(id)

    def get_product_list(self):
        json_product_list = self.__product_model.get_list()
        App().log(self.tag_act_service_,
                  "a user gets product list: " + json.dumps(json_product_list))
        return json_product_list

    def create_product(self, data):
        App().log(self.tag_act_service_, "a user creates a product with data: " + str(data))
        product = App().record_factory.get_record(RecordFactory.table_product(), data)
        self.__product_model.create(product)
        return product

    def update_product(self, data):
        App().log(self.tag_act_service_, "a user updates a product with data: " + str(data))
        product = App().record_factory.get_record(RecordFactory.table_product(), data)
        self.__product_model.update(product)
        return product

    def delete_product(self, id):
        App().log(self.tag_act_service_, "a user deletes a product with id: " + str(id))
        self.__product_model.deactivate(id)

    def get_rate_dict(self, which, currency_base):
        App().log(self.tag_act_service_, "a user gets rate dict with params: " +
                  "which = " + which + ", currency_base = " + currency_base)
        api = None
        if which == "currency":
            api = App().currency_api
            App().log(self.tag_act_service_, "a user gets rate dict via Currency-api")
        elif which == "exchange":
            api = App().exchangerate_api
            App().log(self.tag_act_service_, "a user gets rate dict via ExchangeRate-API")
        else:
            App().log(self.tag_act_service_, "a user fails to get rate dict")
            return {}

        rate_dict = api.get_rate_dict(currency_base)
        if which == "currency":
            App().log(self.tag_api_currency, "a user gets rate dict: " + str(rate_dict))
        elif which == "exchange":
            App().log(self.tag_api_exchange, "a user gets rate dict: " + str(rate_dict))

        return rate_dict

    def get_base_options(self):
        App().log(self.tag_act_service_, "a user gets base options: " +
                  ",".join(ApiStrategy.base_options))
        return ApiStrategy.base_options

    def get_api_options(self):
        App().log(self.tag_act_service_, "a user gets API options: " +
                  ",".join(ApiStrategy.api_options))
        return ApiStrategy.api_options
