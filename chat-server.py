# chat-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connection from {addr}")
        print("Welcome to the chat room! \n"
              "Waiting for response from client.\n"
              "Type EXIT to quit")
        while True:
            data = conn.recv(1024)
            data.decode()
            if not data:
                break
            print(data)
            msg = input("Enter Msg: ")
            msg = msg.encode()
            conn.sendall(msg)
