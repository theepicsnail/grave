"""
Main robot entry point
"""
import connection
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    c = connection.Connection()
    c.connect("hashbang.sh", 7777)
    c.main_loop()

