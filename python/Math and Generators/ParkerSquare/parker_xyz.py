# magic square
import math
import sys
from numba import njit
import numpy as np
import timeit

@njit(parallel = True, fastmath = True)
def main():
    MAX = 2000
    arr_full = [[1.0]]
    for x in range(MAX):
        print(x, x * 100 / MAX, "%")
        for y in range(MAX):
            for z in range(MAX):
                a = x + y
                b = x - y - z
                c = x + z
                d = x - y + z
                e = x
                f = x + y - z
                g = x - z
                h = x + y + z
                i = x - y

                # if a_sqr < 0 or b_sqr < 0 or c_sqr < 0 or d_sqr < 0 or e_sqr < 0 or f_sqr < 0 or g_sqr < 0 or h_sqr < 0 or i_sqr < 0:
                #     continue
                
                a_sqr = a * a
                b_sqr = b * b
                c_sqr = c * c
                d_sqr = d * d
                e_sqr = e * e
                f_sqr = f * f
                g_sqr = g * g
                h_sqr = h * h
                i_sqr = i * i
                # if not int(f) == f or not int(g) == g or not int(h) == h or not int(i) == i or not int(e) == e:
                #     continue
                
                # k = 0
                # for x in [e, f, g, h, i]:
                #     if not int(x) == x:
                #         k += 1
                #         if k > 2:
                #             break
                # if k > 2:
                #     continue

                # if 5 - len(list(filter(lambda x: x == int(x), [e, f, g, h, i]))) > 3:
                #     continue
                if a_sqr + b_sqr + c_sqr == d_sqr + e_sqr + f_sqr == g_sqr + h_sqr + i_sqr == a_sqr + d_sqr + g_sqr == b_sqr + e_sqr + h_sqr == c_sqr + f_sqr + i_sqr == a_sqr + e_sqr + i_sqr == c_sqr + e_sqr + g_sqr:
                    if len([a_sqr, b_sqr, c_sqr, d_sqr, e_sqr, f_sqr, g_sqr, h_sqr, i_sqr]) != len(set([a_sqr, b_sqr, c_sqr, d_sqr, e_sqr, f_sqr, g_sqr, h_sqr, i_sqr])):
                        continue
                    print("lollololoololloolol")
                    #arr_full.append([a, b, c, d, e, f, g, h, i])

    return arr_full

arr_full = main()

with open("square_prize.txt", "w") as f:
    for el in arr_full[1:]:
        f.write(str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + "\n" + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + "\n" + str(el[6]) + " " + str(el[7]) + " " + str(el[8]) + "\n")
        f.write("\n")