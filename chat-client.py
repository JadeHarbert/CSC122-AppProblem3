# chat-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Welcome to the chat room! \nType EXIT to quit")
    while True:
        msg = input("Enter Msg: ")
        if msg == "EXIT":
            break
        msg = msg.encode()
        s.sendall(msg)
        data = s.recv(1024)
        data = data.decode()

        if data == "EXIT":
            break
        print(data)
