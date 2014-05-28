import unittest
import sys
from StringIO import StringIO

class OutputLogger(object):
    def __init__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.new_stdout = StringIO()
        self.new_stderr = StringIO()

        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

    def __enter__(self):
        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr
        self.new_stdout.truncate(0)
        self.new_stderr.truncate(0)
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def getStdout(self):
        self.new_stdout.seek(0)
        return self.new_stdout.read()

    def getStderr(self):
        self.new_stderr.seek(0)
        return self.new_stderr.read()

OUTPUT_LOGGER = OutputLogger() # Must be started before logger is imported.
import logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log = logger.get_logger()

    def produce_logs(self):
        with OUTPUT_LOGGER:
            self.log.debug("debug")
            self.log.info("info")
            self.log.warn("warn")
            self.log.critical("critical")
            self.log.error("error")

    def testDefaultLogger(self):
        self.produce_logs()
        stdout = OUTPUT_LOGGER.getStdout().strip() # trailing newline
        self.assertEqual(len(stdout.split("\n")), 5)

    def testLevel(self):
        self.log.setLevel(logger.INFO)
        self.produce_logs()
        stdout = OUTPUT_LOGGER.getStdout().strip() # trailing newline
        self.assertEqual(len(stdout.split("\n")), 4)

    def testDifferentLoggers(self):
        self.produce_logs() # produce 5 traces with 'root'
        self.assertEqual(OUTPUT_LOGGER.getStdout().count('root'), 5)

        self.log = logger.get_logger('other')
        self.produce_logs() # produce 5 traces with 'other'
        self.assertEqual(OUTPUT_LOGGER.getStdout().count('other'), 5)



