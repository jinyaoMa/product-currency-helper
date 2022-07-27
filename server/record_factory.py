################################################################################
# Record using Factory pattern
#
# Purpose: Define abstract class with simple CRUD functions, so that all types
#          of records can get the same structure of data. Use a template method
#          to extend the constructor of a record for normalizing the data fields
#          of different types of records. Implementation refers to
#          /$references/factory.jpg from the project root folder.
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
from redis import Redis


class RecordFactory():
    ##
    # RecordFactory create record object by choosing different table/type
    ##

    @staticmethod
    def table_token():
        return "token"

    @staticmethod
    def table_product():
        return "product"

    # Get record with different structures of data
    def get_record(self, from_table, data={}):
        if from_table == self.table_token():
            return TokenRecord(data)
        elif from_table == self.table_product():
            return ProductRecord(data)
        else:
            raise ValueError(from_table)


class Record(ABC):
    ##
    # Record abstract record defined with common structure that every record must have
    ##

    def __init__(self, data={}):
        # setup data with certain structure based on different record types
        self.data = {
            **self.__normalize_data(data),
            # extend setup
            **self.normalize_record_data(data),
        }

    # Normalize data with datatype of values adjusted for every record
    def __normalize_data(self, data):
        expect_data = {}
        # id, int | record identifier
        if "id" in data:
            expect_data["id"] = int(data["id"])
        # active, int | default = 1; 0 - inactive record, 1 - active record
        if "active" in data:
            expect_data["active"] = int(data["active"])
        else:
            expect_data["active"] = 1
        return expect_data

    # Template method for concrete classes to normalize/extend set() function
    # Choose keys that are necessary to append, and adjust datatype of values
    @abstractmethod
    def normalize_record_data(self, data: dict):
        return {}

    # Template method for concrete classes to setup key label
    # label used to find Redis keys, e.g. "token:", "product:"
    @abstractmethod
    def key_label(self):
        return "[table|type]:"

    # Get the count key
    def __count_key(self):
        return self.key_label() + "count"

    # Get the count of records in database
    def count(self, dbconn: Redis):
        count = dbconn.get(self.__count_key())
        if count is None:
            return 0
        return int(count)

    # Create a new record in database
    def create(self, dbconn: Redis):
        id = self.count(dbconn) + 1
        dbconn.set(self.__count_key(), id)
        record_key = self.key_label() + str(id)
        dbconn.hmset(record_key, self.data)
        self.data["id"] = id  # give it an id after create

    # Get a list of records from database
    def get_list(self, dbconn: Redis):
        record_list = []
        count = self.count(dbconn)
        if count > 0:
            for i in range(1, count+1):
                record_key = self.key_label() + str(i)
                record = dbconn.hgetall(record_key)
                record_list.append({
                    **{
                        "id": i,
                    },
                    # normalize data types
                    **self.__normalize_data(record),
                    **self.normalize_record_data(record)
                })
        return record_list

    # Update a record in database
    def update(self, dbconn: Redis):
        id = self.data["id"]
        if id > 0 and id <= self.count(dbconn):
            record_key = self.key_label() + str(id)
            temp_data = self.data.copy()
            del temp_data["id"]  # skip id field
            dbconn.hmset(record_key, temp_data)

    # Activate a record in database
    def activate(self, dbconn: Redis, id):
        if id > 0 and id <= self.count(dbconn):
            dbconn.hset(self.key_label() + str(id), "active", 1)

    # Deactivate a record in database
    def deactivate(self, dbconn: Redis, id):
        if id > 0 and id <= self.count(dbconn):
            dbconn.hset(self.key_label() + str(id), "active", 0)


class TokenRecord(Record):
    ##
    # TokenRecord record object mapping to token
    ##

    def key_label(self):
        return "token:"

    def normalize_record_data(self, data: dict):
        expect_data = {}
        # access_token, string | access token string
        if "access_token" in data:
            expect_data["access_token"] = str(data["access_token"])
        # permission, string | permission string
        if "permission" in data:
            expect_data["permission"] = str(data["permission"])
        return expect_data


class ProductRecord(Record):
    ##
    # ProductRecord record object mapping to product
    ##

    def key_label(self):
        return "product:"

    def normalize_record_data(self, data: dict):
        expect_data = {}
        # title, string | Product title
        if "title" in data:
            expect_data["title"] = str(data["title"])
        # url, string | Product’s associated URL
        if "url" in data:
            expect_data["url"] = str(data["url"])
        # img, string | Product’s image URL
        if "img" in data:
            expect_data["img"] = str(data["img"])
        # price, float | Product’s price
        if "price" in data:
            expect_data["price"] = float(data["price"])
        # base, string | Product’s original currency base
        if "base" in data:
            expect_data["base"] = str(data["base"])
        return expect_data
