# magic square
import math
import sys
from numba import njit
import numpy as np
import timeit

@njit(parallel = True, fastmath = True)
def main():
    MAX = 100000
    arr = [[1]]
    a = 2
    b = 94
    c = 113
    d = 127
    e = 58
    f = 46
    g = 74
    h = 97
    i = 82
    arr.append([a, b, c, d, e, f, g, h, i])
    az = a
    bz = b
    cz = c
    dz = d
    ez = e
    fz = f
    gz = g
    hz = h
    iz = i
    for n in range(1,MAX):
        arr.append([a, b, c, d, e, f, g, h, i])
        a += az
        b += bz
        c += cz
        d += dz
        e += ez
        f += fz
        g += gz
        h += hz
        i += iz

    return arr

arr = main()


with open("square_trick.txt", "w") as f:
    for el in arr[1:]:
        f.write(str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + "\n" + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + "\n" + str(el[6]) + " " + str(el[7]) + " " + str(el[8]) + "\n")
        f.write("\n")