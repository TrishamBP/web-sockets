import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on the same machine
s.connect((socket.gethostname(), 1234))
# Connect to a server on a different machine
# s.connect(('<server_ip_address>', 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:

        msg = s.recv(16) # Buffer size is 1024 bytes
        if new_msg:
            print(f"New message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            print("Full message received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''
        