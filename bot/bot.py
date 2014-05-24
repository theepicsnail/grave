import sys
from irc import parse_message

class Bot(object):
    def __init__(self, input_queue, output_queue):
        print >>sys.stderr, "bot started"
        self.pending_rpcs = []
        self.output_queue = output_queue

        self.send("PRIVMSG #! :test")

        while True:
            data = input_queue.get()
            if data == None:
                print >>sys.stderr, "bot caught end signal"
                return
            self.handle_line(data)

    def send(self, msg):
        self.output_queue.put(msg)

    def handle_line(self, line):
        print >>sys.stderr, "Handle line"
        prefix, command, args = parse_message(line)
        print >>sys.stderr, "P:",prefix, "C:",command, "A:",args
        if command == "PING":
            self.send("PONG " + args[0])


