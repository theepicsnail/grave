import threading

class QueueReader(object):
    def __init__(self, name, queue, callback):
        self.queue = queue
        self.callback = callback
        self.thread = threading.Thread(target=self.__read)
        self.thread.start()
        self.running = False

    def __read(self):
        self.running = True
        while self.running:
            val = self.queue.get()
            if self.running:
                self.callback(val)

    def __del__(self):
        self.running = False
        self.queue.put(None)


