from bot.plugin import SimplePlugin
from time import time as cur_time
from time import mktime
import parsedatetime.parsedatetime as pdt

class Alarm(SimplePlugin):
    # Resources
    SCHEDULED = "Scheduled alarm."
    EXAMPLE = "!alarm 3 seconds#Example message"

    def setUp(self):
        super(Alarm, self).setUp()

        self.alarms = self.open_shelve()
        if 'queue' not in self.alarms:
            self.alarms['queue'] = []

        self.parser = pdt.Calendar()

        # Check for expired alarms once a second
        self.checker = self.schedule(self.check_alarms, seconds=1, repeat=True)

    def tearDown(self):
        super(Alarm, self).tearDown()
        self.alarms.close()
        self.checker.cancel()

    def parse_time(self, time):
        return mktime(self.parser.parse(time)[0])

    def check_alarms(self):
        if 'queue' not in self.alarms:
            return

        queue = self.alarms['queue']
        while queue:
            time, msg, location = queue[0]
            if time <= cur_time():
                self.msg(location, msg)
                queue.pop(0)
            else:
                break

        self.alarms['queue'] = queue

    def triggered(self, event):
        super(Alarm, self).triggered(event)
        if "#" not in event.message:
            self.msg(event.location, Alarm.EXAMPLE)
            return

        timespec, msg = event.message.split("#")
        time = self.parse_time(timespec)
        msg = event.sender +": " + msg

        queue = self.alarms['queue']
        queue.append((time, msg, event.location))
        queue.sort()
        self.alarms['queue'] = queue

        self.msg(event.location, Alarm.SCHEDULED)

    def usage(self, event):
        super(Alarm, self).usage(event)
        self.msg(event.location, Alarm.EXAMPLE)



