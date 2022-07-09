################################################################################
# Record using Factory pattern
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
import json


class RecordFactory:

    @staticmethod
    def token():
        return "token"

    @staticmethod
    def product():
        return "product"

    def get_record(self, table, data):
        if table == self.token():
            return Token(data)
        elif table == self.product():
            return Product(data)
        else:
            raise ValueError(table)


class Record(ABC):

    def __init__(self, data):
        self.data = {}
        self.set(data)

    @abstractmethod
    def set_record(self, data):
        pass

    def set(self, data):
        self.data["id"] = data["id"]
        self.data["active"] = data["active"]
        self.set_record(data)

    def get_json(self):
        return json.dumps(self.data)


class Token(Record):

    def set_record(self, data):
        self.data["access_token"] = data["access_token"]
        self.data["permission"] = data["permission"]


class Product(Record):

    def set_record(self, data):
        self.data["title"] = data["title"]
        self.data["url"] = data["url"]
        self.data["img"] = data["img"]
        self.data["price"] = data["price"]
        self.data["currency_base"] = data["currency_base"]
