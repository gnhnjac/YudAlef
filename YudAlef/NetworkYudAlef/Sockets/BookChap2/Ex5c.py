import socket

clnt_socket = socket.socket()

clnt_socket.connect(('127.0.0.1', 1234))

print("Connected to server")

while True:

    data = input("Enter Command: \n")

    clnt_socket.send(data.encode())

    res = clnt_socket.recv(1024).decode()
    print(res)

    if data == 'EXIT':
        break

clnt_socket.close()