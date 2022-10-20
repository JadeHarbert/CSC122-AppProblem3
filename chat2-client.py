# chat-client.py -  Simulates a chatroom by connecting to a
#                   socket that is hosted by chat-server.py and passes
#                   messages back and forth between client and server
# Jade Harbert
# CSC122
# October 10th, 2022

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Variable used to determine if the chat session is ending
    isConnected = True

    print("Welcome to the chat room! \n"
          "Type EXIT to end session \n"
          "Put a period at the end of chat to pass the baton to server")

    # While the chat session is still going
    while isConnected:
        msg = input("Enter Msg: ")

        # If the client wants to end the session
        if msg == "EXIT":
            msg = msg.encode()
            s.sendall(msg)
            break

        # Sends message
        while msg[-1] != ".":
            msg = msg.encode()
            s.sendall(msg)
            msg = input("Enter Msg: ")

        msg = msg.encode()
        s.sendall(msg)

        # Receives message from server
        data = s.recv(1024)
        data = data.decode()
        if not data:
            break

        while data[-1] != ".":
            print("From Server: " + data)
            data = s.recv(1024)
            data = data.decode()
            if not data:
                break

        # If the server wants to end the chat session, then we close the connection
        # We also set the connection variable to false so the program ends
        if data == "EXIT" or data == "QUIT":
            s.close()
            isConnected = False
        else:
            print("From Server:" + data)
