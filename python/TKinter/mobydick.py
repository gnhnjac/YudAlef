
from tkinter import *
root = Tk()

def tim(coll):
        timerla = Label(root,text="8-->")
        timerla.grid(row=0,column=coll)
        
c=0
def timi():
        global c
        c+=5
        tim(c)
        root.after(1000,timi)
timi()



mainloop()

# %%
