import unittest
from collections import defaultdict
from multiprocessing import Queue
from plugin import fake_shelve


class SimpleTest(unittest.TestCase):
    plugins = []

    def __init__(self, *a):
        super(SimpleTest, self).__init__(*a)

        self.write_pipe = Queue(100) # write here, plugin will read it
        self.read_pipe = Queue(100)  # read here, plugin writes to this

        self.instances = [p() for p in self.plugins]
        for plugin in self.instances:
            plugin.set_pipes(self.write_pipe, self.read_pipe)
            plugin.set_shelve_factory(fake_shelve)

    def setUp(self):
        for plugin in self.instances:
            plugin.setUp()

    def tearDown(self):
        for plugin in self.instances:
            plugin.tearDown()

    def __del__(self):
        for plugin in self.instances:
            del plugin

    def simulate_msg(self, who, where, what):
        self.write_pipe.put(":{}!user@host PRIVMSG {} :{}".format(
            who, where, what))

    def assert_msg(self, where, msg):
        self.assertEqual(self.read_pipe.get(timeout=2),
            "PRIVMSG {} {}".format(where, msg))


