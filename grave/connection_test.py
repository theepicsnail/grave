"""Tests for connection"""
import unittest
import connection
from multiprocessing import Queue
from threading import Thread
from time import sleep

class FakeSocket(object):
    def __init__(self):
        self.sent = Queue(100)
        self.received = Queue(100)
    def get(self):
        """ Gets a message that was sent by this socket.
        This method returns what the server would have received."""
        return self.sent.get()

    def put(self, msg):
        """ Enqueues a message for the client to receive.
        This method simulates receiving data over a socket. """
        self.received.put(msg)

    def send(self, data):
        """ Socket interface for sending data to a client.
        This data is retreivable through .get()"""
        self.sent.put(data)

    def recv(self, length = 0):
        """ Socket interface for receiving data from a server.
        This data is seedable through .put() """
        return self.received.get()

    def close(self):
        self.sent.close()
        self.received.close()

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.connection = connection.Connection()
        self.connection.sock = FakeSocket()

    def tearDown(self):
        self.connection.tearDown()

    def testMainLoopStops(self):
        t = Thread(target = self.connection.main_loop)
        t.start()
        self.assertTrue(t.isAlive())
        self.connection.sock.put("") # End of data signal
#         Wait for the shutdown.
        sleep(0.001)
        self.assertFalse(t.isAlive())

    def testHandshake(self):
        t = Thread(target = self.connection.main_loop)
        t.start()
        self.assertEqual(self.connection.sock.get(), "NICK testBot\r\n")
        self.assertEqual(self.connection.sock.get(), "USER a b c d :e\r\n")
        self.connection.sock.put("PING 1234\r\n")
        self.assertEqual(self.connection.sock.get(), "PONG 1234\r\n")
        self.connection.sock.put("")






