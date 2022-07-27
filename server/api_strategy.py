################################################################################
# API using Strategy pattern
#
# Purpose: Define an abstract API strategy class with a template method to
#          extend the function of getting exchange rate list, and the 2 concrete
#          classes will implement a function to get data via http request and
#          normalize the data output from the http response. Implementation
#          refers to /$references/strategy.jpg from the project root folder.
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
from datetime import datetime
import requests


class ApiStrategy(ABC):
    ##
    # ApiStrategy abstract api strategy defined to get exchange rate list
    ##

    # Currency base options related to all APIs
    base_options = ["cad", "cny", "usd", "hkd", "jpy", "eur"]

    def __init__(self):
        # initialize variables for cache
        self.__last_updates = {}
        now = datetime.now()
        for base in self.base_options:
            self.__last_updates[base] = now
        self.__caches = {}

    # Template method for concrete classes to get data via http request
    # and normalize the data output from the http response
    @abstractmethod
    def build_rate_dict(self, from_base, to_bases):
        return {}

    # Get the exchange rate list from http request directly or from cache
    def get_rate_dict(self, currency_base):
        from_base = currency_base.lower()

        # get exchange rate list from cache
        # if the list is up to date (within 24 hours)
        time_diff = datetime.now() - self.__last_updates[from_base]
        if time_diff.seconds < 86400 and from_base in self.__caches:
            return self.__caches[from_base]

        # get exchange rate list by http request
        if from_base in self.base_options:
            to_bases = self.base_options[:]
            to_bases.remove(from_base)
            self.__caches[from_base] = self.build_rate_dict(
                from_base, to_bases)
            return self.__caches[from_base]
        return {}


class CurrencyApi(ApiStrategy):
    ##
    # CurrencyApi use Currency-api web service to get exchange rate data
    ##

    def build_rate_dict(self, from_base, to_bases):
        # normalized structure
        rate_dict = {
            "from": from_base,
            "to": {}
        }
        # http request
        res = requests.get(
            "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/" +
            from_base + ".json")
        # convert http JSON response to dictionary
        res_json = res.json()
        for base in to_bases:  # fill data
            rate_dict["to"][base] = res_json[from_base][base]
        return rate_dict


class ExchangeRateApi(ApiStrategy):
    ##
    # ExchangeRateApi use ExchangeRate-API web service to get exchange rate data
    ##

    def __init__(self, key):
        # initialize variable key that contain the api-key for ExchangeRate-API access
        self.__key = key
        super().__init__()

    def build_rate_dict(self, from_base, to_bases):
        # normalized structure
        rate_dict = {
            "from": from_base,
            "to": {}
        }
        # http request
        res = requests.get("https://v6.exchangerate-api.com/v6/" +
                           self.__key + "/latest/" + from_base)
        # convert http JSON response to dictionary
        res_json = res.json()
        for base in to_bases:  # fill data
            rate_dict["to"][base] = res_json["conversion_rates"][base.upper()]
        return rate_dict
