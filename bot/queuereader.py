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
            print "Waiting..."
            val = self.queue.get()
            print "... got:" , val
            if self.running:
                self.callback(val)

    def end(self):
        self.running = False
        self.queue.put(None)



