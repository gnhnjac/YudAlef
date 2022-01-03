from tkinter import *
from time import sleep
parent = Tk()
explo = PhotoImage(file="200w.gif")
earth = PhotoImage(file="earth.gif")
ephoto = Label(image=earth)
ephoto.pack()

moveup = Label(parent)
moveup.pack(side=BOTTOM)

ss = Label(parent,text=""" 
 ^ \n
 | | \n
 | | \n
/   \ \n
\   / \n
""")
ss.pack(side=BOTTOM)

def spaceship():
    ss.configure(text="""
    ^ \n
    | | \n
    | | \n
    /   \ \n
    \   / \n
    #
    """)
    parent.after(200,s2)
def s2():
    ss.configure(text="""
    ^ \n
    | | \n
    | | \n
    /   \ \n
    \   / \n
    # \n
    #
    """)
    parent.after(200,s3)
def s3():
    ss.configure(text="""
    ^ \n
    | | \n
    | | \n
    /   \ \n
    \   / \n
    # \n
    # \n
    #
    """)
    up()

times=0
plus=0.1
parent.after(3000,spaceship)

def up():
    global plus
    plus+=0.1
    global times
    times+=plus
    ss.configure(pady=times)
    if times == 182.89999999999998:
        up2()
    else:
        parent.after(100,up)

times2=0
def up2():
    global plus
    plus+=0.1
    global times2
    times2+=plus
    moveup.configure(pady=times2)
    if times2 == 208.59999999999974:
        stopspace()
    else:
        parent.after(100,up2)
def stopspace():
        ss.configure(image=explo)
mainloop()