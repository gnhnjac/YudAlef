import random
import pygame
from pygame import gfxdraw
from NN import *

def remap(OldValue, OldMin, OldMax, NewMin, NewMax):

    return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

pygame.init()

window = pygame.display.set_mode((500, 500))

w, h = pygame.display.get_surface().get_size()

res = 10
cols = int(w / res)
rows = int(h / res)

nn = NeuralNetwork(2, 4, 1)

training_data = [

[

[0, 0],
[0]

],
[

[1, 1],
[0]

],
[

[1, 0],
[1]

],
[

[0, 1],
[1]

]

]

'''for i in range(0, 10000):

        data = random.choice(training_data)

        nn.train(data[0], data[1])

print("done training!")'''

run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    window.fill((255,255,255))

    for x in range(0, 1000):

        data = random.choice(training_data)

        nn.train(data[0], data[1])

    for x in range(0, cols):

        for y in range(0, rows):

            z = nn.predict([x/cols, y/rows])[0][0]

            pygame.draw.rect(window, (z*255, z*255, z*255), (x*res, y*res, res, res))

    pygame.display.update()

pygame.quit()