import time
import inspect
from functools import wraps
import logging
import logging.config
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.config.fileConfig("logging/logging.cfg")

def logged(cls):

    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, _log_calls(getattr(cls, attr)))
    return cls

def _log_calls(method):

    cls_name = method.im_class.__name__
    log_name = cls_name+"."+method.__name__
    logger = logging.getLogger(cls_name)

    @wraps(method)
    def wrapped(*args, **kwargs):

        pos_args = map(str, args)
        named_args = map("{}={}".format, kwargs)
        arg_str = ", ".join(pos_args + named_args)

        call_str = "%s(%s)" % (log_name, arg_str)

        ts = time.time()
        try:
            logger.debug("[>>] %s" % (call_str))
            ret = method(*args, **kwargs)
            ts2 = time.time()
            logger.debug("[<<] %s => %s (took %.5f seconds)" % (call_str, ret, ts2-ts))
            return ret
        except:
            ts2 = time.time()
            logger.exception("[XX] %s (took %.5f seconds)" % (call_str, ts2-ts2))
            raise

    return wrapped


