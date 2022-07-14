################################################################################
# Record using Factory pattern
#
# Purpose: to implement simple object-relation-mapping
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod

from api_strategy import ApiStrategy


class RecordFactory():

    @staticmethod
    def table_token():
        return "token"

    @staticmethod
    def table_product():
        return "product"

    def get_record(self, table, data):
        if table == self.table_token():
            return TokenRecord(data)
        elif table == self.table_product():
            return ProductRecord(data)
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
        self.id = data["id"] if "id" in data else None
        self.active = data["active"] if "active" in data else 1
        self.set_record(data)


class TokenRecord(Record):

    def set_record(self, data):
        self.access_token = data["access_token"] if "access_token" in data else None
        self.permission = data["permission"] if "permission" in data else None


class ProductRecord(Record):

    def set_record(self, data):
        self.title = data["title"] if "title" in data else None
        self.url = data["url"] if "url" in data else None
        self.img = data["img"] if "img" in data else None
        self.price = data["price"] if "price" in data else None
        if "base" in data and data["base"] in ApiStrategy.base_options:
            self.base = data["base"]
        else:
            self.base = None
