import pygame
from NN import *
from genetic import *
import random

WIDTH = 640
HEIGHT = 640
BLOCK_SIZE = 20
FPS = 60

class Snake:

    def __init__(self, brain=None):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.velocity = 0
        self.gravity = 0.5
        self.size = BLOCK_SIZE
        self.color = (255, 255, 255)
        if brain is None:
            self.model = NeuralNetwork(5,8,2)
        else:
            self.model = brain.copy()

        self.score = 0
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    display.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)