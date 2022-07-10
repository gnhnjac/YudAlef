import datetime
import time
from random import *
import math
import threading


global sum

global isLocked

def main():


    pairs = 50

    total = 0

    num = []

    fill_pair_lst(num, pairs)

    print(num)

    # SYNC

    start = datetime.datetime.now()
    for i in range(pairs):

        total += num[i*2]*num[i*2+1] if i % 2 == 0 else num[i*2]/num[i*2+1]
    print("time diff sync", (datetime.datetime.now() - start))
    print("total is: " + str(total))


    # ASYNC

    global sum
    sum = 0

    global isLocked
    isLocked = False

    f = {0: f1, 1: f2}

    threads = []

    start = datetime.datetime.now()
    for i in range(pairs):

        t = threading.Thread(target=f[i%2], args=(num[i*2], num[i*2+1]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("time diff async", (datetime.datetime.now() - start))

    print("Sum is: " + str(sum))


def fill_pair_lst(lst, amt):

    for i in range(2*amt):
        lst.append(randint(1, 9))


def f1(x, y):  # MUL
    global sum
    global isLocked
    while isLocked:
        continue

    isLocked = True
    z = float(sum)
    time.sleep(0.1)
    z += x / y
    time.sleep(0.1)
    sum = str(z)
    isLocked = False


def f2(x, y):  # DIV
    global sum
    global isLocked
    while isLocked:
        continue

    isLocked = True
    z = float(sum)
    time.sleep(0.1)
    z += x / y
    time.sleep(0.1)

    sum = str(z)
    isLocked = False


if __name__ == "__main__":

    main()