from io import BytesIO

from tcp_by_size import send_with_size ,recv_by_size
from PIL import Image, ImageGrab
import pygame
import os

__author__ = 'Ami'

import socket, sys


def logtcp(dir, txt):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{txt}')
    else:
        print(f'C LOG:Recieved <<<{txt}')


def menu():
    """
    show client menu
    return: string with selection
    """
    print('\n  1. ask for dir')
    print('\n  2. ask for delete file')
    print('\n  3. ask for copy file')
    print('\n  4. ask for execute program')
    print('\n  5. ask for save screenshot')
    print('\n  6. ask for save screenshot locally')
    print('\n  7. ask for save video locally')
    print('\n  8. stream server screen')
    print('\n  9. notify exit')
    return input('Input 1 - 9 > ' )


def protocol_build_request(from_user):
    """
    build the request according to user selection and protocol
    return: string - msg code
    """
    if from_user == '1':
        dir = input("Enter directory path: ")
        return f'DIR~{dir}'
    elif from_user == '2':
        file = input("Enter file path: ")
        return f'DEL~{file}'
    elif from_user == '3':
        file = input("Enter file path to copy: ")
        paste_file = input("Enter file path to paste contents into: ")
        return f'CPY~{file}~{paste_file}'
    elif from_user == '4':
        prog = input("Enter program path: ")
        return f'EXE~{prog}'
    elif from_user == '5':
        dir = input("Enter directory path to save screenshot: ")
        return f'SHT~{dir}'
    elif from_user == '6':
        return f'SPH'
    elif from_user == '7':
        seconds = input("How many seconds to record? ")
        return f'SVD~{seconds}'
    elif from_user == '9':
        return f'EXT'
    else:
        return ''


def protocol_parse_reply(reply,sock):
    """
    parse the server reply and prepare it to user
    return: answer from server string
    """

    to_show = ''
    try:
        if '~' in reply:
            fields = reply.split('~')
        code = reply[:3]
        if code == 'RDR':
            to_show = 'Directory contents: \n'
            for i in fields[1:]:
                to_show += i + '\n'
        elif code == 'RDL':
            to_show = 'File deleted successfully'
        elif code == 'RCP':
            to_show = 'File copied successfully'
        elif code == 'REX':
            to_show = 'Program opened successfully'
        elif code == 'RTS':
            to_show = 'Screenshot saved successfully'
        elif code == 'RPH':

            if handle_rph(int(fields[1]), sock):
                to_show = 'Screenshot saved locally successfully'
            else:
                to_show = 'Screenshot save attempt was unsuccessful'
        elif code == 'RVD':
            if handle_rvd(int(fields[1]), sock):
                to_show = 'Video saved locally successfully'
            else:
                to_show = 'Video save attempt was unsuccessful'
        elif code == 'ERR':
            to_show = 'Server return an error: ' + fields[1] + ' ' + fields[2]
        elif code == 'RXT':
            pass
    except:
        print ('Server reply bad format')
    return to_show

def handle_rph(image_len,sock):
    img_data = b''

    while len(img_data) < image_len:
        try:
            _d = sock.recv(image_len - len(img_data))
        except socket.error as e:
            print(e)
        if _d == b'':
            img_data = b''
            break
        img_data += _d
    
    if len(img_data) != image_len:
        return False

    img = Image.frombytes("RGB", (1920,1080),img_data)
    img.save('screenshot.jpg')

    return True


def handle_rvd(video_len, sock):
    video_data = b''

    while len(video_data) < video_len:
        try:
            _d = sock.recv(video_len - len(video_data))
        except socket.error as e:
            print(e)
        if _d == b'':
            video_data = b''
            break
        video_data += _d

    if len(video_data) != video_len:
        return False

    with open('recording.mp4', 'wb') as f:
        f.write(video_data)

    return True

def stream_server_screen(sock):

    pygame.init()

    X = 1440
    Y = 810

    display_surface = pygame.display.set_mode((X, Y))

    run = True
    while run:

        send_with_size(sock, 'SPH'.encode())
        byte_data = recv_by_size(sock)
        if byte_data == b'':
            print('Seems server disconnected abnormal')
            pygame.quit()
            return

        data = byte_data.decode('UTF8')  # will crash if contains none text data
        handle_reply(data, sock, False)

        basewidth = 1440
        img = Image.open('screenshot.jpg')
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save('screenshot_resize.jpg')

        image = pygame.image.load('screenshot_resize.jpg')
        display_surface.blit(image, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break

            # Draws the surface object to the screen.
            pygame.display.update()

    os.remove('screenshot.jpg')
    os.remove('screenshot_resize.jpg')

def handle_reply(reply, sock, log=True):
    """
    get the tcp upcoming message and show reply information
    return: void
    """
    to_show = protocol_parse_reply(reply, sock)
    if to_show != '' and log:
        print('\n==============')
        print (f'SERVER Reply: {to_show}')
        print('===============')


def main(ip):
    """
    main client - handle socket and main loop
    """
    connected = False

    sock= socket.socket()
    exit = False

    port = 1233
    try:
        sock.connect((ip,port))
        print (f'Connect succeeded {ip}:{port}')
        connected = True
    except:
        print(f'Error while trying to connect.  Check ip or port -- {ip}:{port}')

    while connected:
        from_user = menu()
        if from_user == '8':
            stream_server_screen(sock)
            continue
        to_send = protocol_build_request(from_user)
        if to_send =='':
            print("Selection error try again")
            continue
        try :
            send_with_size(sock, to_send.encode())
            logtcp('sent', to_send)
            byte_data = recv_by_size(sock)
            if byte_data == b'':
                print ('Seems server disconnected abnormal')
                break
            logtcp('recv',byte_data)

            data = byte_data.decode('UTF8')  # will crash if contains none text data
            handle_reply(data, sock)

            if from_user == '9':
                print('Will exit ...')
                connected = False
                break
        except socket.error as err:
            print(f'Got socket error: {err}')
            break
        except Exception as err:
            print(f'General error: {err}')
            break
    print ('Bye')
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('127.0.0.1')