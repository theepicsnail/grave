from irc import parse_message
from queuereader import QueueReader
from logger import logged

@logged
class Bot(object):

    def __init__(self, input_queue, output_queue):
        self.pending_rpcs = []
        self.output_queue = output_queue
        self.input_queue = input_queue

    def setUp(self):
        self.send("PRIVMSG #test :Started")
        self.reader = QueueReader(self.input_queue, self.handle_line)

    def tearDown(self):
        self.reader.end()
        self.send("PRIVMSG #test :Stopped")

    def send(self, msg):
        self.output_queue.put(msg)

    def handle_line(self, line):
        if line is None:
            self.tearDown()
            return

        prefix, command, args = parse_message(line)


