import random
import pygame
import numpy as np
from NN import *
from genetic import *
import math

CELL_SIZE = 20
XCELLS = 20
YCELLS = 20
HEIGHT = YCELLS * CELL_SIZE + CELL_SIZE
WIDTH = XCELLS * CELL_SIZE + CELL_SIZE
POPULATION_SIZE = 2000

class Cell:

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

def build_maze_map(width, height):
    maze = []

    for i in range(width):
        maze.append([])
        for j in range(height):
            maze[i].append(Cell(i,j))

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

    actual_maze = np.zeros((width*2, height*2))
    for i in range(width):
        for j in range(height):
            actual_maze[i*2,j*2] = 1
            actual_maze[i*2+1,j*2] = 0 if maze[i][j].bot == False else 1
            actual_maze[i*2-1,j*2] = 0 if maze[i][j].top == False else 1
            actual_maze[i*2,j*2+1] = 0 if maze[i][j].right == False else 1
            actual_maze[i*2,j*2-1] = 0 if maze[i][j].left == False else 1

    # add left and top black padding
    actual_maze = np.vstack((np.zeros((1,actual_maze.shape[1])),actual_maze))
    actual_maze = np.hstack((np.zeros((actual_maze.shape[0],1)),actual_maze))
    
    # make hole for exit
    actual_maze[-2, -1] = 1

    return actual_maze

UNIVERSAL_MAP = build_maze_map(XCELLS//2, YCELLS//2)

def count_whites(maze):
    count = 0
    for i in range(XCELLS):
        for j in range(YCELLS):
            if maze[i,j] == 1:
                count += 1
    return count

class Explorer(Individual):
    
        def __init__(self, genome=None):
            if genome is None:
                super().__init__(NeuralNetwork(8, 8, 4))
            else:
                super().__init__(genome)
            
            self.x = 1
            self.y = 1
            self.hp = count_whites(UNIVERSAL_MAP)
            self.map = UNIVERSAL_MAP
            for i in range(XCELLS):
                for j in range(YCELLS):
                    if self.map[i,j] == 1:
                        self.map[i,j] = 2
        
        def show(self, screen):
            pygame.draw.rect(screen, (255,0,0), (self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        
        def get_neighbor_tensor(self):
            
            tensor = []

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:
                        tensor.append(self.map[self.x+i, self.y+j])
            for i in range(len(tensor)):
                if tensor[i] == 1:
                    tensor[i] = 0.5
                if tensor[i] == 2:
                    tensor[i] = 1
            return np.array(tensor)
        
        def move(self, action):
            if action == 0 and self.map[self.x, self.y-1] in [1,2]:
                self.y -= 1
            elif action == 1 and self.map[self.x, self.y+1] in [1,2]:
                self.y += 1
            elif action == 2 and self.map[self.x-1, self.y] in [1,2]:
                self.x -= 1
            elif action == 3 and self.map[self.x+1, self.y] in [1,2]:
                self.x += 1
            
            if self.map[self.x, self.y] == 2:
                self.fitness += 1
                self.map[self.x, self.y] = 1

            self.hp -= 1

def fit(brains):
    for brain in brains:
        brain.fitness = brain.fitness**2

def show_map(screen):
    for i in range(XCELLS+1):
        for j in range(YCELLS+1):
            if UNIVERSAL_MAP[i, j] == 0:
                pygame.draw.rect(screen, (0,0,0), (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255,255,255), (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))

pygame.init()
disp = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

algor = GeneticAlgorithm(POPULATION_SIZE, Explorer, 0.1, fit, True, 3)

population = algor.indentical_population()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    show_map(disp)
    for brain in population:
        brain.show(disp)
    for i in range(10):
        for brain in population:
            inputs = brain.get_neighbor_tensor()
            outputs = brain.predict(inputs)
            direction_to_move = np.argmax(outputs)
            brain.move(direction_to_move)

            if brain.hp <= 0:
                population.remove(brain)

        if len(population) == 0:
            algor.next_generation()
            population = algor.indentical_population()
            print("GENERATION: ", algor.generation)

    pygame.display.flip()
    clock.tick(60)
