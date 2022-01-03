from PIL import Image, ImageTk
import tkinter as tk
import glob, os
from time import sleep
import os.path

root = tk.Tk()

root.geometry("800x800")

speed = tk.Scale(root, from_=1, to=100, length=600, orient=tk.HORIZONTAL, label="Speed")
speed.pack()

panel = tk.Label(root)
panel.pack()

images = []
global image_index
image_index = 0

os.chdir(os.path.dirname(__file__) + "\earth_images")
for file in glob.glob("*.png"):

    img = Image.open(file)
    img.thumbnail((800, 800), Image.ANTIALIAS)

    images.append(img)

def display():

    global image_index

    tk_img = ImageTk.PhotoImage(images[image_index])
    panel.configure(image=tk_img)
    panel.image = tk_img

    image_index += 1
    if image_index == len(images):
        image_index = 0
    root.after((101-speed.get())*10, display)

display()
tk.mainloop()