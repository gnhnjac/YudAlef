__author__ = 'Ami'

import socket, random
import time, threading, os, datetime
from os import listdir, remove
import subprocess
import pyautogui
from tcp_by_size import send_with_size, send_big_with_size, recv_by_size, SIZE_HEADER_FORMAT
import os
import numpy as np
from PIL import ImageGrab
import cv2

all_to_die = False  # global


def logtcp(dir, tid, byte_array):
    """
	log direction, tid and all TCP byte array data
	return: void
	"""
    if dir == 'sent':
        print(f'{tid} S LOG:Sent     >>> {byte_array}')
    else:
        print(f'{tid} S LOG:Recieved <<< {byte_array}')


def send_data(message, tid, sock):
    """
	send to client byte array data
	will add 8 bytes message length as first field
	e.g. from 'abcd' will send  b'00000004~abcd'
	return: void
	"""
    if message[:3] != 'RPH' and message[:3] != 'RVD':
        send_with_size(sock, message.encode())
    logtcp('sent', tid, message.encode())


def check_length(message):
    """
	check message length
	return: string - error message
	"""
    size = len(message)
    if size < 13:  # 13 is min message size
        return 'ERR~003~Bad Format message too short'
    return ''


def protocol_build_reply(request, sock):
    """
	Application Business Logic
	function despatcher ! for each code will get to some function that handle specific request
	Handle client request and prepare the reply info
	string:return: reply
	"""
    reply = ''
    code = request[:3]
    if '~' in request:
        fields = request.split('~')

    if code == 'DIR': # Return all files in certain dir
        try:
            file_list = listdir(fields[1])
            reply = 'RDR'
            for file in file_list:
                reply += '~' + file
        except:
            reply = 'ERR~004~Directory not found'
    elif code == 'DEL': # Delete file
        try:
            remove(fields[1])
            reply = 'RDL'
        except:
            reply = 'ERR~005~File to delete not found'
    elif code == 'CPY': # Copy file to another location
        try:
            with open(fields[1], 'rb') as f1:
                try:
                    with open(fields[2], 'wb') as f2:
                        f2.write(f1.read())

                except:
                    reply = 'ERR~007~New file path to copy to not found'
                else:
                    reply = 'RCP'
        except:
            reply = 'ERR~006~File to copy not found'
    elif code == 'EXE': # Run exe
        try:
            subprocess.call(fields[1])
            reply = 'REX'
        except:
            reply = 'ERR~008~Program not found'
    elif code == 'SHT': # Save screenshot here

        try:
            image = pyautogui.screenshot()
        except:
            reply = "ERR~009~Couldn't take screenshot"
        else:
            try:
                image.save(r'{}\screenshot.jpg'.format(fields[1]))
            except:
                reply = 'ERR~010~Directory path to save screenshot to not found'
            else:
                reply = 'RTS'
    elif code == 'SPH': # Save photo

        try:
            image = pyautogui.screenshot()
            reply = f'RPH~{len(image.tobytes())}'
            send_big_with_size(sock, reply.encode(), image.tobytes())

        except:
            reply = "ERR~009~Couldn't take screenshot"
    elif code == 'SVD': # Save video

        try:
            save_compressed_screen_recording(int(fields[1]))
            with open('output_c.mp4', 'rb') as v:
                video = v.read()
                reply = f'RVD~{len(video)}'
                send_big_with_size(sock, reply.encode(), video)
            os.remove('output_c.mp4')
        except:
            reply = "ERR~011~Couldn't save screen recording"
    elif code == 'EXT': # Disconnect client
        reply = 'RXT'
    else:
        reply = 'ERR~002~code not supported'
        fields = ''
    return reply


def save_compressed_screen_recording(seconds):
    start = time.time()
    frames = []
    while int(time.time() - start) < seconds:
        start_take = time.time()
        printscreen_pil = ImageGrab.grab()
        printscreen_numpy = np.array(printscreen_pil, dtype='uint8')
        frames.append(printscreen_numpy[..., :3])

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 19, (1920, 1080))
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()

    os.system('ffmpeg -y -i output.mp4 -vcodec h264 -crf 28 -an -filter:v fps=fps=19 output_c.mp4')
    os.remove('output.mp4')


def handle_request(request, sock):
    """
	Hadle client request
	tuple :return: return message to send to client and bool if to close the client socket
	"""
    try:
        to_send = protocol_build_reply(request, sock)
        if request[:3] == 'EXT':
            return to_send, True
    except:
        to_send = 'ERR~001~General error'
    return to_send, False


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
            byte_data = recv_by_size(sock)
            if byte_data == b'':
                print('Seems client disconnected')
                break
            logtcp('recv', tid, byte_data)
            string_data = byte_data.decode('utf-8')
            err_size = check_length(SIZE_HEADER_FORMAT + string_data)
            if err_size != '':
                to_send = err_size
            else:
                to_send, finish = handle_request(string_data, sock)
            if to_send != '':
                send_data(to_send, tid, sock)
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

    srv_sock.bind(('0.0.0.0', 1233))

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
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('Main thread: going down for maintenance')
            break

    all_to_die = True
    print('Main thread: waiting to all clints to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
