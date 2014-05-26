import unittest
from collections import defaultdict
from multiprocessing import Queue

class FakeShelve(dict):
    def close(self):
        pass
    def sync(self):
        pass

class SimpleTest(unittest.TestCase):
    def __init__(self, *a):
        super(SimpleTest, self).__init__(*a)
        print "simple test init"
        self.write_pipe = Queue() # write here, plugin will read it
        self.read_pipe = Queue()  # read here, plugin writes to this
        self.set_pipes(self.write_pipe, self.read_pipe)
        self.__fake_shelves = defaultdict(FakeShelve)

    def set_pipes(self, input_queue, output_queue):
        print "simple test set_pipes"
        raise NotImplementedError()

    def simulate_msg(self, who, where, what):
        print "simulate msg:", who, where, what, self.write_pipe
        self.write_pipe.put(":{}!user@host PRIVMSG {} :{}".format(
            who, where, what))

    def assert_msg(self, where, msg):
        print "assert msg:", where, msg
        self.assertEqual(self.read_pipe.get(timeout=2),
            "PRIVMSG {} {}".format(where, msg))

    def __del__(self):
        print "simple test del"

    def setUp(self):
        super(SimpleTest, self).setUp()

    def tearDown(self):
        super(SimpleTest, self).tearDown()

    # Override the shelve returned in the plugin.
    def open_shelve(self, name=""):
        return self.__fake_shelves[name]

