import time
import inspect
from functools import wraps
import logging
import logging.config
import threading
import os
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import getLogger

def loadLogConfig():
    logging.config.fileConfig("logging/logging.cfg")
    print "Loaded logging config"
loadLogConfig()

    global loaded
    loaded = True
    getLogger().debug("debug")
    getLogger().info("info")
    getLogger().warn("warn")
    getLogger().error("error")
    getLogger().critical("critical")
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

#def getLogger(name=""):
#    calling_thread = threading.currentThread()
#    thread_name = calling_thread.getName()
#    thread_id = calling_thread.ident
#    pid = os.getpid()
#    log_name = "Process - %s.%s(%s)" % (
#        pid, thread_name, thread_id)
#    if name:
#        log_name += "." + name
#    return logging.getLogger()#log_name)


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
            #args[0].logger = logger
            ret = method(*args, **kwargs)
            ts2 = time.time()
            logger.debug("[<<] %s => %s (took %.5f seconds)" % (call_str, ret, ts2-ts))
            return ret
        except:
            ts2 = time.time()
            logger.exception("[XX] %s (took %.5f seconds)" % (call_str, ts2-ts2))
            raise

    return wrapped


