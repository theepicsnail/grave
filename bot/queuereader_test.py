import unittest
import queuereader
import multiprocessing

class QueueReaderTest(unittest.TestCase):

    def setUp(self):
        self.queue = multiprocessing.Queue()

    def testQueueReaderEnds(self):
        def callback(val):
            pass
        reader = queuereader.QueueReader(self.queue, callback)
        reader.end()

