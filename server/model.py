################################################################################
# Model to access and manipulate database
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
from app_singleton import App


class Model(ABC):
    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def create(self, record):
        pass

    @abstractmethod
    def get_list(self):
        pass

    @abstractmethod
    def update(self, record):
        pass

    @abstractmethod
    def activate(self, id):
        pass

    @abstractmethod
    def deactivate(self, id):
        pass


class TokenModel(Model):

    def count(self):
        count = App().dbconn.get("token:count")
        if count is None:
            return 0
        return int(count)

    def create(self, record):
        record.id = self.count() + 1
        App().dbconn.set("token:count", record.id)
        token_key = "token:" + str(record.id)
        App().dbconn.hset(token_key, "access_token",
                          record.access_token)
        App().dbconn.hset(token_key, "permission", record.permission)
        App().dbconn.hset(token_key, "active", record.active)

    def get_list(self):
        token_list = []
        count = self.count()
        if count > 0:
            for i in range(0, count):
                token_key = "token:" + str(i)
                token = {
                    "id": i,
                }
                token["access_token"] = str(
                    App().dbconn.hget(token_key, "access_token"))
                token["permission"] = str(
                    App().dbconn.hget(token_key, "permission"))
                token["active"] = bool(App().dbconn.hget(token_key, "active"))
                token_list.append(token)
        return token_list

    def update(self, record):
        if record.id >= 0 and record.id < self.count():
            token_key = "token:" + str(record.id)
            App().dbconn.hset(token_key, "access_token",
                              record.access_token)
            App().dbconn.hset(token_key, "permission",
                              record.permission)
            App().dbconn.hset(token_key, "active", record.active)

    def activate(self, id):
        if id >= 0 and id < self.count():
            App().dbconn.hset("token:" + str(id), "active", True)

    def deactivate(self, id):
        if id >= 0 and id < self.count():
            App().dbconn.hset("token:" + str(id), "active", False)


class ProductModel(Model):

    def count(self):
        count = App().dbconn.get("product:count")
        if count is None:
            return 0
        return int(count)

    def create(self, record):
        record.id = self.count() + 1
        App().dbconn.set("product:count", record.id)
        product_key = "product:" + str(record.id)
        App().dbconn.hset(product_key, "title", record.title)
        App().dbconn.hset(product_key, "url", record.url)
        App().dbconn.hset(product_key, "img", record.img)
        App().dbconn.hset(product_key, "base", record.base)
        App().dbconn.hset(product_key, "price", record.price)
        App().dbconn.hset(product_key, "active", record.active)

    def get_list(self):
        product_list = []
        count = self.count()
        if count > 0:
            for i in range(0, count):
                product_key = "product:" + str(i)
                product = {
                    "id": i,
                }
                product["title"] = str(App().dbconn.hget(product_key, "title"))
                product["url"] = str(App().dbconn.hget(product_key, "url"))
                product["img"] = str(App().dbconn.hget(product_key, "img"))
                product["base"] = str(App().dbconn.hget(product_key, "base"))
                product["price"] = float(
                    App().dbconn.hget(product_key, "price"))
                product["active"] = bool(
                    App().dbconn.hget(product_key, "active"))
                if product["active"]:  # only get those are NOT soft deleted
                    product_list.append(product)
        return product_list

    def update(self, record):
        if record.id >= 0 and record.id < self.count():
            product_key = "product:" + str(record.id)
            App().dbconn.hset(product_key, "title", record.title)
            App().dbconn.hset(product_key, "url", record.url)
            App().dbconn.hset(product_key, "img", record.img)
            App().dbconn.hset(product_key, "base", record.base)
            App().dbconn.hset(product_key, "price", record.price)
            App().dbconn.hset(product_key, "active", record.active)

    def activate(self, id):
        if id >= 0 and id < self.count():
            App().dbconn.hset("product:" + str(id), "active", True)

    def deactivate(self, id):
        if id >= 0 and id < self.count():
            App().dbconn.hset("product:" + str(id), "active", False)
