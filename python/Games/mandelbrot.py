import pygame
from pygame import gfxdraw
import math  

def map(OldValue, OldMin, OldMax, NewMin, NewMax):

    OldRange = (OldMax - OldMin) 
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

    return NewValue


pygame.init()

iterations = 2000

width = 500
height = 500

window = pygame.display.set_mode((width, height))

brightness_values = []

for x in range(0,width):
    brightness_values.append([])

    

for x in range(0, width):

    for y in range(0, height):

        a = map(x, 0, width, -2.5, 2.5)
        b = map(y, 0, height, -2.5, 2.5)

        originalA = a
        originalB = b

        bounded = 0

        for i in range(0, iterations):
            
            newA = a * a - b * b
            newB = 2 * a * b

            a = newA + originalA
            b = newB + originalB

            if(abs(a + b) > 16):
                break

            bounded+=1

        brightness = map(bounded, 0, iterations, 0, 1)
        brightness = map(math.sqrt(brightness), 0, 1, 0, 255)

        if(bounded == iterations):
            brightness = 0

        brightness_values[x].append(brightness)

        


run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    for x in range(0, width):

        for y in range(0, height):

            gfxdraw.pixel(window, x, y, [brightness_values[x][y],brightness_values[x][y],brightness_values[x][y]])

    pygame.display.update()

pygame.quit()