"""
Connection module.
This module kicks off the bot class.
"""
import socket
from irc import parse_message
from multiprocessing import Queue, Process
import threading
import bot

class Connection(object):
    def __init__(self, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        self.sock = sock
        self.thread2 = threading.Thread(target = self.__write)
        self.output_queue = Queue(100)
        self.input_queue = Queue(100)
        self.thread2.start()

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
        print "Registering"
        self.sock.send("NICK testBot\r\nUSER a b c d :e\r\n")
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.sock.close()
                return

            irc_buffer += data

            lines = irc_buffer.split("\r\n")
            irc_buffer = lines[-1]
            for msg in lines[:-1]:
                print "loop:",msg
                if msg.startswith(":snail!") and\
                        ("NOTICE" in msg) and\
                        msg.endswith(":restart"):
                    self.output_queue.put(None)
                    self.process.join(1)
                    self.process.terminate()
                    self.start_consumer()

                if msg.startswithith("PING"):
                    self.input_queue.put(msg.replace("I", "O"))

                self.output_queue.put(parse_message(msg.strip()))

    def __write(self):
        while True:
            data = self.input_queue.get()
            self.sock.send(data + "\r\n")


