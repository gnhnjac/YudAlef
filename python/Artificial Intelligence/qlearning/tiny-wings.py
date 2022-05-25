import pygame
from NN import *
from genetic import *
import numpy as np
import random
import math

# a tiny birds (the mobile game) genetic algorithm

# sin^2 = more frequent
# sin * x = more/less sloped
# sin(x * n) = more/less sloped
# sin (x + n) = n -> move along axis

def hill_function(x):
    return math.sin(x/100 + 200) * 100 + 200

WIDTH = 800
HEIGHT = 400
ACCURACY = 5
MAX_VELOCITY = 10

class Bird(Individual):

    def __init__(self, genome=None):
        if genome is None:
            super().__init__(NeuralNetwork(3, 5, 2)) # 3 inputs - dist from ground, y velocity, x velocity, 2 outputs - ground slam, do nothing 
        else:
            super().__init__(genome)
        self.points = []
        self.sticks = []
        self.score = 0
        self.saved_velocity = 0
        self.failed = False
        self.top_height = 0
        self.fitness = 0

        # add points in the shape of a circle
        for i in range(0, 360, 40):
            self.points.append(Point(WIDTH/2 + math.cos(i) * 100, HEIGHT/2 + math.sin(i) * 100))
        
        # add sticks
        for i in range(len(self.points) - 1):
            self.sticks.append(Stick(self.points[i], self.points[i+1], 30))
        self.sticks.append(Stick(self.points[-1], self.points[0], 30))
    
    def update(self):
        for point in self.points:
            point.solve_position()
        for i in range(ACCURACY):
            for stick in self.sticks:
                stick.update()
    
    def draw(self, surface):
        for point in self.points:
            point.draw(surface)
        for stick in self.sticks:
            stick.draw(surface)

    def ground_press(self):
        pass

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.friction = 0.9
        self.gravity = 0.5
    
    def solve_position(self):

        # solve position using verlet integation

        self.xvel = (self.x - self.last_x) * self.friction
        self.yvel = (self.y - self.last_y) * self.friction

        self.last_x = self.x
        self.last_y = self.y
        self.x += self.xvel
        self.y += self.yvel
        self.y += self.gravity
    
    def constrain(self):
        if self.y > hill_function(self.x):
            self.y = hill_function(self.x)
            self.last_y = self.y + self.yvel
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 2)

class Stick:

    def __init__(self, p1, p2, len):
        self.p1 = p1
        self.p2 = p2
        self.len = len
    

    
    def update(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        dist = math.sqrt(dx**2 + dy**2)
        diff = self.len - dist
        precent = diff / dist / 2
        offx = dx * precent
        offy = dy * precent
        self.p1.x -= offx
        self.p1.y -= offy
        self.p2.x += offx
        self.p2.y += offy

        self.p1.constrain()
        self.p2.constrain()
    
    def draw(self, surface):
        pygame.draw.line(surface, (255, 255, 255), (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 3)


def draw_surface(surface, xoff):
    for x in range(WIDTH):
        y = hill_function(x + xoff)
        pygame.draw.line(surface, (255, 255, 255), (x, y), (x, y+10))


def fit(birds):
    for bird in birds:
        bird.fitness = bird.x + bird.top_height    

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("Tiny Birds")

font = pygame.font.SysFont(None, 30)

ga = GeneticAlgorithm(500, Bird, 0.1, fit, True, 3)

birds = ga.indentical_population()

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keyboard = pygame.key.get_pressed()
    if keyboard[pygame.K_SPACE]:
        birds[0].ground_press()

    display.fill((0, 0, 0))

    draw_surface(display, birds[0].points[0].x)

    for bird in birds:
        bird.update()
    birds[0].draw(display)

    pygame.display.update()
    clock.tick(60)