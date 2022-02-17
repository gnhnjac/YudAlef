import os
from PIL import Image,ImageDraw
import random

class cell:

    def __init__(self, i:int,j:int) -> None:
        # pos
        self.i = i
        self.j = j

        # has partner
        self.left = False
        self.right = False
        self.top = False
        self.bot = False

        # visited
        self.visited = False

path = os.path.dirname(os.path.realpath(__file__))

im = Image.open(path+"\\img2.jpg").convert("RGB")

width,height=im.size

begin_pos = None

maze = []
for i in range(width):
    maze.append([])
    for j in range(height):
        maze[i].append(cell(i,j))

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

        if im.getpixel((try_x,try_y)) == (0,0,0) and (try_x,try_y) not in quarantined:
            path.append((try_x,try_y))
            return

        arr.remove(choice)
    im.putpixel(path[-1:][0],(0,0,0))
    im.putpixel(path[-2:][0], (0, 0, 0))
    quarantined.append(path[-1:][0])
    quarantined.append(path[-2:][0])
    del path[-2:]

# import pygame
#
# # display image using pygame
#
# # initialize pygame
# pygame.init()
#
# # create a surface on screen that has the size of the maze
# screen = pygame.display.set_mode((width*2,height*2)) # (500,500))
# clock = pygame.time.Clock()
#
# quar = 0
#
# # main loop
# done = False
# while not done:
#     # event handling, gets all event from the event queue
#     for event in pygame.event.get():
#         # only do something if the event is of type QUIT
#         if event.type == pygame.QUIT:
#             # change the value to False, to exit the main loop
#             done = True
#     # draw the maze on the screen
#     picture = pygame.image.fromstring(im.tobytes(), im.size, im.mode)
#     picture = pygame.transform.scale(picture, (width*2, height*2))
#     screen.blit(picture, (0,0,50,50))
#     # update the screen
#     pygame.display.flip()
#     clock.tick(100)
#     try:
#         for i in range(10000):
#             quar += 1
#             if quar % 2000 == 0:
#                 quarantined.clear()
#             step()
#             # 650 223
#             if len(path) > 0 and abs(path[-1:][0][0]-650) < 20 and abs(path[-1:][0][1]-223) < 20:
#                 done = True
#                 break
#     except Exception as e:
#         print(e)
#         done = True
#         break
quar = 0
done = False
while not done:
    quar += 1
    if quar % 2000 == 0:
        quarantined.clear()
    try:
        step()
    except:
        done = True
        break
    # 650 223
    if len(path) > 0 and abs(path[-1:][0][0] - (width-2)) < 1 and abs(path[-1:][0][1] - height-1) < 1:
        done = True
        break

for i in range(width):

    for j in range(height):

        if im.getpixel((i,j)) == (255,0,0):
            im.putpixel((i,j),(0,0,0))
        if im.getpixel((i,j)) == (0,255,0):
            path.append((i,j))

for k in range(len(path)-1):
    i = path[k][0]
    j = path[k][1]
    next_i = path[k+1][0]
    next_j = path[k+1][1]
    im.putpixel((i,j),(0,255,0))
    maze[i][j].visited = True

    diff = (next_i-i,next_j-j)

    if diff == (-1,0):
        maze[i][j].top = True
        maze[next_i][next_j].bot = True
    elif diff == (1,0):
        maze[i][j].bot = True
        maze[next_i][next_j].top = True
    elif diff == (0,1):
        maze[i][j].right = True
        maze[next_i][next_j].left = True
    elif diff == (0,-1):
        maze[i][j].left = True
        maze[next_i][next_j].right = True
print("DONE COMPUTING BASE MAZE")

i = 0
j = 0
stack = []
cell = maze[i][j]
#cell.visited = True
stack.append(cell)

while len(stack) > 0:
    cell = stack.pop(0)
    i = cell.i
    j = cell.j

    placed = False
    arr = [0,1,2,3]
    while not placed and len(arr) > 0:
        choice = random.choice(arr)

        if cell.right == False and j+1 < len(maze[0]) and maze[i][j+1].visited == False and choice == 0:
            stack.insert(0,cell)
            cell.right = True
            maze[i][j+1].left = True
            maze[i][j+1].visited = True
            stack.insert(0,maze[i][j+1])
            placed = True
        if cell.left == False and j-1 >= 0 and maze[i][j-1].visited == False and choice == 1:
            stack.insert(0,cell)
            cell.left = True
            maze[i][j-1].right = True
            maze[i][j-1].visited = True
            stack.insert(0,maze[i][j-1])
            placed = True
        if cell.top == False and i-1 >= 0 and maze[i-1][j].visited == False and choice == 2:
            stack.insert(0,cell)
            cell.top = True
            maze[i-1][j].bot = True
            maze[i-1][j].visited = True
            stack.insert(0,maze[i-1][j])
            placed = True
        if cell.bot == False and i+1 < len(maze) and maze[i+1][j].visited == False and choice == 3:
            stack.insert(0,cell)
            cell.bot = True
            maze[i+1][j].top = True
            maze[i+1][j].visited = True
            stack.insert(0,maze[i+1][j])
            placed = True

        arr.remove(choice)

print("DONE MAKING MAZE")

maze_img = Image.new('RGB',(width*2,height*2))
white = (255,255,255)
black = (0,0,0)
for i in range(width):
    for j in range(height):

        try:

            maze_img.putpixel((i*2,j*2),white)

            maze_img.putpixel((i*2+1,j*2),(black if maze[i][j].bot == False else white))

            maze_img.putpixel((i*2-1,j*2),(black if maze[i][j].top == False else white))

            maze_img.putpixel((i*2,j*2+1),(black if maze[i][j].right == False else white))

            maze_img.putpixel((i*2,j*2-1),(black if maze[i][j].left == False else white))
        except:
            continue
maze_img.putpixel((width-2,height-1),white)
maze_img.show()

maze_img.save("yossiword.png")

im.show()