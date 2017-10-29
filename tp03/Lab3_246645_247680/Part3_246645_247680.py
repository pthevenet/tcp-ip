import sys
import socket
import re
import select


HOST = "lab3.iew.epfl.ch"
PORT = 5004


# Command to send
cmd = "RESET:20"
msg = cmd.encode()

# Response type
response = re.compile("^OFFSET=\d+$")


def run(sock):
    sock.setblocking(0)
    received = False
    while not received:
        # send and timemout
        sock.sendto(msg, (HOST, PORT))
        ready = select.select([sock], [], [], 1) # reading, writing, exception, timeout
        if ready[0]:
            data = sock.recv(65507).decode()
            if re.match(response, data):
                # got valid response
                received = True # stop looping
                print("Received : " + data)



try:
    # IPv6 / UDP
    sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    run(sock6)
except:
    print()

try:
    # IPv4 / UDP
    sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run(sock4)
except:
    print()
