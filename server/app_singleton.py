################################################################################
# App using Singleton pattern
#
# Purpose:
#
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
    __instance: "App"
    __logger: Logger

    # Return the signleton instance instead of creating a new object of App
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(App, cls).__new__(cls)
            cls.__instance.setup()

        return cls.__instance

    def setup(self):
        # soad configuration file
        config = configparser.ConfigParser()
        config.read('config.server.cfg')

        # setup redis database connection
        self.dbconn = redis.Redis(
            host=config["Database"]["host"],
            port=config["Database"]["port"],
            password=config["Database"]["pwd"],
            decode_responses=True
        )

        # setup logger
        if config["Log"]["console"] == "TRUE":
            self.__logger = ConsoleLogger().next(self.__logger)
        if config["Log"]["file"] == "TRUE":
            self.__logger = FileLogger(
                config["Log"]["log_file"]).next(self.__logger)

        # setup record factory to create records for token and product
        self.record_factory = RecordFactory()

        # setup the 2 currency exchange rate APIs
        self.currency_api = CurrencyApi()
        self.amdoren_api = AmdorenApi(config["Others"]["amdoren_key"])

        # setup access token for admin
        self.admin_token = config["Others"]["admin_token"]

        # setup server's port
        self.server_port = config["Others"]["server_port"]

    # Log a message with a tag in front of it
    def log(self, tag, message):
        if self.__logger is not None:
            self.__logger.log(tag, message)
