import socket
import datetime
import random

srv_socket = socket.socket()

srv_socket.bind(('0.0.0.0', 1234))

print("Server is up and running!")
srv_socket.listen()

clnt_socket, clnt_address = srv_socket.accept()

data = clnt_socket.recv(1024).decode()

while(data != 'EXIT'):

    if data == 'TIME':
        clnt_socket.send(f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'.encode())

    elif data == 'WHOU':
        clnt_socket.send("I am Ami's cute server".encode())

    elif data == 'RAND':
        clnt_socket.send(str(random.randint(1,10)).encode())

    else:
        clnt_socket.send('Unrecognized command...'.encode())

    data = clnt_socket.recv(1024).decode()

clnt_socket.close()


srv_socket.close()