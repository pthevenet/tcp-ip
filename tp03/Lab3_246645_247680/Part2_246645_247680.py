import socket
import sys
import re

HOST = "tcpip.epfl.ch"
PORT = 5003
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))


args = sys.argv[1:]
if (len(args) < 1):
    print("USAGE : python pdc.py command")
    sys.exit()


commands = args

floodme_cmd = re.compile("^CMD_floodme$")
short_cmd = re.compile("^CMD_short:\d+$")
short_response = re.compile("^This is PMU data \d+$")

for cmd in commands:
    if re.match(floodme_cmd, cmd):
        cnt = 0
        print("sending:", cmd)
        sock.sendall(cmd.encode())

        data = ""
        while True:
            new = sock.recv(18).decode()
            if new:
                cnt += 1
                data += new
            elif not new:
                print(data)
                break

        print(data)
        print("In : " + str(cnt) + " recv calls.")

    elif re.match(short_cmd, cmd) :
        print("sending:", cmd)
        sock.sendall(cmd.encode())

        data = ""
        while True:
            data += sock.recv(1).decode()
            if data and re.match(short_response, data):
                print(data)
                data = ""
            elif not data:
                print("No more data from")
                break
