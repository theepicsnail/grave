import time
import inspect
from functools import wraps
import logging
import logging.config
import threading
import os
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.config.fileConfig("logging/logging.cfg")

def logged(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, _log_calls(getattr(cls, attr)))
    return cls

def _log_calls(method):
    cls_name = method.im_class.__name__
    method_name = cls_name+"."+method.__name__

    @wraps(method)
    def wrapped(*args, **kwargs):
        calling_thread = threading.currentThread()
        thread_name = calling_thread.getName()
        thread_id = calling_thread.ident
        pid = os.getpid()
        log_name = "Process - %s.%s(%s).%s" % (
            pid, thread_name, thread_id, cls_name)
        logger = logging.getLogger(log_name)

        pos_args = map(str, args)
        named_args = map("{}={}".format, kwargs)
        arg_str = ", ".join(pos_args + named_args)

        call_str = "%s(%s)" % (method_name, arg_str)

        ts = time.time()
        try:
            logger.debug("[>>] %s" % (call_str))
            args[0].logger = logger
            ret = method(*args, **kwargs)
            ts2 = time.time()
            logger.debug("[<<] %s => %s (took %.5f seconds)" % (call_str, ret, ts2-ts))
            return ret
        except:
            ts2 = time.time()
            logger.exception("[XX] %s (took %.5f seconds)" % (call_str, ts2-ts2))
            raise

    return wrapped


