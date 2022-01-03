import base64, socket,os

def smtp_recv(sock):

    data = b''

    while b'\r\n' not in data:

        _d = sock.recv(1)

        if _d == b'':

            return b''

        data += _d

    return data

def log_recv(data):
    print('S: ', end='')
    print(data)

def send_smtp(sock,data):

    print("C: ",end='')
    print(data.encode())
    sock.send(data.encode())

def main():

    sock = socket.socket()

    sock.connect(('172.66.42.230', 25))

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    log_recv(smtp_recv(sock))
    send_smtp(sock,f'EHLO {local_ip}\r\n')
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))
    log_recv(smtp_recv(sock))

    send_smtp(sock, 'AUTH LOGIN\r\n')
    log_recv(smtp_recv(sock))
    send_smtp(sock, f'{base64.b64encode(input("USERNAME: ").encode()).decode()}\r\n')
    log_recv(smtp_recv(sock))
    send_smtp(sock, f'{base64.b64encode(input("PASSWORD: ").encode()).decode()}\r\n')
    log_recv(smtp_recv(sock))
    send_smtp(sock, f'MAIL FROM:<{input("ENTER EMAIL: ")}>\r\n')
    log_recv(smtp_recv(sock))

    inp = input('ENTER RECIPIENT: ')

    if (inp == ''):
        send_smtp(sock, f'RCPT TO:random@gmail.com\r\n')
        log_recv(smtp_recv(sock))

    while (inp != ''):
        send_smtp(sock, f'RCPT TO:{inp}\r\n')
        log_recv(smtp_recv(sock))
        inp = input('ENTER RECIPIENT: ')

    send_smtp(sock, f'DATA\r\n')
    log_recv(smtp_recv(sock))

    send_smtp(sock, f'Subject: {input("Enter Subject: ")}\r\n\r\n{input("Enter Message: ")}\r\n.\r\n')
    log_recv(smtp_recv(sock))
    send_smtp(sock, f'QUIT\r\n')
    log_recv(smtp_recv(sock))

if __name__ == '__main__':

    main()