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
from record_factory import RecordFactory
from api_strategy import ApiStrategy
from permission_decorator import *
import random
import re


class ProductCurrencyHelperServices():

    # labels to prepend at the beginning of every log message
    tag_api_currency = "API|CURRENCY"
    tag_api_exchange = "API|EXCHANGE"
    tag_act_service_ = "ACT|SERVICE_"

    def check_token(self, token):
        if token == App().admin_token:
            App().log(self.tag_act_service_, "admin checks token (" + token + ") and pass")
            return AdvancedPermission(ManipulationPermission(BasicPermission(1), 1), 1).get_string()
        for t in App().record_factory.get_record(RecordFactory.table_token()).get_list(App().dbconn):
            if token == t["access_token"] and t["active"] == 1:
                App().log(self.tag_act_service_, "a user checks token (" + token + ") and pass")
                return t["permission"]
        App().log(self.tag_act_service_, "a user's token (" + token + ") is invalid")
        return ""

    def get_token_list(self):
        token_list = App().record_factory.get_record(
            RecordFactory.table_token()).get_list(App().dbconn)
        App().log(self.tag_act_service_, "a user gets token list: " + json.dumps(token_list))
        return token_list

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
        token.create(App().dbconn)
        return token

    def deactivate_token(self, id):
        App().log(self.tag_act_service_, "a user deactivates a token with id: " + str(id))
        App().record_factory.get_record(
            RecordFactory.table_token()).deactivate(App().dbconn, id)

    def activate_token(self, id):
        App().log(self.tag_act_service_, "a user activates a token with id: " + str(id))
        App().record_factory.get_record(
            RecordFactory.table_token()).activate(App().dbconn, id)

    def get_product_list(self):
        product_list = App().record_factory.get_record(
            RecordFactory.table_product()).get_list(App().dbconn)
        App().log(self.tag_act_service_,
                  "a user gets product list: " + json.dumps(product_list))
        return product_list

    def create_product(self, data):
        App().log(self.tag_act_service_, "a user creates a product with data: " + str(data))
        product = App().record_factory.get_record(RecordFactory.table_product(), data)
        product.create(App().dbconn)
        return product

    def update_product(self, data):
        App().log(self.tag_act_service_, "a user updates a product with data: " + str(data))
        product = App().record_factory.get_record(RecordFactory.table_product(), data)
        product.update(App().dbconn)
        return product

    def delete_product(self, id):
        App().log(self.tag_act_service_, "a user deletes a product with id: " + str(id))
        App().record_factory.get_record(
            RecordFactory.table_product()).deactivate(App().dbconn, id)

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
