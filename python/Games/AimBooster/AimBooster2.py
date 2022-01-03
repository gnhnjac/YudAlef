import PIL
from pyautogui import *
import sys

while True:

    y = 0
    x = 0

    screen = PIL.ImageGrab.grab(bbox=(659,370,1261,790))
    px = screen.load()
    while y <= 410:
        while x <= 590:
            if px[x,y] == (255,219,195):
                    click(x+659,y+370)
                    y = 410
                    x = 590
            x+=10
        y+=10
        x=0