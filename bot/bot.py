import sys
from irc import parse_message
from queuereader import QueueReader

class Bot(object):
    def __init__(self, input_queue, output_queue):
        self.pending_rpcs = []
        self.output_queue = output_queue
        print "Bot started"
        self.send("PRIVMSG #! :test2")

        self.reader = QueueReader(input_queue, self.handle_line)

    def send(self, msg):
        self.output_queue.put(msg)

    def handle_line(self, line):
        print "Bot handle line:", line
        prefix, command, args = parse_message(line)


