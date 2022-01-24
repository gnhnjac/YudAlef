import socket

sock = socket.socket()

ip = '127.0.0.1'
port = 3001

sock.connect((ip, port))

print(f'Connected to {ip} on port {port}')

data = input("Enter data to send: \n")

while data[:1] != 'q':

    sock.send(data.encode('utf-8'))
    print("Sent>>>", data)

    data = sock.recv(1024).decode('utf-8')
    if data == "":
        print("Server Disconnected")
        break
    print("Received<<<", data)
    data = input("Enter data to send: \n")
sock.close()

