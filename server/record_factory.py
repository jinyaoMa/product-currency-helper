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


class RecordFactory():

    @staticmethod
    def table_token():
        return "token"

    @staticmethod
    def table_product():
        return "product"

    def get_record(self, table, data):
        if table == self.token():
            return TokenRecord(data)
        elif table == self.product():
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
        if data["id"] is None:
            self.id = -1
        else:
            self.id = data["id"]
        if data["active"] is None:
            self.active = True
        else:
            self.active = data["active"]
        self.set_record(data)


class TokenRecord(Record):

    def set_record(self, data):
        self.access_token = data["access_token"]
        self.permission = data["permission"]


class ProductRecord(Record):

    def set_record(self, data):
        self.title = data["title"]
        self.url = data["url"]
        self.img = data["img"]
        self.price = data["price"]
        self.base = data["base"]
