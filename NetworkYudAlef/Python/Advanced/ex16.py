
from time import sleep

def fibo():

    i = 0
    j = 1

    while True:
        yield i
        tmp = j
        j += i
        i = tmp

gen = fibo()

num = int(input("Which number in the series? "))
n = 0

for i in range(num):

    n = next(gen)

print(n)