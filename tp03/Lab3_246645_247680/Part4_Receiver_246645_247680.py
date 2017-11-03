import socket
import struct

MCAST_GRP = "224.1.1.1"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  msg = sock.recv(65507)
  #print(msg.decode())
  id = msg[:6].decode()
  rest = msg[6:].decode()
  print("id : " + str(id))
  print("message : \n" + str(rest))
