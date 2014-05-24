from bot.testing import SimpleTest
from plugins import alarm

class Alarm(alarm.Alarm, SimpleTest):

    def testEndToEnd(self):
        self.simulate_msg("user", "#room", "!alarm now#msg")
        self.assert_msg("#room", Alarm.SCHEDULED)
        self.assert_msg("#room", "user: msg")

    def testUsage(self):
        self.simulate_msg("user", "#room", "?alarm")
        self.assert_msg("#room", Alarm.EXAMPLE)

    def testAutoExample(self):
        self.simulate_msg("user", "#room", "!alarm adfadf")
        self.assert_msg("#room", Alarm.EXAMPLE)

