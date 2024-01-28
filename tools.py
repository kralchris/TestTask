"""
Tools - tools for advanced parametrization and reusability of code,
        including but not limited to decorators

@author: Kristijan <kristijan.sarin@gmail.com>
"""

import time
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler


class Tools:
    @staticmethod
    def io_retry(max_retries=3, delay=1):
        """
        Decorator to retry a function in case of an IOError.

        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                while retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except IOError as e:
                        retries += 1
                        print(
                            f"IOError on {func.__name__}: {e}. Retrying {retries}/{max_retries}")
                        time.sleep(delay)
                raise
            return wrapper
        return decorator

    @staticmethod
    def setup_logger(log_file):
        """
        Sets up a logger with both console and file handlers.

        """

        logger = logging.getLogger('TestTaskLogger')
        logger.setLevel(logging.INFO)

        c_handler = logging.StreamHandler()
        f_handler = RotatingFileHandler(
            log_file, maxBytes=1000000, backupCount=3)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger
