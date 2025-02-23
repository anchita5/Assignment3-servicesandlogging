<<<<<<< HEAD
import socket
import threading
import argparse
import time

client_last_log = {}
LOG_FILE = "logs.txt"
RATE_LIMIT = 1  

def handle_client(conn, addr):
    """Handles incoming log messages from clients."""
    global client_last_log
=======
import socket
import threading
import argparse
import time

client_last_log = {}
LOG_FILE = "logs.txt"
RATE_LIMIT = 1  

def handle_client(conn, addr):
    """Handles incoming log messages from clients."""
    global client_last_log
>>>>>>> a2e8eef53d1ae6d01962469a3e8071d18a6420d9
    now = time.time()