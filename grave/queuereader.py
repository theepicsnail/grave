""" queuereader.py
Read from a multiprocessing queue, and call a callback with the
retreived data.
"""
import threading
import logger

class QueueReader(object):
    """ Async reader for multiprocessing.queues.
    Given a callback, call the callback with each item pulled from the queue.
    """
    def __init__(self, queue, callback):
        self.queue = queue
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self.__read)
        self.thread.start()
        self.log = logger.getLogger()

    def __read(self):
        """ Main loop, started on another thread.
        Consume the queue, calling the callback on each item"""
        while self.running:
            val = self.get()
            if self.running:
                try:
                    self.callback(val)
                except:
                    self.log.exception("Exception while calling {} with value \"{}\"".format(
                        self.callback, val))


    def get(self):
        return self.queue.get()

    def end(self):
        """ Shut down the queue reader. """
        self.running = False
        self.queue.put(None)



