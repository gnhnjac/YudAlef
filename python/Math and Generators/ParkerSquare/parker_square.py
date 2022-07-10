# magic square
import math
import sys
from numba import njit
import numpy as np
import timeit

@njit(parallel = True, fastmath = True)
def main():
    MAX = 2000
    arr_half = [[1]]
    arr_full = [[1]]
    for a in range(MAX):
        print(a, a * 100 / MAX, "%")
        for b in range(MAX):
            for c in range(MAX):
                for d in range(MAX):
                    a_sqr = a * a
                    b_sqr = b * b
                    c_sqr = c * c
                    d_sqr = d * d

                    g_sqr = b_sqr + c_sqr - d_sqr
                    f_sqr = g_sqr + c_sqr - d_sqr
                    h_sqr = d_sqr + f_sqr - b_sqr
                    i_sqr = a_sqr + b_sqr + c_sqr - h_sqr - g_sqr
                    e_sqr = a_sqr + b_sqr + c_sqr - f_sqr - d_sqr

                    if e_sqr < 0 or f_sqr < 0 or g_sqr < 0 or h_sqr < 0 or i_sqr < 0:
                        continue

                    e = math.sqrt(e_sqr)
                    f = math.sqrt(f_sqr)
                    g = math.sqrt(g_sqr)
                    h = math.sqrt(h_sqr)
                    i = math.sqrt(i_sqr)
                    if not int(f) == f or not int(g) == g or not int(h) == h or not int(i) == i or not int(e) == e:
                        continue

                    if a_sqr + b_sqr + c_sqr == d_sqr + e_sqr + f_sqr == g_sqr + h_sqr + i_sqr == a_sqr + d_sqr + g_sqr == b_sqr + e_sqr + h_sqr == c_sqr + f_sqr + i_sqr and (
                            a_sqr + e_sqr + i_sqr == a_sqr + b_sqr + c_sqr or c_sqr + e_sqr + g_sqr == a_sqr + b_sqr + c_sqr):
                        # print("NORMAL HALF:")
                        # print(a, b, c, "\n", d, int(e), int(f), "\n", int(g), int(h), int(i))
                        # print("SQR HALF:")
                        # print(a_sqr, b_sqr, c_sqr, "\n", d_sqr, e_sqr, f_sqr, "\n", g_sqr, h_sqr, i_sqr)
                        if len([a_sqr, b_sqr, c_sqr, d_sqr, int(e_sqr), int(f_sqr), int(g_sqr), int(h_sqr), int(i_sqr)]) != len(set([a_sqr, b_sqr, c_sqr, d_sqr, int(e_sqr), int(f_sqr), int(g_sqr), int(h_sqr), int(i_sqr)])):
                            continue
                        if a_sqr + e_sqr + i_sqr == c_sqr + e_sqr + g_sqr:
                            arr_full.append([a, b, c, d, int(e), int(f), int(g), int(h), int(i)])
                        else:
                            arr_half.append([a, b, c, d, int(e), int(f), int(g), int(h), int(i)])

    return arr_half, arr_full

arr_half, arr_full = main()

with open("square.txt", "w") as f:

    f.write("FULL:\n")
    for el in arr_full[1:]:
        f.write(str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + "\n" + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + "\n" + str(el[6]) + " " + str(el[7]) + " " + str(el[8]) + "\n")
        f.write("\n")
    f.write("HALF:\n")
    for el in arr_half[1:]:
        f.write(str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + "\n" + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + "\n" + str(el[6]) + " " + str(el[7]) + " " + str(el[8]) + "\n")
        f.write("\n")