#!/bin/python
# author : ipmstyle <ipmstyle@gmail.com>

import os
from dotenv import load_dotenv

import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

load_dotenv()
logpath = os.getenv("LOG_FILEPATH", default=os.path.abspath('.'))

class Logger:
    def __init__(self, log_level=logging.DEBUG):
        log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        self.logger = logging.getLogger('webcam_logger')
        self.logger.setLevel(log_level)
        
        file_handler = TimedRotatingFileHandler(logpath, when='midnight', interval=1, backupCount=90, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        ## display to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)

if __name__ == "__main__":
    logger = Logger()

    # log msg example
    logger.log_debug('This is a debug message')
    logger.log_info('This is an info message')
    logger.log_warning('This is a warning message')
    logger.log_error('This is an error message')
    logger.log_critical('This is a critical message')
