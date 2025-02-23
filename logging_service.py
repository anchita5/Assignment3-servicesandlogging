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
    print(f"Connected to {addr[0]}:{addr[1]}")
    now = time.time()
    
    
    if addr[0] in client_last_log and now - client_last_log[addr[0]] < RATE_LIMIT:
        msg = "Too many requests. Please wait.\n"
        print(f"Rate limit hit for {addr[0]}")  # print
        conn.send(msg.encode())  # send message to client
        conn.close()
        print(f"Disconnected from {addr[0]}")
        return