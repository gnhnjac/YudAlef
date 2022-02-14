import os
from PIL import Image
import random

path = os.path.dirname(os.path.realpath(__file__))

im = Image.open(path+"\\img.jpg").convert("RGB")

width,height=im.size

begin_pos = None

for i in range(width):

    for j in range(height):
        if im.getpixel((i,j))==(0,0,0):
            begin_pos = (i,j)
            break
    if begin_pos is not None:
        break
if begin_pos == None:
    print("NO BLACK PIXELS FOUND")
    exit(1)

im.putpixel(begin_pos,(255,0,0))

path = []
path.append(begin_pos)

def get_neighbors(cell):

    amt = 0

    x = cell[0]
    y = cell[1]

    if im.getpixel((x,y+1)) == (0,0,0):
        amt+=1
    if im.getpixel((x,y-1)) == (0,0,0):
        amt+=1
    if im.getpixel((x+1,y)) == (0,0,0):
        amt+=1
    if im.getpixel((x-1,y)) == (0,0,0):
        amt+=1

    return amt

quarantined = []
def step():

    if len(path) == 0:
        path.append(begin_pos)

    current = path[len(path)-1]
    x = current[0]
    y = current[1]

    im.putpixel((x,y),(255,0,0))

    arr = [(0,-1),(0,1),(1,0),(-1,0)]

    while len(arr) > 0:
        choice = random.choice(arr)
        try_x = x + choice[0]
        try_y = y + choice[1]

        if im.getpixel((try_x,try_y)) == (0,0,0): #and current not in quarantined:
            path.append((try_x,try_y))
            #quarantined.clear()
            return

        arr.remove(choice)

    while(get_neighbors(current) < 2):
        path.pop(len(path)-1)
        if len(path) == 0:
            path.append(begin_pos)
        current = path[len(path)-1]
        x = current[0]
        y = current[1]
        im.putpixel((x,y),(0,0,0))
    #quarantined.append(current)


import pygame

# display image using pygame

# initialize pygame
pygame.init()

# create a surface on screen that has the size of the maze
screen = pygame.display.set_mode((width*2,height*2)) # (500,500))
clock = pygame.time.Clock()
# main loop
done = False
while not done:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            done = True
    # draw the maze on the screen
    picture = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
    picture = pygame.transform.scale(picture, (width*2, height*2))
    screen.blit(picture, (0,0,50,50))
    # update the screen
    pygame.display.flip()
    clock.tick(100)
    try:
        for i in range(1000):
            step()
    except:
        done = True
        break

print(path)