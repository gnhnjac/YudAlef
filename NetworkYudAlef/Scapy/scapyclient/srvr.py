__author__ = 'Ami Kraizel'

import socket

sock = socket.socket()

sock.bind(('0.0.0.0',135))

sock.listen()

print("listening...")

clnt,addr = sock.accept()
print("Connection made with", addr)
clnt.recv(100)