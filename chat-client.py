"""
chat-client.py -  Simulates a chatroom by connecting to a
                  socket that is hosted by chat-server.py and passes
                  messages back and forth between client and server
Jade Harbert
CSC122
October 10th, 2022
"""
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))


    def send_message(msg):
        """
        Send the msg parameter to the socket.

        :param msg: str
            Message to send to the socket
        """
        message = msg.encode()
        s.sendall(message)

    def receive_message():
        """
        Receive message from the socket and returns that.

        :return: str
            Data received from socket
        """
        data = s.recv(1024)
        return data.decode()


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
            send_message(msg)
            break

        # If the client isn't ready to pass the baton,
        # then we keep sending messages
        while msg[-1] != ".":
            if msg == "EXIT":
                break
            send_message(msg)
            msg = input("Enter Msg: ")

        if msg == 'EXIT':
            send_message(msg)
            break
        else:
            send_message(msg)
        # Receives message from server
        data = receive_message()

        # Checks to make sure the server doesn't want to quit or exit
        if data != "EXIT" and data != "QUIT":

            # If the server hasn't passed the baton to the client,
            # then we continuously print messages from the server
            while data[-1] != ".":
                if data == 'EXIT' or data == 'QUIT':
                    s.close()
                    isConnected = False
                    break
                print("From Server: " + data)
                data = receive_message()

        # If the server wants to end the chat session, then we close the connection
        # We also set the connection variable to false so the program ends
        if data == "EXIT" or data == "QUIT":
            s.close()
            isConnected = False
        else:
            print("From Server:" + data)
