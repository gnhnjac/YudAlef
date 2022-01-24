import socket
import sys
import os


def logtcp(dir, txt):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{txt}')
    else:
        print(f'C LOG:Recieved <<<{txt}')

def recv_post(sock):

    data = b''

    while (b'\r\n\r\n' not in data):

        _d = sock.recv(1)

        if _d == b'':
            return b''

        data += _d

    return data

def build_post(filename):
    if os.path.isfile(filename):
        data = b''

        with open(filename, 'rb') as f:
            data = f.read()

        body = f"""file-name={filename}\x00&image-data=""".encode('utf-8') + data

        post = f"""POST /upload HTTP/1.1\r\nContent-Length: {str(len(body))}\r\n\r\n""".encode('utf-8') + body

        return post

    else:

        return b''

def main(ip):
    """
    main client - handle socket and main loop
    """
    connected = False

    sock = socket.socket()
    port = 80
    try:
        sock.connect((ip, port))
        print(f'Connect succeeded {ip}:{port}')
        connected = True
    except:
        print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')

    while connected:
        from_user = input("Enter filename: ")
        to_send = build_post(from_user)
        if to_send == b'':
            print("Selection error try again")
            continue
        try:
            sock.send(to_send)
            logtcp('sent', to_send)
            byte_data = recv_post(sock)
            if byte_data == b'':
                print('Seems server disconnected abnormal')
                break
            logtcp('recv', byte_data)

            data = byte_data.decode('UTF8')  # will crash if contains none text data
            # handle_post(data, sock)

            if from_user == 'exit':
                print('Will exit ...')
                break
        except socket.error as err:
            print(f'Got socket error: {err}')
            break
        except Exception as err:
            print(f'General error: {err}')
            break
    print('Bye')
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('127.0.0.1')
