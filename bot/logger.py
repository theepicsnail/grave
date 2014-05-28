import logging
import logging.config
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.config.fileConfig("logging/logging.cfg")

def get_logger(prefix="root"):
    return logging.getLogger(prefix)

