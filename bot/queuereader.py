import threading

class QueueReader(object):
    def __init__(self, queue, callback):
        self.queue = queue
        self.callback = callback
        self.running = False
        self.thread = threading.Thread(target=self.__read)
        self.thread.start()

    def __read(self):
        self.running = True
        while self.running:

            print "queue reader", self.callback," waiting..."
            val = self.queue.get()
            print "...queue ", self.callback, "reader got:", val
            if self.running:
                print "calling callback", self.callback, val
                self.callback(val)
        print "queue reader exited."
    def end(self):
        print "queue reader delete"
        self.running = False
        self.queue.put(None)



