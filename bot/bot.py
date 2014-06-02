from irc import parse_message
from queuereader import QueueReader
from logger import logged
from threading import Event

@logged
class Bot(object):

    def __init__(self, input_queue, output_queue):
        self.running = True
        self.pending_rpcs = []
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.event = Event()
        self.setUp()
        self.mainloop()

    def setUp(self):
        self.send("JOIN #test")
        self.send("PRIVMSG #test :Started")
        self.reader = QueueReader(self.input_queue, self.handle_line)

    def tearDown(self):
        self.send("PRIVMSG #test :Stopped")
        self.reader.end()
        self.running = False
        self.event.set()

    def send(self, msg):
        self.output_queue.put(msg)

    def handle_line(self, line):
        if line is None:
            self.tearDown()
            return
        prefix, command, args = parse_message(line)
        print "Bot:", prefix, command, args

    def mainloop(self):
        # Deal with plugin io here.
        while self.running:
            self.event.wait()
            self.event.clear()
