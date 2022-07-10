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

from app_singleton import App
from model import *
from record_factory import RecordFactory
from permission_decorator import *
import json
import random
import re


class ProductCurrencyHelperServices():

    tag_api_currency = "API|CURRENCY"
    tag_api_amdoren_ = "API|AMDOREN_"
    tag_act_service_ = "ACT|SERVICE_"

    def __init__(self, token_model: TokenModel, product_model: ProductModel):
        self.token_model = token_model
        self.product_model = product_model

    def check_token(self, token):
        if token == App().admin_token:
            App().log(self.tag_act_service_, "admin checks token (" + token + ") and pass")
            return True
        for _, t in self.token_model.get_list():
            if token == t["access_token"] and t["active"]:
                App().log(self.tag_act_service_, "a user checks token (" + token + ") and pass")
                return True
        App().log(self.tag_act_service_, "a user's token (" + token + ") is invalid")
        return False

    def get_token_list(self):
        json_token_list = json.dumps(self.token_model.get_list())
        App().log(self.tag_act_service_, "a user gets token list: " + json_token_list)
        return json_token_list

    def create_token(self, permission_string):
        permission = BasicPermission(1)
        if len(re.findall("manipulation:1", permission_string)) > 0:
            permission = ManipulationPermission(permission, 1)
        else:
            permission = ManipulationPermission(permission, 0)
        if len(re.findall("advanced:1", permission_string)) > 0:
            permission = AdvancedPermission(permission, 1)
        else:
            permission = AdvancedPermission(permission, 0)

        token = App().record_factory.get_record(RecordFactory.table_token, {
            "access_token": "".join(random.sample("0123456789abcdef".split(""), 8)),
            "permission": permission
        })
        self.token_model.create(token)
        return token

    def deactivate_token(self, id):
        self.token_model.deactivate(id)

    def activate_token(self, id):
        self.token_model.activate(id)

    def get_product_list(self):
        json_product_list = json.dumps(self.product_model.get_list())
        App().log(self.tag_act_service_, "a user gets product list: " + json_product_list)
        return json_product_list

    def create_product(self, data):
        product = App().record_factory.get_record(RecordFactory.table_product, data)
        self.product_model.create(product)
        return product

    def update_product(self, data):
        product = App().record_factory.get_record(RecordFactory.table_product, data)
        self.product_model.update(product)
        return product

    def delete_product(self, id):
        self.product_model.deactivate(id)

    def get_rate_dict(self, which, currency_base):
        api = None
        if which == "currency":
            api = App().currency_api
        elif which == "currency":
            api = App().amdoren_api
        else:
            return {}

        return api.get_rate_dict(currency_base)
