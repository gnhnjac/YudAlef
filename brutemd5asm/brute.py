import subprocess
import psutil
import threading
import timeit

current_number = 0
CHECKS_PER_SESH = 10_000_000
NUM_OF_PROCESSES = 8
lock = threading.Lock()
found = False
processes = []

def handle_process(log=False):
    global current_number
    global found
    accumulated = 0
    while not found:
        
        time = timeit.default_timer()
        
        lock.acquire()
        minrange = current_number
        current_number += CHECKS_PER_SESH
        lock.release()
        maxrange = minrange + CHECKS_PER_SESH
        if log:
            print(f"Checking range {minrange:_}-{minrange + CHECKS_PER_SESH*NUM_OF_PROCESSES:_}")
        buff = b''
        proc = subprocess.Popen(['a.out', str(minrange), str(maxrange)], stdout=subprocess.PIPE)
        processes.append(proc)
        p = psutil.Process(proc.pid)
        p.nice(psutil.HIGH_PRIORITY_CLASS)
        
        buff, err = proc.communicate()
        
        processes.remove(proc)
        
        if (proc.poll() == 0):
            found = True
            print(f"Found number: {buff.decode()} in {(accumulated + timeit.default_timer() - time):.3f}s")
            return
           
        if found:
            return
            
        time = timeit.default_timer() - time
        accumulated += time
        if log:
            print(f"Loop - {time:.3f}s\nAccumulated - {accumulated:.3f}s")
    
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