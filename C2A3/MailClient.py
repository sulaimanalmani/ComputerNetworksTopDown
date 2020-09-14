from socket import *
import argparse
import base64
import ssl

parser = argparse.ArgumentParser(description='This is an email client')
parser.add_argument('--emailfrom', metavar= 'email_from', type = str, nargs = '?')
parser.add_argument('--emailto', metavar= 'email_to', type = str, nargs = '?')
parser.add_argument('--passw', metavar= 'passw', type = str, nargs = '?')
parser.add_argument('--message', metavar= 'message', type = str, nargs = '?', default="I love computer networks!")

args = parser.parse_args()
email = str(base64.b64encode(args.emailfrom.encode()))[2:-1]
passw = str(base64.b64encode(args.passw.encode()))[2:-1]
msg = "\r\n " + args.message
endmsg = "\r\n"

mailserver = gethostbyaddr("smtp.mail.yahoo.com")[2][0]
serverPort = 587

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 12000))
s.settimeout(10)
s.connect((mailserver,serverPort))
s.send('starttls\r\n'.encode())
print(s.recv(1024).decode())
ss = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)

heloCommand = "HELO Localhost\r\n"
ss.send(heloCommand.encode())
recv1 = ss.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print("250 reply not received from server")

#Authenticating with into mail server
print(email)
print(passw)
ss.send("AUTH LOGIN\r\n".encode())
print(ss.recv(1024).decode())
ss.send(email.encode())
ss.send(endmsg.encode())
print(ss.recv(1024).decode())
ss.send(passw.encode())
ss.send(endmsg.encode())
print(ss.recv(1024).decode())

#Sending Mail
ss.send(f"MAIL FROM:<{args.emailfrom}>".encode())
ss.send(endmsg.encode())
print(ss.recv(1024).decode())
ss.send(f"RCPT TO:<{args.emailto}>".encode())
ss.send(endmsg.encode())
print(ss.recv(1024).decode())
ss.send("data".encode())
ss.send(endmsg.encode())
print(ss.recv(1024).decode())

ss.send(f"From: {args.emailfrom}\r\n"
        f"To: {args.emailto}\r\n"
        f"Subject: Test Email\r\n"
        f"{msg}\r\n\r\n.\r\n".encode())

print(ss.recv(1024).decode())
ss.send("quit".encode())
ss.send(endmsg.encode())