import subprocess
from tabnanny import check
import psutil
import threading
import timeit
import socket
import struct
import signal
import atexit
import multiprocessing


CURRENT_NUMBER = 0
FINISH_NUMBER = 0
AMT_PER_CHECK = 0
CHECKS_PER_SESH = 10_000_000
NUM_OF_PROCESSES = multiprocessing.cpu_count()#4
ADDR = 'localhost'
PORT = 2022
LOCK = threading.Lock()

print(f"Started client with {NUM_OF_PROCESSES} cores.")

found = False
processes = []

s = socket.socket()
s.connect((ADDR, PORT))
amt_per_check_length_packet = s.recv(9)[:-1]
amt_per_check_packet = s.recv(int(amt_per_check_length_packet))
AMT_PER_CHECK = struct.unpack("!I",amt_per_check_packet)[0]
s.send(b'A')

print("Completed handshake with server...")

while True:
    msg = s.recv(1)
    if len(msg) == 0:
        print("Server stopped running for some reason.")
        s.close()
        exit(1)
    
    if msg == b'P':
        print("Ping from server...")
    
    elif msg == b'S':
        print("Starting work...")
        break

def handle_process(log=False):
    global CURRENT_NUMBER
    global FINISH_NUMBER
    global found
    while not found:
        
        checks_to_do = CHECKS_PER_SESH

        LOCK.acquire()

        minrange = CURRENT_NUMBER

        if FINISH_NUMBER - CURRENT_NUMBER < CHECKS_PER_SESH:
            
            if CURRENT_NUMBER >= FINISH_NUMBER:
                s.send(b'R')
                startpoint_length_packet = s.recv(9)[:-1]
                startpoint_packet = s.recv(int(startpoint_length_packet))
                CURRENT_NUMBER = struct.unpack("!I",startpoint_packet)[0]
                FINISH_NUMBER = CURRENT_NUMBER + AMT_PER_CHECK
                s.send(b'A')
                print(f"Requested work by host, range {CURRENT_NUMBER}-{FINISH_NUMBER}")

                minrange = CURRENT_NUMBER
                CURRENT_NUMBER += CHECKS_PER_SESH
            else:
                checks_to_do = FINISH_NUMBER - CURRENT_NUMBER
                CURRENT_NUMBER += checks_to_do
            
            
        else:
            CURRENT_NUMBER += CHECKS_PER_SESH

        LOCK.release()

        maxrange = minrange + checks_to_do
        if log:
            print(f"Checking range {minrange:_}-{(minrange + CHECKS_PER_SESH*NUM_OF_PROCESSES) if (minrange + CHECKS_PER_SESH*NUM_OF_PROCESSES) < FINISH_NUMBER else FINISH_NUMBER:_}")
        
        buff = b''
        proc = subprocess.Popen(['a.out', str(minrange), str(maxrange)], stdout=subprocess.PIPE)
        processes.append(proc)
        #p = psutil.Process(proc.pid)
        #p.nice(psutil.HIGH_PRIORITY_CLASS)
        
        buff, err = proc.communicate()
        
        processes.remove(proc)
        
        if (proc.poll() == 0):
            found = True
            s.send(b'F')
            s.send(buff)
            print(f"Found number: {buff.decode()}")
            return
           
        if found:
            return

def send_death_message_to_srvr():

    s.send(b'D')

atexit.register(send_death_message_to_srvr)
signal.signal(signal.SIGTERM, send_death_message_to_srvr)
signal.signal(signal.SIGINT, send_death_message_to_srvr)

threads = []
t = threading.Thread(target=handle_process, args=[True])
t.start()
threads.append(t)
for i in range(NUM_OF_PROCESSES-1):
    t = threading.Thread(target=handle_process)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

input()