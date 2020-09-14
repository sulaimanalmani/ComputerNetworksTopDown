import random
from socket import *
import time
import select

serverip = 'localhost'
serverport = 12000
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('',12001))
s.settimeout(1000)

n = 0
start_time = time.time()
loss = 0
RTTs = []
for i in range(0, 9):
    current_time = time.time()
    n = (n+1) % 10
    print(f"sending ping {n}, at time t+{current_time-start_time}s")
    message = "ping"
    s.sendto(message.encode(), (serverip,serverport))

    ready = select.select([s], [], [], 1)
    if ready[0]:
        message, addr = s.recvfrom(1024)
        RTT = time.time() - current_time
        RTTs.append(RTT)
        print(f"Ping received. RTT: {RTT}s\n")
    else:
        print(f"Timeout for ping {n}\n")
        loss = loss + 1

    i = i + 1
print(f"Max RTT: {max(RTTs)}\nMin RTT: {min(RTTs)}\nAvg RTT: {sum(RTTs)/len(RTTs)}\n")
print(f"Loss = {loss*10}%")