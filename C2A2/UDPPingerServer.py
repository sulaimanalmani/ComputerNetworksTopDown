import random
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 12000))

while True:
    rand = random.randint(0,10)
    message, addr = s.recvfrom(1024)
    message = message.upper()
    if rand < 4:
        continue
    s.sendto(message, addr)