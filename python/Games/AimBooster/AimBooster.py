from pyautogui import *

def find():
        trigger = None
        while trigger == None:
                trigger = locateOnScreen('trigger.png',grayscale=True,confidence=0.8,region=(551,320,641,500))

        triggerc = center(trigger)

        color = pixelMatchesColor(int(triggerc[0]),int(triggerc[1]),(255,219,195))
        if color == True:
                moveTo(triggerc[0],triggerc[1])
                click()
                find()
        else:
                find()
