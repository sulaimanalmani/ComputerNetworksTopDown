import random
from socket import *
import time
import select

serverip = 'localhost'
serverport = 12000
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('',12001))

n = 0
start_time = time.time()
while True:
    n = n + 1
    if random.randint(0,10) > 3:
        s.sendto(f"ping: {n} time: {time.time() - start_time}".encode(),(serverip, serverport))
    else:
        continue