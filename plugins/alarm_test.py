from grave.testing import SimpleTest
from plugins.alarm import Alarm

class Test(SimpleTest):
    plugins = [Alarm]

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



