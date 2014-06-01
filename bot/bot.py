from irc import parse_message
from queuereader import QueueReader
from logger import logged

@logged
class Bot(object):

    def __init__(self, input_queue, output_queue):
        self.pending_rpcs = []
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.setUp()

    def setUp(self):
        self.send("JOIN #test")
        self.send("PRIVMSG #test :Started")
        self.reader = QueueReader(self.input_queue, self.handle_line)

    def tearDown(self):
        self.send("PRIVMSG #test :Stopped")
        self.reader.end()

    def send(self, msg):
        self.output_queue.put(msg)

    def handle_line(self, line):
        print "Handle line:", line
        if line is None:
            self.tearDown()
            return
        prefix, command, args = line
        print "Bot:", prefix, command, args
        import sys
        sys.stdout.flush()

