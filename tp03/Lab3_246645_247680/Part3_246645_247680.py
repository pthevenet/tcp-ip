import sys
import socket
import re
import select
import datetime


HOST = "lab3.iew.epfl.ch"
PORT = 5004


# Command to send
cmd = "RESET:20"
msg = cmd.encode()

# Response type
response = re.compile("^OFFSET=\d+$")


sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock6.setblocking(0)
sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock4.setblocking(0)
received = False

while not received:
    sock6.sendto(msg, (HOST, PORT))
    sock4.sendto(msg, (HOST, PORT))
    ready = select.select([sock4, sock6], [], [], 1)[0] # reading, writing, exception
    if ready:
        response = ready[0].recv(65507).decode()
        print(datetime.datetime.now())
        print(response)
        received = True

        if (ready[0] == sock6):
            print("Received using IPv6")
        else:
            print("Received using IPv4")

    else:
        print("timeout")
