from pyautogui import *
from time import sleep

win = None
while win == None:
    win = locateOnScreen('win.png',grayscale=True,confidence=0.8)

winc = center(win)

moveTo(winc[0],winc[1])
click()

for key in 'calculator':
    press(key)

press('enter')

sleep(1)

sbtn = None
while sbtn == None:

    sbtn = locateOnScreen('6btn.png',grayscale=True,confidence=0.9)

sbtnc = center(sbtn)

moveTo(sbtnc[0],sbtnc[1])
click()

nbtn = None
while nbtn == None:

    nbtn = locateOnScreen('9btn.png',grayscale=True,confidence=0.9)

nbtnc = center(nbtn)

moveTo(nbtnc[0],nbtnc[1])
click()