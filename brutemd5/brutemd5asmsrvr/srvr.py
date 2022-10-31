import socket
import threading
import struct
import timeit

AMT_PER_PC = 200_000_000 # !! Can't be smaller than 10m, must be a multiple of it.
NUMBER = 0
LOCK = threading.Lock()
PORT = 2022

STARTTIME = timeit.default_timer()

s = socket.socket()

s.bind(('localhost', PORT))

s.listen()

print(f"Server running on {socket.gethostbyname(socket.gethostname())}:{PORT}")

found = False

threads = []
pending_ranges = []

def get_prefix(bytes):
    return str(len(bytes)).zfill(8).encode() + b'|'

def handle_conn(conn, addr):

    global s
    global found
    global NUMBER
    global STARTTIME
    
    CURRENTLY_CHECKING = -1

    try:
        amount = struct.pack("!I", AMT_PER_PC)
        prefix = get_prefix(amount)

        conn.send(prefix + amount)
        ack = conn.recv(1)
        if len(ack) == 0:
            print(f"Computer {addr} disconnected.")
            return

        print(f"Handshake established with {addr}.")


        while not found:

            req = conn.recv(1)
            if len(req) == 0:
                print(f"Computer {addr} disconnected.")
                return

            if req == b'R':
                
                took_from_pending = False

                LOCK.acquire()
                if len(pending_ranges) == 0:
                    startpoint = struct.pack("!I", NUMBER)
                else:
                    startpoint = struct.pack("!I", pending_ranges[0])
                    took_from_pending = True
                prefix = get_prefix(startpoint)

                conn.send(prefix + startpoint)

                ack = conn.recv(1)
                if len(ack) == 0:
                    LOCK.release()
                    print(f"Computer {addr} disconnected.")                
                    return
                
                if not took_from_pending:
                    NUMBER += AMT_PER_PC
                else:
                    del pending_ranges[0]
                LOCK.release()
                if not took_from_pending:
                    CURRENTLY_CHECKING = NUMBER - AMT_PER_PC
                    print(f"Computer {addr} checking numbers {NUMBER-AMT_PER_PC}-{NUMBER}")
                else:
                    CURRENTLY_CHECKING = struct.unpack("!I", startpoint)[0]
                    print(f"Computer {addr} checking PENDING numbers {CURRENTLY_CHECKING}-{CURRENTLY_CHECKING+AMT_PER_PC}")
            
            elif req == b'F':
                number = conn.recv(1024)
                print(f"Computer {addr} found number, it was {int(number.decode()):_}\nelapsed time: {(timeit.default_timer() - STARTTIME):.4f}s")
                found = True
                return

            elif req == b'D':
                print(f"Computer {addr} disconnected.")
                if CURRENTLY_CHECKING != -1:
                    pending_ranges.append(CURRENTLY_CHECKING)
                return

    except ConnectionResetError:
        print(f"Computer {addr} disconnected.")
        if CURRENTLY_CHECKING != -1:
            pending_ranges.append(CURRENTLY_CHECKING)           
        return

while not found:

    conn, addr = s.accept()

    t = threading.Thread(target=handle_conn, args=[conn, addr])

    t.start()

    threads.append(t)

for t in threads:

    t.join()

s.close()