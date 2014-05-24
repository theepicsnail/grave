import multiprocessing
import socket
from irc import *
from multiprocessing import Queue
import threading
import sys
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
        global bot
        bot = reload(bot)
        self.process = multiprocessing.Process(target = bot.Bot,
            args=(self.output_queue, self.input_queue))
        self.process.start()

    def main_loop(self):
        self.start_consumer()
        b = ""
        self.sock.send("NICK testBot\r\nUSER a b c d :e\r\n")
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.sock.close()
                return

            b += data

            lines = b.split("\r\n")
            b=lines[-1]
            for msg in lines[:-1]:
                print >>sys.stderr, ">>%s" % msg.strip()
                if msg.startswith(":snail!") and ("NOTICE" in msg) and msg.endswith(":restart"):
                    print >>sys.stderr, "restarting"
                    self.output_queue.put(None)
                    self.process.join(1)
                    self.process.terminate()
                    self.start_consumer()
                    print >>sys.stderr, "restarted"

                self.output_queue.put(msg.strip())

    def __write(self):
        while True:
            data = self.input_queue.get()
            print >>sys.stderr, "<<%s" % data
            self.sock.send(data + "\r\n")


if __name__=="__main__":
    multiprocessing.freeze_support()
    Connection("hashbang.sh", 7777).main_loop()
