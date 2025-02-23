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

     data = conn.recv(1024).decode()
    print(f"Received from {addr[0]}: {data}")
    
    # write log in a file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{addr[0]} - {time.strftime('%Y-%m-%d %H:%M:%S')} - {data}\n") 
    
    client_last_log[addr[0]] = now  
    conn.send(b"Log received.\n")  # send the confirmation to client
    conn.close()

    def start_server(host, port):
    """Starts the logging server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #server starting
    server.bind((host, port))
    server.listen(5)
    print(f"Logging server started on {host}:{port}")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()