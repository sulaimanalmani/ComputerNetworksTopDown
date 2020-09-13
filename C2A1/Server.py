from socket import *
import argparse
import threading

parser = argparse.ArgumentParser(description='This is the Server side code for multi threaded socket application')
parser.add_argument('--host', metavar='host', type = str, nargs='?', default=gethostname())
parser.add_argument('--port', metavar='port', type = int, nargs='?', default=12000)
args = parser.parse_args()

print(f"Creating Server at: {args.host} on port: {args.port}")

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverName = args.host
port = args.port
s.bind(('', port))
s.listen(5)

def on_new_client(connectionSocket, addr):
    print('process started')
    print(f"connected to client at ip: {addr[0]} and socket{addr[1]}")
    while True:
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split(sep=' ')[1] if message != '' else ''
            print(f"{filename} is requested by client")
            f = open(filename[1:])

            if filename.split(sep='.')[-1] != 'html':
                connectionSocket.send('HTTP/1.1 404 Not Found'.encode())
                break
            outputdata = f.read()
            output_message = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + outputdata
            connectionSocket.send(output_message.encode())
            break
        except IOError:
            connectionSocket.send('HTTP/1.1 404 Not Found'.encode())
            break
        except Exception as e1:
            SystemExit(f"Exception: {e1}")
    print(f'Served the client ip: {addr[0]} and socket{addr[1]}\n')
    connectionSocket.close()


while True:
    try:
        print('READY TO SERVE')
        connectionSocket, addr = s.accept()
        threading._start_new_thread(on_new_client, (connectionSocket, addr,))
    except KeyboardInterrupt:
            SystemExit()
    except Exception as e:
        print(f"Exception : {e}")

s.close()
