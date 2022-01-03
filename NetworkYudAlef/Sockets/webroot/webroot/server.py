import os

__author__ = 'Ami'

import time
import socket
import threading
import re

HTTP_VER = '1.1'

all_to_die = False  # global

def get_data(sock):

    data = b''

    while b'\r\n\r\n' not in data:

        _d = sock.recv(1)

        if _d == b'':
            return b''

        data += _d

    return data

def get_post_body(sock, post):

    len = 0

    for header in post:

        if header.split(':')[0] == 'Content-Length':

            len = int(header.split(':')[1][1:])
            break

    return sock.recv(len)


def res(sock, data):

    # returns True if 1.0 False if 1.1 and 2nd item is response
    parsed_data = data.replace('\r\n\r\n', '')
    parsed_data = parsed_data.split('\r\n')
    if '1.1' in parsed_data[0]:

        if parsed_data[0][:4] == 'POST':

            body = get_post_body(sock, parsed_data)
            return False, BUILD_POST_RES(re.search(r'POST (.*?) HTTP', parsed_data[0]).group(1),body, False)

        return False, BUILD_RES(re.search(r'GET (.*?) HTTP', parsed_data[0]).group(1),False)

    else:

        return True, BUILD_RES(re.search(r'GET (.*?) HTTP', parsed_data[0]).group(1),True)

def ok_200(url, ver):
    data = b''

    with open(url[1:], 'rb') as f:
        data += f.read()

    type = url.split('.')[1]
    if type == 'html' or type == 'txt':
        type = 'text/html; charset=utf-8'
    elif type == 'jpg' or type == 'ico':
        type = 'image/jpeg'
    elif type == 'js':
        type = 'text/javascript; charset=UTF-8'
    elif type == 'css':
        type = 'text/css'

    return f"""HTTP/{ver} 200 OK\r\nContent-Length: {str(len(data))}\r\nContent-Type: {type}\r\n\r\n""".encode('utf-8') + data

def forbidden_403(ver):
    html = f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
            <html><head>
            <title>403 Forbidden</title>
            </head><body>
            <p>Forbidden access to file</p>
            </body></html>
            """.encode('utf-8')

    return f'HTTP/{ver} 403 Forbidden\r\nContent-Length: {len(html)}\r\n\r\n'.encode('utf-8') + html

def notfound_404(url, ver):

    html = f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
                                   <html><head>
                                   <title>404 Not Found</title>
                                   </head><body>
                                   <h1>Not Found</h1>
                                   <p>The requested URL {url} was not found on this server.</p>
                                   </body></html>
                                   """.encode('utf-8')

    return f'HTTP/{ver} 404 Not Found\r\nContent-Length: {len(html)}\r\n\r\n'.encode('utf-8') + html

def calculate_next_200(num, ver):

    html = f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
                <html><head>
                <title>200 Calculate Next</title>
                </head><body>
                <p>The next num is: {str(int(num) + 1)}</p>
                </body></html>
                """.encode('utf-8')

    return f"""HTTP/{ver} 200 OK\r\nContent-Length: {str(len(html))}\r\nContent-Type: {type}\r\n\r\n""".encode('utf-8') + html

def calculate_area_200(width, height, version):
    print('hey')
    html = f"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
                <html><head>
                <title>200 Calculate Next</title>
                </head><body>
                <p>The area is: {str(int(width) * int(height)  / 2)}</p>
                </body></html>
                """.encode('utf-8')

    return f"""HTTP/{version} 200 OK\r\nContent-Length: {str(len(html))}\r\nContent-Type: {type}\r\n\r\n""".encode('utf-8') + html

def BUILD_POST_RES(url, body, isClient10):
    ver = HTTP_VER

    if isClient10:
        ver = '1.0'
    if url == '/upload':

        body_list = body.split(b'\x00&', 1)

        with open(body_list[0].split(b'=')[1], 'wb') as f:
            f.write(body_list[1].split(b'=', 1)[1])

        res = f"""HTTP/{ver} 200 OK\r\n\r\n""".encode('utf-8')

    else:

        res = f"""HTTP/{ver} 404 Not Found\r\n\r\n""".encode('utf-8')


    return res


def BUILD_RES(url, isClient10):

    ver = HTTP_VER

    if '/../' in url:
        return notfound_404(url, ver)

    not_found = False

    res = b''

    if isClient10:
        ver = '1.0'

    forbidden = [

        'hot.html',
        'sexy.html',
        '18+.html'

    ]

    moved_temp = [

        ['home.html', 'index.html'],
        ['general.html', 'index.html']

    ]

    if (url == '/'):
        url = '/index.html'

    for i in moved_temp:
        if url[1:] == i[0]:
            res = f'HTTP/{ver} 302 Found\r\nLocation: /{i[1]}\r\n\r\n'.encode('utf-8')

    if '?' in url:

        try:

            base_url = url[1:].split('?')[0]

            if base_url == 'calculate-next':
                res = calculate_next_200(url.split('=')[1], ver)

            elif base_url == 'calculate-area':
                params = url.split('?')[1].split('&')

                res = calculate_area_200(width=params[1].split('=')[1], height=params[0].split('=')[1], version=ver)

        except Exception as e:
            not_found = True

    if res == b'':
        if (os.path.isfile(url[1:])):

            if not url[1:] in forbidden:

                res = ok_200(url, ver)

            else:

                res = forbidden_403(ver)
        else:

            not_found = True

    if not_found:
        res = notfound_404(url, ver)

    return res


def logtcp(dir, tid, byte_array):
    """
	log direction, tid and all TCP byte array data
	return: void
	"""
    if dir == 'sent':
        print(f'{tid} S LOG:Sent     >>> {byte_array}')
    else:
        print(f'{tid} S LOG:Recieved <<< {byte_array}')

def check_validity(data):
    if len(data) < 16 or (not 'GET / HTTP/1.0\r\n' in data and not 'GET / HTTP/1.1\r\n'):
        return False
    return True


def handle_client(sock, tid, addr):
    """
	Main client thread loop (in the server),
	:param sock: client socket
	:param tid: thread number
	:param addr: client ip + reply port
	:return: void
	"""
    global all_to_die

    finish = False
    print(f'New Client number {tid} from {addr}')
    while not finish:

        if all_to_die:
            print('will close due to main server issue')
            break
        try:
            byte_data = get_data(sock)
            if byte_data == b'':
                print('Seems client disconnected')
                break
            logtcp('recv', tid, byte_data)
            string_data = byte_data.decode('utf-8')

            if check_validity(string_data):
                try:
                    finish, to_send = res(sock, string_data)
                except Exception as e:

                    print(e)

                    to_send = f'HTTP/1.0 500 Internal Server Error\r\n\r\n'.encode('utf-8')

                sock.send(to_send)

                if HTTP_VER == '1.0':
                    finish = True


            else:
                break
            if finish:
                time.sleep(1)
                break
        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as  err:
            print(f'General Error %s exit client loop: {err}')
            break

    print(f'Client {tid} Exit')
    sock.close()


def main():
    global all_to_die
    """
	main server loop
	1. that accept tcp connection
	2. create thread for each connected new client
	3. wait for all threads
	4. every X clients limit will exit
	"""
    threads = []
    srv_sock = socket.socket()

    srv_sock.bind(('0.0.0.0', 80))

    srv_sock.listen(20)
    print('after listen ... start accepting')

    # next line release the port
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    i = 1
    while True:
        print('Main thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr))
        t.start()
        threads.append(t)

    all_to_die = True
    print('Main thread: waiting to all clints to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
