from socket import *

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(('',12000))
tcpSerSock.listen(5)

while True:
    print("Ready to serve...")
    tcpCliSock, addr = tcpSerSock.accept()
    print(f"Received connection from {addr}")
    message = tcpCliSock.recv(1024).decode()
    #alive = message.split().index
    alive = (message.split()[message.split().index('Connection:')+1] == 'keep-alive')
    print(alive)
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        f= open(filetouse[1:], "r",encoding="ISO-8859-1")
        output = f.readlines()
        fileExist = "true"
        for i in range(len(output)):
            tcpCliSock.send(output[i].encode())
        print("Read from cache")
    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            c.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            c.bind(('',12001))

            hostn = filename.replace("www.", "", 1)
            print(hostn)

            try:
                hostIP = gethostbyname(hostn)
                print(hostIP)
                c.connect((hostIP,80))
                req = "GET" + " / " + "HTTP/1.0\n\n"
                c.send(req.encode())
                data = b''
                while 1:
                    buffer = c.recv(1024)
                    if not buffer:
                        break
                    data += buffer
                tcpCliSock.sendall(data)
                tmpFile = open("./" + filename, mode= 'a+b')
                tmpFile.write(data)
            except Exception as e:
                print(f"Illegal request, Exception: {e}")
        else:
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n".encode())
    tcpCliSock.close()