#pylint: disable=C0111
import shelve
from queuereader import QueueReader
from irc import parse_message
import threading

from collections import namedtuple
Event = namedtuple('Event', ['message', 'location', 'sender'])

#Some mixins to make plugins more rich
from threading import Timer
class Scheduler(object):
    def schedule(self, callback, seconds=0, repeat=False):
        class Canceller(object):
            def start_timer(self, timer):
                self.timer = timer
                timer.start()

            def cancel(self):
                self.timer.cancel()

        c = Canceller()

        # Create a wrapper with the loop logic
        def wrapper():
            if repeat:
                c.start_timer(Timer(seconds, wrapper))
            callback()

        # Start it
        c.start_timer(Timer(seconds, wrapper))
        return c

class IrcActions(object):
    def msg(self, location, msg):
        self.send_raw("PRIVMSG {} {}".format(location, msg))

    def send_raw(self, line):
        raise NotImplementedError(
            "send_raw must be defined to perform IrcActions")


# Shelve providers
# fake_shelve - in memory shelve
from collections import defaultdict
class FakeShelve(dict):
    def close(self):
        pass
    def sync(self):
        pass
__fake_shelves = defaultdict(FakeShelve)
def fake_shelve(name):
    return __fake_shelves[name]

# disk_shelve - on disk shelve
def disk_shelve(name):
    return shelve.open("data/" + name)


#Main pluin class
class Plugin(Scheduler, IrcActions):

    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        # Default factories
        self.set_shelve_factory(disk_shelve)

    # Shelve utility
    def set_shelve_factory(self, shelve_factory):
        self.shelve_factory = shelve_factory

    def open_shelve(self, name=""):
        pkl_ident = self.__class__.__name__
        if name:
            pkl_ident += "." + name
        return self.shelve_factory(pkl_ident)

    def setUp(self):
        """Called once the bot is ready to load this plugin"""
        pass

    def tearDown(self):
        self.reader.end()

    def set_pipes(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.reader = QueueReader(input_queue, self.on_raw)

    def send_raw(self, line):
        try:
            self.output_queue.put(line, timeout=1)
        except:
            print type(self), "send_raw had an exception on:"
            print "line:", line
            import traceback, sys
            traceback.print_exc(file=sys.stdout)

    def on_raw(self, raw_line):
        """Each line the bot gives this plugin enters here"""
        pass

#Convenience subclass
class SimplePlugin(Plugin):
    """Simple plugins are plugins that are triggered by:
    channel(or private message): !<classname> <arg string>

    TODO "or <botname> <classname> <arg string>"

    """
    def __init__(self, *args, **kwargs):
        super(SimplePlugin, self).__init__(*args, **kwargs)
        self.command_prefix = type(self).__name__.lower()
        print "init ", self

    def on_raw(self, raw_line):
        super(SimplePlugin, self).on_raw(raw_line)
        prefix, command, args = parse_message(raw_line)
        if command != 'PRIVMSG':
            return
        print "on_raw", self
        msg = args[-1]
        if not msg[1:].startswith(self.command_prefix):
            return

        if ' ' in msg:
            cmd, msg = msg.split(' ', 1)
        else:
            cmd, msg = msg, ''
        who = prefix.split("!")[0]
        evt = Event(message=msg, location=args[0], sender=who)
        { # Prefix to handler map
        "!": self.triggered,
        "?": self.usage
        }[cmd[0]](evt) #execute

    def triggered(self, event):
        pass

    def usage(self, event):
        self.msg(event.location, "No usage for !{} provided.".format(
            self.command_prefix))


