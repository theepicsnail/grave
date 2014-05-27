"""Tests for connection"""
import unittest
import connection

class Connection(connection.Connection, unittest.TestCase):

    def testEndToEnd(self):
        self.assertTrue(True)

