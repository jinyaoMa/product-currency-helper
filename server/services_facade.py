################################################################################
# ProductCurrencyHelperServices using Service Layer + Facade pattern
#
# Purpose: Implement services as methods to define inputs and outputs of
#          specific use cases. Implementation refers to /$references/facade.jpg
#          from the project root folder.
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

import json
from app_singleton import App
from api_strategy import *
from permission_decorator import *
import random
import re


class ProductCurrencyHelperServices():
    ##
    # ProductCurrencyHelperServices contain all the services available from the back
    ##

    # labels to prepend at the beginning of every log message
    tag_api_currency = "API|CURRENCY"
    tag_api_exchange = "API|EXCHANGE"
    tag_act_service_ = "ACT|SERVICE_"

    # Check if an access token is valid and return its permission string
    def check_token(self, token):
        if token == App().admin_token:
            App().log(self.tag_act_service_, "admin checks token (" + token + ") and pass")
            # all permissions allowed for admin
            return AdvancedPermission(ManipulationPermission(BasicPermission(1), 1), 1).get_string()
        for t in App().record_token().get_list(App().dbconn):
            if token == t["access_token"] and t["active"] == 1:
                App().log(self.tag_act_service_, "a user checks token (" + token + ") and pass")
                return t["permission"]
        App().log(self.tag_act_service_, "a user's token (" + token + ") is invalid")
        return ""

    # Get a list of tokens from database
    def get_token_list(self):
        token_list = App().record_token().get_list(App().dbconn)
        App().log(self.tag_act_service_, "a user gets token list: " + json.dumps(token_list))
        return token_list

    # Create a token and store data into database
    def create_token(self, permission_string):
        App().log(self.tag_act_service_,
                  "a user creates a token with permission: " + permission_string)

        # build permission string
        permission = BasicPermission(1)
        if len(re.findall("m", permission_string)) > 0:
            permission = ManipulationPermission(permission, 1)
        else:
            permission = ManipulationPermission(permission, 0)
        if len(re.findall("a", permission_string)) > 0:
            permission = AdvancedPermission(permission, 1)
        else:
            permission = AdvancedPermission(permission, 0)

        # store data to database
        token = App().record_token({
            "access_token": "".join(random.sample("0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f".split(","), 8)),
            "permission": permission.get_string()
        })
        token.create(App().dbconn)
        return token

    # Deactivate a token record by ID
    def deactivate_token(self, id):
        App().log(self.tag_act_service_, "a user deactivates a token with id: " + str(id))
        App().record_token().deactivate(App().dbconn, id)

    # Activate a token record by ID
    def activate_token(self, id):
        App().log(self.tag_act_service_, "a user activates a token with id: " + str(id))
        App().record_token().activate(App().dbconn, id)

    # Get a list of products from database
    def get_product_list(self):
        product_list = App().record_product().get_list(App().dbconn)
        App().log(self.tag_act_service_,
                  "a user gets product list: " + json.dumps(product_list))
        return product_list

    # Create a product and store data into database
    def create_product(self, data):
        App().log(self.tag_act_service_, "a user creates a product with data: " + str(data))
        product = App().record_product(data)
        product.create(App().dbconn)
        return product

    # Update a product's' data in database
    def update_product(self, data):
        App().log(self.tag_act_service_, "a user updates a product with data: " + str(data))
        product = App().record_product(data)
        product.update(App().dbconn)
        return product

    # Deactivate a product record by ID
    def deactivate_product(self, id):
        App().log(self.tag_act_service_, "a user deactivates a product with id: " + str(id))
        App().record_product().deactivate(App().dbconn, id)

    # Activate a product record by ID
    def activate_product(self, id):
        App().log(self.tag_act_service_, "a user activates a product with id: " + str(id))
        App().record_product().activate(App().dbconn, id)

    # Get exchange rate data of a selected currency base with a selected Web service
    def get_rate_dict(self, which, currency_base):
        App().log(self.tag_act_service_, "a user gets rate dict with params: " +
                  "which = " + which + ", currency_base = " + currency_base)
        if which == App.api_currency():
            App().log(self.tag_act_service_, "a user gets rate dict via Currency-api")
        elif which == App.api_exchange():
            App().log(self.tag_act_service_, "a user gets rate dict via ExchangeRate-API")
        else:
            App().log(self.tag_act_service_, "a user fails to get rate dict")
            return {}

        # the condition flow to assign selected api is removed
        # use a dictionary to contain apis associated to App()
        # so that here only need one line of code to get the exchange rate data
        rate_dict = App().apis[which].get_rate_dict(currency_base)

        if which == App.api_currency():
            App().log(self.tag_api_currency, "a user gets rate dict: " + str(rate_dict))
        elif which == App.api_exchange():
            App().log(self.tag_api_exchange, "a user gets rate dict: " + str(rate_dict))

        return rate_dict

    # Get the available currency base options
    def get_base_options(self):
        App().log(self.tag_act_service_, "a user gets base options: " +
                  ",".join(ApiStrategy.base_options))
        return ApiStrategy.base_options

    # Get the available API service options
    def get_api_options(self):
        options = list(App().apis.keys())
        App().log(self.tag_act_service_, "a user gets API options: " +
                  ",".join(options))
        return options
