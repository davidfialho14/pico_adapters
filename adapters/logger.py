import logging
import os
from logging.handlers import TimedRotatingFileHandler

import sys


class Logging:

    logger = None

    @staticmethod
    def setup(filepath):
        # redirect stderr to a file next to the log file with extension .err
        filename, log_extension = os.path.splitext(filepath)
        sys.stderr = open(filename + ".err", 'w')

        Logging.logger = logging.getLogger()
        Logging.logger.setLevel(logging.DEBUG)

        if filepath:
            # a new log file will be created every day
            # only a backup of the previous day will be kept
            handler = TimedRotatingFileHandler(filename=filepath,
                                               when='D', interval=1,
                                               backupCount=1)
        else:
            # file path is not specified -> messages will be printed to
            # the console
            handler = logging.StreamHandler()

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

        Logging.logger.addHandler(handler)

    @staticmethod
    def info(msg):
        Logging.logger.info(msg)

    @staticmethod
    def debug(msg):
        Logging.logger.debug(msg)

    @staticmethod
    def warning(msg):
        Logging.logger.warning(msg)

    @staticmethod
    def error(msg):
        Logging.logger.error(msg)
