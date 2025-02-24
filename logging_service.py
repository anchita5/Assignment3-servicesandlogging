#File: logging_Server.py
#Project: Assignment 2 - NAD
# Prpgrammer: Anchita Kakria, Uttam Arora
# Date: 23 Feb 2025
# Desc: This script impements a logging server which will take on the messages
#       sent by the client. 

import socket
import threading
import argparse
import time

# rate limiting
client_last_log = {}
LOG_FILE = "logs.txt"
RATE_LIMIT = 1  # 1 second between logs per client

# Function: handle_client
#Desc: This function will handle the messages from clients and writes into a file
# Parameter: conn, addr
#return: none

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
    
    # receive log message
    data = conn.recv(1024).decode()
    print(f"Received from {addr[0]}: {data}")
    
    # write log in a file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{addr[0]} - {time.strftime('%Y-%m-%d %H:%M:%S')} - {data}\n")
    
    client_last_log[addr[0]] = now  # update timestamp
    conn.send(b"Log received.\n")  # send the confirmation to client
    conn.close()

#Function: start_server
#Desc: This function starts the server and accepts the connection and handles the clients
# Parameters: host, port
#Returns: none

def start_server(host, port):
    """Starts the logging server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Logging server started on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Logging Service")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    parser.add_argument("--format", default="{ip} - {timestamp} - {message}", help="Log message format")
    args = parser.parse_args()
    
    start_server(args.host, args.port)
