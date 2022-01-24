import requests
import json
import io
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

api_key = "lCt83KBF21w4t0RwbPYXBezwgmrevuVtbCQIoMoo"

today = datetime.today()

res = requests.get(f"https://api.nasa.gov/EPIC/api/natural/all/?api_key={api_key}")

available_dates = res.json()

images = []
global image_index
image_index = 0

root = tk.Tk()
root.geometry("800x800")

global job
job = None

year = tk.StringVar()
year.set(2015)

yearlbl = tk.Label(root, text="Year").pack()
year_box = tk.OptionMenu(root, year, *tuple(range(2015, today.year+1)))
year_box.pack()

month = tk.StringVar()
month.set(1)

monthlbl = tk.Label(root, text="Month").pack()
month_box = tk.OptionMenu(root, month, *tuple(range(1, 13)))
month_box.pack()

day = tk.StringVar()
day.set(1)

daylbl = tk.Label(root, text="Day").pack()
day_box = tk.OptionMenu(root, day, *tuple(range(1, 32)))
day_box.pack()

def check_available(y, m, d):

    for date in available_dates:

        if date['date'] == f"{y}-{m:02d}-{d:02d}":
            return True
    return False

def load_planet():

    global job
    if job is not None:
        root.after_cancel(job)
        job = None

    images.clear()

    if check_available(year.get(), int(month.get()), int(day.get())):
        res = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{year.get()}-{int(month.get()):02d}-{int(day.get()):02d}?api_key={api_key}")

        for i, data in enumerate(res.json()):

            print("{:.2f}%".format(i * 100 / len(res.json())))

            response = requests.get(f"https://api.nasa.gov/EPIC/archive/natural/{year.get()}/{int(month.get()):02d}/{int(day.get()):02d}/png/{data['image']}.png?api_key={api_key}")
            img = Image.open(io.BytesIO(response.content))
            img.thumbnail((800, 800), Image.ANTIALIAS)

            images.append(img)

        display()
    else:
        panel.configure(text="Date not available", image='')

def display():

    global image_index

    tk_img = ImageTk.PhotoImage(images[image_index])
    panel.configure(image=tk_img)
    panel.image = tk_img

    image_index += 1
    if image_index == len(images):
        image_index = 0

    job = root.after((101-speed.get())*10, display)

load = tk.Button(root, text="Load", command=load_planet)
load.pack()

speed = tk.Scale(root, from_=1, to=100, length=600, orient=tk.HORIZONTAL, label="Speed")
speed.pack()

panel = tk.Label(root)
panel.pack()

tk.mainloop()