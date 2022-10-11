# chat-server.py
# Jade Harbert
# CSC122
# October 10th, 2022

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
            print(f"connection from {addr}")
            print("Welcome to the chat room! \n"
                  "Type EXIT to end session \n"
                  "Type QUIT to close server \n"
                  "Put a period at the end of chat to send message\n\n"
                  "Waiting for response from client.\n"
                  )

            # While the chat session is still going
            while isConnected:

                # Receive message from client
                data = conn.recv(1024)
                data = data.decode()
                if not data:
                    break

                # If the client wants to end the session, then we close the connection
                # We set isConnected to false, so we can go back to awaiting a connection
                if data == "EXIT":
                    isConnected = False
                    print("\nAwaiting another connection\n")
                    conn.close()

                else:
                    print("From Client: " + data)
                    msg = input("Enter Msg: ")

                    # If the user wants to close the server
                    if msg == "QUIT":

                        # Send message to client
                        msg = msg.encode()
                        conn.sendall(msg)

                        isServerRunning = False
                        isConnected = False

                        # Close connection
                        conn.close()

                    # If the server wants to end the session
                    elif msg == "EXIT":

                        # Send message to client
                        msg = msg.encode()
                        conn.sendall(msg)

                        # Close connection
                        conn.close()
                        print("\nAwaiting another connection\n")
                        isConnected = False
                    else:

                        # Checks to see if the client wants to send their message.
                        # Continuously asks for input until the client is ready to send
                        while msg[-1] != ".":
                            msg += "\n\t\t\t" + input()

                        # Send message to client
                        msg = msg.encode()
                        conn.sendall(msg)


