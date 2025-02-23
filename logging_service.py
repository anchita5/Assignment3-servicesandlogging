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