import threading, string,time,datetime
import random as rnd

total_amount = 0

class Son(threading.Thread):
    def __init__(self, tid, amount_to_add, name):
        super(Son, self).__init__()  # inheritance from threading.Thread (superclass/parent)
        self.tid = tid
        self.amount_to_add = amount_to_add
        self.name = name
        self.sleep_time = rnd.randint(1, 4)

    def do_action(self):
        global total_amount
        for i in range(10):
            time.sleep(self.sleep_time)
            total_amount += self.amount_to_add

    def run(self):
        print("name: %s, tid: %s, sleep time: %s" % (self.name, self.tid, self.sleep_time))
        self.do_action()
        print("End Run %s" % self.name)


def main():

    s1 = Son(1, 1, "Avi")
    s2 = Son(2, 1, "Beni")
    s3 = Son(3, 1, "Gadi")

    s1.start()
    s2.start()
    s3.start()

    s1.join()
    s2.join()
    s3.join()

    global total_amount
    print(total_amount)


if __name__ == "__main__":
    main()
