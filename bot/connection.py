"""
Connection module.
This module kicks off the bot class.
"""
import socket
from irc import parse_message
from multiprocessing import Queue, Process
import threading
import bot
from queuereader import QueueReader
from logger import logged
@logged
class Connection(object):

    def __init__(self):
        self.sock = None
        self.running = True
        self.reader = None

    def handleDisconnect(self):
        # Replace this with reconnect logic
        self.tearDown()

    def __del__(self):
        self.tearDown()

    def tearDown(self):
        self.running = False
        self.sock.close()
        self.stop_consumer()

    def connect(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def send_data(self, msg):
        try:
            self.sock.send(msg + "\r\n")
        except:
            self.handleDisconnect()

    def start_consumer(self):
        """ Start up the bot process. """
        # I'm unsure if we can reuse the same queues.
        self.output_queue = Queue(100)
        self.input_queue = Queue(100)
        self.reader = QueueReader(self.input_queue, self.send_data)

        global bot
        bot = reload(bot)
        self.process = Process(target = bot.Bot,
            args=(self.output_queue, self.input_queue))
        self.process.start()

    def stop_consumer(self):
        self.output_queue.put(None)
        self.process.join(1)
        self.process.terminate()
        if self.reader:
            self.reader.end()

    def perform_handshake(self):
        self.input_queue.put("NICK testBot")
        self.input_queue.put("USER a b c d :e")

    def receive_data(self):
        try:
            data = self.sock.recv(1024)
        except:
            data = ""
        finally:
            if not data:
                self.tearDown()

        return data

    def main_loop(self):
        self.start_consumer()
        irc_buffer = ""
        data = ""
        self.perform_handshake()
        while self.running:
            irc_buffer += self.receive_data()
            lines = irc_buffer.split("\r\n")
            irc_buffer = lines[-1]

            for msg in lines[:-1]:
                self.process_line(msg)

    def process_line(self, msg):
        if msg.startswith(":snail!") and\
                ("NOTICE" in msg) and\
                msg.endswith(":restart"):
            self.stop_consumer()
            self.start_consumer()

        if msg.startswith("PING"):
            self.input_queue.put(msg.replace("I", "O"))

        self.broadcast(msg.strip())#parse_message(msg.strip()))

    def broadcast(self, irc_message):
        self.output_queue.put(irc_message)

