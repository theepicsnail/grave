from threading import Event
from threading import currentThread as thread
import time
import sys
sys.stdout = sys.stderr
class FakeTime(object):
    def __init__(self, start_time=0):
        self.epoch = start_time
        self.sleeping = set()

    def inc_time(self, length):
        self.set_time(self.time() + length)

    def set_time(self, timestamp):
        self.epoch = timestamp
        for e in set(self.sleeping):
            e.set()
    def time(self):
        return self.epoch

    def sleep(self, length):
        end = self.time() + length
        e = Event()
        self.sleeping.add(e)
        while self.time() < end:
            e.clear()
            e.wait()
        self.sleeping.remove(e)

from threading import Thread
class ScheduledEvent(object):
    def __init__(self, seconds, callback, repeat, sleep):
        self.seconds = seconds
        self.callback = callback
        self.repeat = repeat
        self.canceled = False
        self.sleep = sleep

        self.thread = Thread(target=self.loop)
        self.thread.start()

    def cancel(self):
        self.canceled = True

    def loop(self):
        while not self.canceled:
            if not self.repeat: # Not repeating, no more loops
                self.cancel()
            print "Sleep %s\n" % self.seconds
            self.sleep(self.seconds)
            print "Wake\n"
            self.callback()

class Scheduler(object):
    def __init__(self, time_module = time):
        """Create a scheduler.
        This accepts a time_module so that the real time module
        can be replaced with one better suited for testing.
        """
        self.sleep = time_module.sleep

    def schedule(self, callback, seconds=0, repeat=False):
        return ScheduledEvent(seconds, callback, repeat, self.sleep)



