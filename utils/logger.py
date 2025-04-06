# -*- coding: utf-8 -*-
#  wai-life-bot - Telegram bot
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging
import sys
# from utils.file_logger import FileLogger

class Logger:
    _instance = None 

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.INFO:
                return f"{record.getMessage()}"
            elif record.levelno == logging.WARNING:
                return f"Warning: {record.getMessage()}"
            elif record.levelno == logging.ERROR:
                return f"Error: {record.getMessage()}"
            elif record.levelno == logging.DEBUG:
                return f"Debug: {record.getMessage()}"
            return f"{record.levelname} - {record.getMessage()}"

    def __new__(cls, log_file=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file)
        return cls._instance

    def _initialize(self, log_file):
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)  

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.CustomFormatter())
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(self.CustomFormatter())
            self.logger.addHandler(file_handler)

    @classmethod
    def log(cls, level, message):
        instance = cls._instance or cls()
        instance.logger.log(level, message)

    @classmethod
    def info(cls, message):
        cls.log(logging.INFO, message)

    @classmethod
    def warning(cls, message):
        cls.log(logging.WARNING, message)

    @classmethod
    def error(cls, message):
        cls.log(logging.ERROR, message)

    @classmethod
    def debug(cls, message):
        cls.log(logging.DEBUG, message)
    
    # @classmethod
    # def log_to_file(cls, file_path, message):
    #     FileLogger.log(file_path, message)