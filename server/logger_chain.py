################################################################################
# Logger using Chain-of-Responsibility pattern
#
# Purpose: Define an abstract logger class with a template method to extend the
#          function for logging messages in different ways include:
#           - log to console
#           - log to file
#          Implementation refers to /$references/chainOfResponsibility.jpg
#          from the project root folder.
#
# Reason to use Chain-of-Responsibility pattern:
#  - need to process a sequence of logging tasks by one function call
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
from datetime import datetime


class Logger(ABC):
    ##
    # Logger abstract logger defined with a next logger reference for chaining
    ##

    __next_logger: "Logger" = None

    # Setup the next logger in the chain
    def next(self, logger):
        self.__next_logger = logger
        return self

    # Log a message with a tag and continue in the chain
    def log(self, tag, message):
        self.make_entry(tag, message)
        # pass the messsage if it has an associated next logger
        if self.__next_logger is not None:
            self.__next_logger.log(tag, message)

    # Template method for concrete classes to log messages in different ways
    @abstractmethod
    def make_entry(self, tag, message):
        pass


class ConsoleLogger(Logger):
    ##
    # ConsoleLogger logger to output messages to console
    ##

    def make_entry(self, tag, message):
        # log message to console
        print("[" + tag + "]" +
              "(" + datetime.now().strftime("%Y/%m/d,%H:%M:%S") + "): " +
              message)


class FileLogger(Logger):
    ##
    # FileLogger logger to output messages to file
    ##

    def __init__(self, filename):
        # initialize variable file to prepare for message writing
        self.__file = open(filename, "a")

    def make_entry(self, tag, message):
        # log message into file
        self.__file.write("[" + tag + "]" +
                          "(" + datetime.now().strftime("%Y/%m/d,%H:%M:%S") + "): " +
                          message + "\n")
