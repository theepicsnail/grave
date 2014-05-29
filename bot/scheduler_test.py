import unittest
import scheduler
from threading import Event
import time
import sys
sys.stdout = sys.stderr
class SchedulerTest(unittest.TestCase):

    def setUp(self):
        self.time = scheduler.FakeTime()
        self.sched = scheduler.Scheduler(self.time)
        self.event = Event()
    def _testScheduleWaitsFirst(self):
        val = [1]

        self.event.clear()
        def callback():
            val.append(2)
            print "callback %s\n" % val,

        self.sched.schedule(callback, 1)

        val.append(3)

        val.append(2)
        self.time.inc_time(1)
        time.sleep(2)
        self.assertEqual(val, [1, 3, 2])

    def testParallelScheduled(self):
        val = []
        def callback2():
            val.append(2)
        def callback3():
            val.append(3)

        self.time.set_time(0)
        cb2 = self.sched.schedule(callback2, 2, True)
        cb3 = self.sched.schedule(callback3, 3, True)
        time.sleep(.001) # Wait for schedulers to be started
        try:
            expected_length = 0
            for t in xrange(1, 100):
                self.time.inc_time(1)
                time.sleep(.001) # Wait for callbacks to be called
                if t % 2 == 0:
                    expected_length += 1
                if t % 3 == 0:
                    expected_length += 1
                self.assertEqual(expected_length, len(val))
        finally:
            cb2.cancel()
            cb3.cancel()
            self.time.inc_time(3) # triggers both cb2 and cb3 to update
