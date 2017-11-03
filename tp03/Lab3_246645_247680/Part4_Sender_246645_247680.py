import socket
import struct
import threading
import sys

MCAST_IP = "224.1.1.1"
PORT = 5005
MCAST_GRP = (MCAST_IP, PORT)



args = sys.argv[1:]
if (len(args) < 1):
    print("USAGE : python Part4_Sender_246645_247680.py sciper")
    sys.exit()

ID = args[0]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', PORT))

# join group
mreq = struct.pack("4sl", socket.inet_aton(MCAST_IP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# set IP_MULTICAST_TTL
ttl = struct.pack('b', 127)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


def listener():
    """Reading input packets."""
    while True:
      msg = sock.recv(65507)
      id = msg[:6].decode()
      rest = msg[6:].decode()
      print("READING FROM " + str(id))
      print("\t" + str(rest) + "\n")
      sys.stdout.flush()

def writer():
    while True:
        try:
            msg = input() # 'Message to send: '
            tosend = ID + msg
            #print("SENDING : ", tosend, "\n")
            sock.sendto(tosend.encode(), MCAST_GRP)
        except Exception as e:
            print(e)



threads = []
threads.append(threading.Thread(target=listener))
threads.append(threading.Thread(target=writer))

for t in threads:
    t.start()
