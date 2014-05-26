"""
Main robot entry point
"""
import connection
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    connection.Connection("hashbang.sh", 7777).main_loop()
