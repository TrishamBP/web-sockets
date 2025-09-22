import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
s.bind((socket.gethostname(), 1234))

# Listen for incoming connections
s.listen(5)

while True:
    # Accept a connection
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    # Send a message to the client
    clientsocket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f'The time is {time.time()}'
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg, "utf-8"))
         # Send a message to the client
        clientsocket.send(bytes(msg, "utf-8"))


