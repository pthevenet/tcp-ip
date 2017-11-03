import websocket
import sys

args = sys.argv[1:]
if (len(args) < 1):
    print("USAGE : python Part5_246645_247680.py command")
    sys.exit()

cmd = args[0]

ws = websocket.create_connection("ws://tcpip.epfl.ch:5006")

# Sending cmd
print("SENDING : ", cmd)
ws.send(cmd)

# Listening
cnt = 0
try:

    while True:
        # Receiving
        result =  ws.recv().decode()
        cnt += 1
        print(result)
except:
    ws.close()


print(cnt, "calls to recv")
