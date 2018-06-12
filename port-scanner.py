"""
    Multithreaded port scanner: re-implementation of http://www.pythonforbeginners.com/ Tutorial, and using techniques
    from another tutorial https://code.tutsplus.com/articles/introduction-to-parallel-and-concurrent-programming-in-python--cms-28612
"""

import socket
import subprocess
import sys, os
from datetime import datetime
from queue import Queue
from threading import Thread
from time import sleep
# Detetcts the number of cores
NUM_WORKERS = os.cpu_count()
task_queue = Queue()
# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer    = input("Enter a remote host to scan: ")
remoteServerIP  = socket.gethostbyname(remoteServer)

port_list = [port for port in range(1, 51)]

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((remoteServerIP, port))
    if result == 0:
        print ("Port {}: 	 Open".format(port))
    sock.close()


def worker():
    while True:
        port = task_queue.get()
        check_port(port)
        task_queue.task_done()
def main():

    # Print a nice banner with information on which host we are about to scan
    print ("-" * 60)
    print ("Please wait, scanning remote host", remoteServerIP)
    print ("-" * 60)

    # Check what time the scan started
    t1 = datetime.now()

    # Using the range function to specify ports (here it will scans all ports between 1 and 1024)

    # We also put in some error handling for catching errors

    try:
        threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
        for thread in threads:
            thread.daemon = True
        [task_queue.put(port) for port in port_list]
        [thread.start() for thread in threads]
        task_queue.join()

    except KeyboardInterrupt:
        print ("\nYou pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print ("Couldn't connect to server")
        sys.exit()

    # Checking the time again
    t2 = datetime.now()

    # Calculates the difference of time, to see how long it took to run the script
    total =  t2 - t1

    # Printing the information to screen
    print ('Scanning Completed in: ', total)
if __name__ == '__main__':
    main()
