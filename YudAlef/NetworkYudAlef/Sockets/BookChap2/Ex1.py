import socket

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))


my_socket.send('Omer'.encode())
data = my_socket.recv(1024).decode()
print('The server sent: ' + data)

my_socket.close()