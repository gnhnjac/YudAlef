import pygame
from random import uniform
from math import sqrt

pygame.init()

width = 500
height = 500

radius = int(width/2)

Rpoints = 0
Cpoints = 0

window = pygame.display.set_mode((width, height))

pygame.draw.circle(window, [255,255,255], (radius,radius), radius, 1)

run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    for i in range(0,1000):

        x = uniform(0, width)
        y = uniform(0, height)

        xdist = radius - x
        ydist = radius - y

        d = sqrt(xdist * xdist + ydist * ydist)

        if d < radius:
            pygame.draw.rect(window, [255, 0, 0], (x, y, 2, 2))
            Cpoints += 1
        else:
            pygame.draw.rect(window, [0, 255, 0], (x, y, 2, 2))
        Rpoints += 1


    print(4*(Cpoints/Rpoints))

    pygame.display.flip()




pygame.quit()