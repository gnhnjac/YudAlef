import socket

sock = socket.socket()

ip = '0.0.0.0'
port = 3001
sock.bind((ip, port))

print(ip, "Running on port", port)

sock.listen(5)

while True:

    new_sock, address = sock.accept()

    while True:

        data = new_sock.recv(1024).decode('utf-8')
        if data == "":

            print('Client Disconnected')
            break

        print("Received<<<" + data)
        to_send = data.upper()

        new_sock.send(to_send.encode('utf-8'))
        print("Sent>>>" + to_send)

    new_sock.close()

sock.close()