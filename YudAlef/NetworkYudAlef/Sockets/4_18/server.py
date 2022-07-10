import socket
import struct
import time

def logtcp(dir, txt):
    """
    log direction and all TCP byte array data
    return: void
    """

    if txt == b'':
        return

    if dir == 'sent':
        print(f'LOG:Sent     >>>{txt}')
    else:
        print(f'LOG:Recieved <<<{txt}')

def send_udp(sock, data, dest_addr):
    print("Sending to: " + dest_addr[0],dest_addr[1])

    sock.sendto(data, dest_addr)

    logtcp('sent',data)


def get_from_google(data):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    s.send(data)
    data = s.recv(1024)
    s.close()
    return data


def build_dns_res(data):

    res = b''

    orig_data = data

    try:
        if (data[-4:-2] == b'\x00\x01'):
            url = ''

            t_id_raw = data[:2]
            t_id, = struct.unpack('!H', data[:2])

            data = data[12:]

            len = int(hex(data[0]), 16)

            anchor = 1

            while len != 0:

                url += data[anchor:anchor+len].decode('utf-8') + '.'

                anchor += len
                len = int(hex(data[anchor]), 16)
                anchor+=1

            url = url[:-1]

            print("Transaction id: " + str(t_id))
            print(url)
            if (url == 'www.MyFakeDomain.co.il.lan' or url == 'www.MyFakeDomain.co.il'):

                res = t_id_raw + b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00' + data + b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x4f\x04' + struct.pack('B', 55) + struct.pack('B', 122) + struct.pack('B', 5) + struct.pack('B', 33)
            else:
                raise Exception
        else:
            raise Exception
    except Exception as e:

        res = get_from_google(orig_data)

    return res

def main():
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    srv_sock.bind(('127.0.0.1', 53))
    print(srv_sock.getsockname())

    while True:
        try:
            byte_data, dest_addr = srv_sock.recvfrom(1024)
            if byte_data == None:
                print('Seems client disconnected')
            else:
                logtcp('recv', byte_data)

                to_send = build_dns_res(byte_data)
                if to_send != b'':
                    send_udp(srv_sock, to_send, dest_addr)
        except:
            pass


    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
