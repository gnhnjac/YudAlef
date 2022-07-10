
from PIL import Image
import os
import operator

def tupleadd(tup1, tup2):
    return tuple(map(operator.add, tup1, tup2))

directions = {'left':(0,-1),'right':(0,1),'top':(-1,0),'bot':(1,0)}

path = os.path.dirname(os.path.realpath(__file__))

maze = Image.open(path+"\\mazehuge.png").convert('RGB')

width,height = maze.size

white = (255,255,255)

stack = []

links = {}

stack.append((0,0))
#stack.append((width-2,0))
start = True
def step():
    global start

    current = stack[0]
    found = 0
    if maze.getpixel(tupleadd(current,directions['right'])) == white:
        stack.insert(0,tupleadd(current,directions['right']))
        found +=1
    elif maze.getpixel(tupleadd(current,directions['left'])) == white:
        stack.insert(0,tupleadd(current,directions['left']))
        found+=2
    elif maze.getpixel(tupleadd(current,directions['top'])) == white:
        stack.insert(0,tupleadd(current,directions['top']))
        found+=3
    elif maze.getpixel(tupleadd(current,directions['bot'])) == white:
        stack.insert(0,tupleadd(current,directions['bot']))
        found+=4
    
    if found == 0 and not start:
        maze.putpixel(current,(255,0,0))
        stack.pop(0)
    else:
        maze.putpixel(current, (0,255,0))

    start = False

import pygame

# display image using pygame

# initialize pygame
pygame.init()

# create a surface on screen that has the size of the maze
screen = pygame.display.set_mode((width,height)) # (500,500))
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
    picture = pygame.image.fromstring(maze.tobytes(), maze.size, maze.mode)
    #picture = pygame.transform.scale(picture, (500, 500))
    screen.blit(picture, (0,0,50,50))
    # update the screen
    pygame.display.flip()
    clock.tick(100)
    for i in range(1000):
        try:
            step()
        except Exception as e:
            print(e)
            done = True
            break

for i in range(width):
    for j in range(height):
        if maze.getpixel((i,j)) == (255,0,0):
            maze.putpixel((i,j),(255,255,255))
maze.putpixel((width-2,height-1),(0,255,0))
maze.show()