################################################################################
# API using Strategy pattern
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
import requests


class ApiStrategy(ABC):

    base_options = ["cad", "cny", "usd", "hkd", "jpy", "eur"]

    @abstractmethod
    def build_rate_dict(self, from_base, to_bases):
        pass

    def get_rate_dict(self, currency_base):
        from_base = currency_base.lower()
        if from_base in self.base_options:
            to_bases = self.base_options[:]
            to_bases.remove(from_base)
            return self.build_rate_dict(from_base, to_bases)
        return {}


class CurrencyApi(ApiStrategy):

    def build_rate_dict(self, from_base, to_bases):
        rate_dict = {
            "from": from_base,
            "to": {}
        }
        res = requests.get(
            "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/" +
            from_base + ".json")
        res_json = res.json()
        for base in to_bases:
            rate_dict["to"][base] = res_json[from_base][base]
        return rate_dict


class ExchangeRateApi(ApiStrategy):

    def __init__(self, key):
        self.__key = key

    def build_rate_dict(self, from_base, to_bases):
        rate_dict = {
            "from": from_base,
            "to": {}
        }
        res = requests.get("https://v6.exchangerate-api.com/v6/" +
                           self.__key + "/latest/" + from_base)
        res_json = res.json()
        for base in to_bases:
            rate_dict["to"][base] = res_json["conversion_rates"][base.upper()]
        return rate_dict
