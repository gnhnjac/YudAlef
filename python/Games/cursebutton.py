
import tkinter as tk
from tkinter import *
from random import randint as random
from tkinter import messagebox
with open("curses.txt",'r') as curses:
    listcu = curses.read()
    listgay = listcu.split('\n')

run = tk.Tk()

i=0
def plusone():
    randgay = random(0,len(listgay)-1)
    gaystr = listgay[randgay]
    randgay2 = random(0,len(listgay)-1)
    gaystr2 = listgay[randgay2]
    messagebox.showinfo(gaystr2,gaystr)

butt = tk.Button(run,text="gay",command=plusone,bg="red",fg="green")

butt.pack(fill=X)

mainloop()