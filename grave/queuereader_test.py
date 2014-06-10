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

    def testExceptionInCallback(self):
        data = []
        def callback(val):
            if val == "foo":
                raise Exception("exception")
            else:
                data.append(val)

        reader = queuereader.QueueReader(self.queue, callback)
        self.queue.put("a")
        self.queue.put("foo")
        self.queue.put("b")
        reader.end()
        self.assertEqual(data, ["a", "b"])

