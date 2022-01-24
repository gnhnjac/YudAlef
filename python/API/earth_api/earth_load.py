import requests
import json
import io
from PIL import Image, ImageDraw, ImageFont
import os
import glob
import urllib.request
import time
import os.path

api_key = "bKuVzBpE9MjCl3CcuW2bgLD7hLUB3diCNATSUkd3"

res = requests.get(f"https://api.nasa.gov/EPIC/api/natural/all/?api_key={api_key}")

available_dates = res.json()

def check_available(y, m, d):

    for date in available_dates:

        if date['date'] == f"{y}-{m:02d}-{d:02d}":
            return True
    return False

year = ''
month = ''
day = ''

available = False
while not available:
    while (year == '' or month == '' or day == ''):
        year = input("Year: ")
        month = input("Month: ")
        day = input("Day: ")

    if check_available(year, int(month), int(day)):
        available = True
    else:
        print("Date not available")
        year = ''
        month = ''
        day = ''

res = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{year}-{int(month):02d}-{int(day):02d}?api_key={api_key}")

files = glob.glob(os.path.dirname(__file__) + 'earth_images/*')
for f in files:
    os.remove(f)

font = ImageFont.truetype("C:\Windows\Fonts\\arial.ttf", 60)

for i, data in enumerate(res.json()):

    '''

    Checked with perf_counter

    results:

    Requests Time: 89.060116 seconds
    Urllib Time: 70.344256 seconds

    ~19 second difference

    '''

    response = requests.get(f"https://api.nasa.gov/EPIC/archive/natural/{year}/{int(month):02d}/{int(day):02d}/png/{data['image']}.png?api_key={api_key}")
    img = Image.open(io.BytesIO(response.content))

    date = ImageDraw.Draw(img)
    date.text((10,10), data['date'], fill=(255,255,255), font=font)

    img.save(os.path.dirname(__file__) + f"/earth_images/{i:02d}.png")

    # urllib.request.urlretrieve(f"https://api.nasa.gov/EPIC/archive/natural/{year}/{int(month):02d}/{int(day):02d}/png/{data['image']}.png?api_key={api_key}", f"API/earth_api/earth_images/{i:02d}.png")
