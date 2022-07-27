################################################################################
# App using Singleton pattern
#
# Purpose: Define a class to contain global read-only state and utilities. The
#          class processes configuration file, and then setting up logger, redis
#          database connection, record factory, the 2 currency exchange rate
#          APIs, access token for admin and server's port. Implementation
#          refers to /$references/singleton.jpg from the project root folder.
#
# Reason to use Singleton pattern:
#  - contain resources for global use
#  - need to process configuration file for the application setup
#  - need resources to only be created once
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from api_strategy import *
from logger_chain import *
from record_factory import *
import configparser
import redis


class App():
    ##
    # App create singleton instance with resources to use everywhere in the app
    ##

    __instance: "App" = None
    __logger: Logger = None

    # api option: Currency-api
    @staticmethod
    def api_currency():
        return "currency"

    # api option: ExchangeRate-API
    @staticmethod
    def api_exchange():
        return "exchange"

    # Return the signleton instance instead of creating a new object of App
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()

        return cls.__instance

    # Setup all the resources
    def setup(self):
        # soad configuration file
        config = configparser.ConfigParser()
        config.read('config.server.cfg')

        # setup logger
        if config["Log"]["console"] == "TRUE":
            self.__logger = ConsoleLogger().next(self.__logger)
        if config["Log"]["file"] == "TRUE":
            self.__logger = FileLogger(
                config["Log"]["log_file"]).next(self.__logger)

        # setup redis database connection
        self.dbconn = redis.Redis(
            host=config["Database"]["host"],
            port=int(config["Database"]["port"]),
            password=config["Database"]["pwd"],
            decode_responses=True
        )

        # setup record factory to create records for token and product
        self.__record_factory = RecordFactory()

        # setup the 2 currency exchange rate APIs
        self.__apis: dict[str, ApiStrategy] = {
            self.api_currency(): CurrencyApi(),
            self.api_exchange(): ExchangeRateApi(
                config["Others"]["exchangerate_api_key"])
        }

        # setup access token for admin
        self.__admin_token = config["Others"]["admin_token"]

        # setup server's port
        self.__server_port = int(config["Others"]["server_port"])

    # Log a message with a tag in front of it
    def log(self, tag, message):
        if self.__logger is not None:
            self.__logger.log(tag, message)

    # Get a token record with normalize data structure
    def record_token(self, data={}):
        return self.__record_factory.get_record(RecordFactory.table_token(), data)

    # Get a product record with normalize data structure
    def record_product(self, data={}):
        return self.__record_factory.get_record(RecordFactory.table_product(), data)

    @property
    def apis(self):
        return self.__apis

    @property
    def admin_token(self):
        return self.__admin_token

    @property
    def server_port(self):
        return self.__server_port
