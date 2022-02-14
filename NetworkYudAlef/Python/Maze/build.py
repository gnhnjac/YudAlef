from PIL import Image
import random

width,height = 1500,1500

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

maze = []

for i in range(width):
    maze.append([])
    for j in range(height):
        maze[i].append(cell(i,j))

i = 0
j = 0
stack = []
cell = maze[i][j]
cell.visited = True
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

#maze_img.putpixel((0,0),(0,255,0))
maze_img.putpixel((width*2-2,height*2-1),(255,255,255))
maze_img.show()
maze_img.save("maze.png")