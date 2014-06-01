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
        self.output_queue = Queue(100)
        self.input_queue = Queue(100)
        self.reader = QueueReader(self.input_queue, self.__send)

    def __del__(self):
        self.tearDown()

    def tearDown(self):
        self.reader.end()

    def connect(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def __send(self, msg):
        self.sock.send(msg + "\r\n")

    def start_consumer(self):
        """ Start up the bot process. """
        global bot
        bot = reload(bot)
        self.process = Process(target = bot.Bot,
            args=(self.output_queue, self.input_queue))
        self.process.start()

    def main_loop(self):
        self.start_consumer()
        irc_buffer = ""
        data = ""
        self.input_queue.put("NICK testBot")
        self.input_queue.put("USER a b c d :e")
        while True:
            try:
                data = self.sock.recv(1024)
            except:
                data = ""
            finally:
                if not data:
                    self.reader.end()
                    self.sock.close()
                    return

            irc_buffer += data

            lines = irc_buffer.split("\r\n")
            irc_buffer = lines[-1]
            for msg in lines[:-1]:
                if msg.startswith(":snail!") and\
                        ("NOTICE" in msg) and\
                        msg.endswith(":restart"):
                    self.output_queue.put(None)
                    self.process.join(1)
                    self.process.terminate()
                    self.start_consumer()

                if msg.startswith("PING"):
                    self.input_queue.put(msg.replace("I", "O"))

                self.output_queue.put(parse_message(msg.strip()))

