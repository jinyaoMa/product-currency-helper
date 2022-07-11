################################################################################
# Logger using Chain-of-Responsibility pattern
#
# Purpose:
#
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from abc import ABC, abstractmethod
from datetime import datetime


class Logger(ABC):

    __next_logger: "Logger" = None

    def next(self, logger):
        self.__next_logger = logger
        return self

    def log(self, tag, message):
        self.make_entry(tag, message)
        # pass the messsage if it has an associated next logger
        if self.__next_logger is not None:
            self.__next_logger.log(tag, message)

    @abstractmethod
    def make_entry(self, tag, message):
        pass


class ConsoleLogger(Logger):

    def make_entry(self, tag, message):
        # log message to console
        print("[" + tag + "]" +
              "(" + datetime.now().strftime("%Y/%m/d,%H:%M:%S") + "): " +
              message)


class FileLogger(Logger):

    def __init__(self, filename):
        self.__file = open(filename, "a")

    def make_entry(self, tag, message):
        # log message into file
        self.__file.write("[" + tag + "]" +
                          "(" + datetime.now().strftime("%Y/%m/d,%H:%M:%S") + "): " +
                          message + "\n")
