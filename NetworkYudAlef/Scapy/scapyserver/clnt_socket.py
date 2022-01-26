import time

__author__ = 'Ami Kraizel'

import socket

sock = socket.socket()

print("Trying to connect")

sock.connect(('127.0.0.1', 135))

print("Connected successfully")

time.sleep(3)

sock.send(b'Hello from client')
print("Sent hello")
print('S:', sock.recv(100))
