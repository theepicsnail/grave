import unittest
import plugin
import time

class SchedulerTest(unittest.TestCase):

    def setUp(self):
        self.sched = plugin.Scheduler()


    def testScheduleNonBlocking(self):
        val = [1]
        def callback():
            val.append(2)

        self.sched.schedule(callback, .1)
        val.append(3)
        time.sleep(.2)
        self.assertEqual(val, [1, 3, 2])





