# logging_example.py
import logging
import sys
import os

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
# d_handler = logging.StreamHandler()   #mode='w' ensures this files is overwritten every time the logger runs
# f_handler = logging.StreamHandler()
# i_handler = logging.StreamHandler()

# c_handler.setLevel(logging.DEBUG)
# f_handler.setLevel(logging.ERROR)
# i_handler.setLevel(logging.INFO)
# d_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
c_format = logging.Formatter('[%(levelname)s]: %(message)s')
# d_format = logging.Formatter('[%(levelname)s]: %(message)s')
# f_format = logging.Formatter('[%(levelname)s] %(message)s {File: (%(filename)s), Function: (%(funcName)s), Line: (%(lineno)d), at (%(asctime)s)}' )
# i_format = logging.Formatter('[%(levelname)s] %(message)s at (%(asctime)s)')

c_handler.setFormatter(c_format)
# d_handler.setFormatter(d_format)
# f_handler.setFormatter(f_format)
# i_handler.setFormatter(i_format)

# Add handlers to the logger
logger.addHandler(c_handler)
# logger.addHandler(d_handler)
# logger.addHandler(f_handler)
# logger.addHandler(i_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
# logger.setLevel(logging.DEBUG)
# logger.info("Testng writing to log file")