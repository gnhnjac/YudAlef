from os import system as sys
from tcp_by_size import send_with_size ,recv_by_size
from time import time

__author__ = 'Ami'

import socket, sys


def logtcp(dir, txt):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'LOG:Sent     >>>{txt}')
    else:
        print(f'LOG:Recieved <<<{txt}')


def client_req(data, port):
    """
    build the request according to user selection and protocol
    return: string - msg code
    """
    return f'{data}~{port}'

def main(isServer, port, remaining):

    orig_is_serv = isServer

    port = int(port)

    start = time()

    while remaining > 0:

        if isServer:
            srv_sock = socket.socket()

            srv_sock.bind(('0.0.0.0', port))

            srv_sock.listen()
            #print('after listen ... start accepting')

            # next line release the port
            srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            cli_sock, addr = srv_sock.accept()

            byte_data = recv_by_size(cli_sock)
            if byte_data == b'':
                    print('Seems client disconnected')
                    cli_sock.close()
                    srv_sock.close()
                    quit(0)
            #logtcp('recv', byte_data)
            string_data = byte_data.decode('utf-8')

            data, port = string_data.split('~')
            port = int(port)
            #print("Other side said: " + data)

            cli_sock.close()
            srv_sock.close()

        else:

            sock = socket.socket()

            new_port = port + 1 if port < 65535 else 0
            try:
                sock.connect(('127.0.0.1', port))
                # print (f'Connect succeeded {ip}:{port}')
            except:
                print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')

            data = 'a' * 40  # input("Send to server: ")
            to_send = client_req(data, new_port)
            send_with_size(sock, to_send.encode())

            # logtcp('sent', to_send)

            sock.close()

            port = new_port

        remaining -= 1
        isServer = not isServer

    if not orig_is_serv:
        print('Elapsed time: ' + str(time() - start))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == 'c':
            main(False, 10000, int(sys.argv[2]))
        elif sys.argv[1] == 's':
            main(True, 10000, int(sys.argv[2]))