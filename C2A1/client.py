import socket
import argparse

parser = argparse.ArgumentParser(description='This is the client side code for multi threaded socket application')
parser.add_argument('--host', metavar='host', type = str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type = int, nargs='?', default=12000)
parser.add_argument('--filename', metavar='filename', type = str, nargs='?', default='/thegradcafe.com.html' )

args = parser.parse_args()

print(f"Connecting to Server: {args.host} on port: {args.port}")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((args.host, args.port))
        request = 'GET ' + args.filename + ' HTTP/1.1'
        s.send(request.encode())
        message = s.recv(102400).decode()
        print(message)

    except Exception as e:
        print(f'We have failed to connect with the host: {args.host} on port: {args.port} due to {e}')
        raise SystemExit()

