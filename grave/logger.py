import time
import inspect
from functools import wraps
import logging
import logging.config
import threading
import os
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import  currentframe
import hashlib

loaded = False
def getLogger(*a):
    if not loaded:
        loadLogConfig()
    return logging.getLogger(*a)

class ConsoleFormatter(logging.Formatter):
    RESET       = "\033[0m"
    BLACK       = "\033[30m"
    RED         = "\033[31m"
    GREEN       = "\033[32m"
    YELLOW      = "\033[33m"
    BLUE        = "\033[34m"
    PURPLE      = "\033[35m"
    CYAN        = "\033[36m"
    LIGHT_GRAY  = "\033[37m"
    DARK_GRAY   = "\033[1;30m"
    LIGHT_RED   = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_YELLOW= "\033[1;33m"
    LIGHT_BLUE  = "\033[1;34m"
    LIGHT_PURPLE= "\033[1;35m"
    LIGHT_CYAN  = "\033[1;36m"
    WHITE       = "\033[1;37m"

    def hashColor(self, value):
        return [
            ConsoleFormatter.RED,
            ConsoleFormatter.GREEN,
            ConsoleFormatter.YELLOW,
            ConsoleFormatter.BLUE,
            ConsoleFormatter.PURPLE,
            ConsoleFormatter.CYAN,
            ConsoleFormatter.WHITE,
        ][sum(map(ord, hashlib.sha1(str(value)).digest()))%7]

    def format(self, record):
        record.reset_color = ConsoleFormatter.RESET
        #'created', 'exc_info', 'exc_text', 'filename', 'funcName', 'getMessage',
        #'levelname', 'levelno', 'lineno', 'module', 'msecs', 'msg', 'name',
        #'pathname', 'process', 'processName', 'relativeCreated', 'thread', 'threadName'
        record.level_color = {
            "DEBUG": ConsoleFormatter.LIGHT_GRAY,
            "INFO": ConsoleFormatter.CYAN,
            "WARNING": ConsoleFormatter.YELLOW,
            "ERROR": ConsoleFormatter.RED,
            "CRITICAL": "\033[1;41m"
        }[record.levelname]

        record.process_color = self.hashColor(record.process)
        record.name_color = self.hashColor(record.name)
        record.thread_color = self.hashColor(record.thread)

        return super(ConsoleFormatter, self).format(record)

    def formatTime(self, record, datefmt=None):
        s = super(ConsoleFormatter, self).formatTime(record, datefmt)
        return ConsoleFormatter.YELLOW + s + ConsoleFormatter.RESET

def loadLogConfig():
    logging.config.fileConfig("logging/logging.cfg")
    print "Loaded logging config"
    global loaded
    loaded = True
    logger = getLogger()
    logger.debug("debug")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")
    logger.critical("critical")
    try:
        def exception():
            raise Exception()
        exception()
    except:
        getLogger().exception("exception")
def logged(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, _log_calls(getattr(cls, attr)))
    return cls

import traceback
def _log_calls(method):
    cls_name = method.im_class.__name__
    method_name = cls_name+"."+method.__name__

    @wraps(method)
    def wrapped(*args, **kwargs):
        logger = getLogger()

        # Override loggers 'findCaller'
        caller = traceback.extract_stack()[-2][:3]
        logger.findCaller = lambda:caller

        pos_args = map(str, args)
        named_args = map("{}={}".format, kwargs)
        arg_str = ", ".join(pos_args + named_args)

        call_str = "%s(%s)" % (method_name, arg_str)

        ts = time.time()
        try:
            logger.debug("[>>] %s" % (call_str))
            args[0].logger = logger
            args[0].log = logger
            ret = method(*args, **kwargs)
            ts2 = time.time()
            logger.debug("[<<] %s => %s (took %.5f seconds)" % (call_str, ret, ts2-ts))
            return ret
        except:
            ts2 = time.time()
            logger.exception("[XX] %s (took %.5f seconds)" % (call_str, ts2-ts2))
            raise

    return wrapped


