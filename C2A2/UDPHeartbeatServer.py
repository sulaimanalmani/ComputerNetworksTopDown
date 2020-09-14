import random
from socket import *
import time
import select

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 12000))

loss = 0
pings = []
times = []
last_ping_index = 0
last_ping_time = 0
while True:
    ready = select.select([s], [], [], 3)
    if ready[0]:
        message, addr = s.recvfrom(1024)
        message = message.decode().split(sep=' ')

        current_ping_index = int(message[1])
        loss = loss + (current_ping_index - last_ping_index - 1)
        print(f"Loss: {(loss/current_ping_index)*100}%")
        last_ping_index = current_ping_index
        
        current_ping_time = float(message[3])
        td = current_ping_time - last_ping_time
        print(f"Time Difference: {td}\n")
        last_ping_time = current_ping_time

    else:
        break
print("Client heartbeat stopped")

