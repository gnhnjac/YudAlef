import math

import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from itertools import count, islice

def isPalindrome(str):
    # Run loop from 0 to len/2
    for i in range(0, int(len(str) / 2)):
        if str[i] != str[len(str) - i - 1]:
            return False
    return True


def iterations(num):

    iters = 0
    while not isPalindrome(str(num)):
        num = num + int(str(num)[::-1])
        iters += 1
        if iters > 288:
            return -1

    return iters

vals = []
lychrel = []
last = 196
for i in range(100000):
    if iterations(i) == -1:
        vals.append((i-last))
        lychrel.append(i)
        last = i

i = 0
vals2 = []
while i < len(vals):
    try:
        repeating = []
        broke = False
        repeating.append(vals[i])
        orig_i = i
        while vals[i+1] != vals[orig_i]:
            repeating.append(vals[i+1])
            i+=1

            if (i+1-orig_i > 5):
                i = orig_i
                broke = True
                break

        if not broke:

            vals2.append(len(repeating))

        while vals[i+1] in repeating:
            i += 1
    except:
        break

d = {2: 0, 3: 0, 4: 0, 5: 0}

for val in vals2:

    d[val]+=1

print('2: ', d[2]/sum(d.values()))
print('3: ', d[3]/sum(d.values()))
print('4: ', d[4]/sum(d.values()))
print('5: ', d[5]/sum(d.values()))

plt.plot(vals)
plt.grid()
plt.show()
