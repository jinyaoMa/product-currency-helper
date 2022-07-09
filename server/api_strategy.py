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


class ApiStrategy(ABC):

    @abstractmethod
    def get_rate_list(self, currency_base):
        pass


class CurrencyApi(ApiStrategy):

    def get_rate_list(self, currency_base):
        pass


class AmdorenApi(ApiStrategy):

    def get_rate_list(self, currency_base):
        pass
