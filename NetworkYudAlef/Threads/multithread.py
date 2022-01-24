import threading, string,time,datetime
import random as rnd

total_amount = 0

def Son(tid, n, name):

    sleep_time = rnd.randint(1, 4)

    print(sleep_time, tid, name)

    do_action(n, sleep_time)

    print(f'End Run {name}')

def do_action(amount_to_add, sleep_time):

    global total_amount

    for i in range (10):

        time.sleep(0.001)
        total_amount += amount_to_add

def print_char(ch):

    time.sleep(0.01)
    print(ch)


def main():

    s1 = threading.Thread(target=Son, args=(1, 1, "Avi"))
    s2 = threading.Thread(target=Son, args=(2, 1, "Beni"))
    s3 = threading.Thread(target=Son, args=(3, 1, "Gadi"))

    s1.start()
    s2.start()
    s3.start()

    s1.join()
    s2.join()
    s3.join()

    global total_amount
    print(total_amount)

    th_str = "Threads"

    for char in th_str:

        t = threading.Thread(target=print_char, args=(char))
        t.start()





if __name__ == "__main__":
    main()
