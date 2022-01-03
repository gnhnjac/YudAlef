import requests
import urllib.request
import bs4
from PIL import ImageTk
import PIL.Image
import io
import time
from tkinter import *

year_now = time.strftime("%y", time.localtime())

def get_apod():

    res = requests.get(f"https://apod.nasa.gov/apod/ap{year.get():02d}{month.get():02d}{day.get():02d}.html")

    soup = bs4.BeautifulSoup(res.content)

    img = soup.find('img')
    try:
        response = requests.get(f"https://apod.nasa.gov/apod/{img.get('src')}")
        image = PIL.Image.open(io.BytesIO(response.content))

        tk_img = ImageTk.PhotoImage(image)
        panel.configure(image=tk_img)
        panel.image = tk_img

        for element in soup.findAll('p'):

            if 'Explanation:' in element.text:

                ctr = element.find('center')
                ctr.extract()

                description_v.set(element.text)

    except AttributeError:
        panel.configure(text="Image Not Found", image='')

master = Tk()
master.title("Astronomy Picture of the Day")
master.geometry("800x900")

year_t = Label(master, text="Year", relief=RAISED, width=50, pady=5)
year_t.pack()

year = Scale(master, from_=15, to=year_now, length=600, orient=HORIZONTAL)
year.pack()

month_t = Label(master, text="Month", relief=RAISED, width=50, pady=5)
month_t.pack()

month = Scale(master, from_=1, to=12, length=600, orient=HORIZONTAL)
month.pack()

day_t = Label(master, text="Day", relief=RAISED, width=50, pady=5)
day_t.pack()

day = Scale(master, from_=1, to=31, length=600, orient=HORIZONTAL)
day.pack()

btn = Button(master, text="Get APOD", command=get_apod)
btn.pack()

panel = Label(master)
panel.pack(side=RIGHT)

description_v = StringVar()

description = Label(master, textvariable=description_v)
description.pack(side=LEFT)

mainloop()