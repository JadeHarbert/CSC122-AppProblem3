"""
chat-server.py -  Simulates a chatroom by awaiting a connection
                  to the hosted socket and passing messages back
                  and forth between client and server
Jade Harbert
CSC122
October 10th, 2022
"""


import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

isServerRunning = True

while isServerRunning:

    # Variable used to determine if the chat session is ending
    isConnected = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        # Await a connection
        s.listen()
        conn, addr = s.accept()
        with conn:
            def send_message(msg):
                """
                Send the msg parameter to the socket.

                :param msg: str
                    message to send to the socket
                """
                message = msg.encode()
                conn.sendall(message)

            def receive_message():
                """
                Receives messages from the socket and returns that.

                :return: str
                    Data received from socket
                """
                data = conn.recv(1024)
                return data.decode()

            print(f"connection from {addr}")
            print("Welcome to the chat room! \n"
                  "Type EXIT to end session \n"
                  "Type QUIT to close server \n"
                  "Put a period at the end of chat to pass baton to client\n\n"
                  "Waiting for response from client.\n"
                  )

            # While the chat session is still going
            while isConnected:

                # Receive message from client
                data = receive_message()
                if not data:
                    break

                # If the client wants to end the session, then we close the connection
                # We set isConnected to false, so we can go back to awaiting a connection
                if data == "EXIT":
                    isConnected = False
                    print("\nAwaiting another connection\n")
                    conn.close()

                # Else if the client doesn't want to end the session,
                # then we keep printing the clients messages
                else:
                    print("From Client: " + data)

                    # If the client hasn't passed the baton over to the server,
                    # then we keep receiving messages from the client
                    while data[-1] != ".":
                        data = receive_message()
                        if data == "EXIT":
                            isConnected = False
                            print("\nAwaiting another connection\n")
                            conn.close()
                            break
                        print("From Client: " + data)

                    if not isConnected:
                        break
                    msg = input("Enter Msg: ")

                    # If the user wants to close the server
                    if msg == "QUIT":

                        # Send message to client
                        send_message(msg)

                        isServerRunning = False
                        isConnected = False

                        # Close connection
                        conn.close()

                    # If the server wants to end the session
                    elif msg == "EXIT":

                        # Send message to client
                        send_message(msg)

                        # Close connection
                        conn.close()
                        print("\nAwaiting another connection\n")
                        isConnected = False
                    else:

                        # Keeps sending messages until the server is ready
                        # to pass the baton
                        while msg[-1] != ".":
                            send_message(msg)
                            if msg == 'EXIT':
                                conn.close()
                                print("\nAwaiting another connection\n")
                                isConnected = False
                                break
                            if msg == 'QUIT':
                                # Send message to client
                                send_message(msg)

                                isServerRunning = False
                                isConnected = False

                                # Close connection
                                conn.close()
                                break
                            msg = input("Enter Msg: ")

                        if isConnected:
                            send_message(msg)
