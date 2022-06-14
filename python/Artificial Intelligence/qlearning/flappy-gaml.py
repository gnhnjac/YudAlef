from asyncio.subprocess import PIPE
import random
import pygame
import numpy as np
from NN_ML import *
import copy
from genetic import *

from genetic import GeneticAlgorithm

HEIGHT = 480
WIDTH = 640
BIRD_RADIUS = 20
PIPE_WIDTH = 80
PIPE_SPEED = 6
PIPE_GAP = 200
PIPE_INTERVAL = 75
BIRD_COUNT = 500
MAX_VELOCITY = 12#8
FPS = 60

def remap( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


# classes
class Bird(Individual):

    def __init__(self, brain=None):

        if brain is None:
            super().__init__(NeuralNetwork(5,[8],2))
        else:
            super().__init__(brain)

        self.x = 60
        self.y = HEIGHT/2
        self.velocity = 0
        self.gravity = 0.5
        self.size = BIRD_RADIUS
        self.color = (255, 255, 255)
        self.jump_height = -MAX_VELOCITY

    
    def jump(self):
        self.velocity = self.jump_height
    
    def update(self):
        self.velocity += self.gravity
        if self.velocity > MAX_VELOCITY:
            self.velocity = MAX_VELOCITY
        self.y += self.velocity
        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        self.fitness += 1
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
    
    def collide(self, pipes):
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                if self.x + self.size > pipe.x and self.x - self.size < pipe.x + pipe.width:
                    if self.y + self.size > pipe.y and self.y - self.size < pipe.y + pipe.height:
                        return True
        return False

class Pipe:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
    
    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

def fit(brains):
    for brain in brains:
        brain.fitness = brain.fitness**2

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 30)

ga = GeneticAlgorithm(BIRD_COUNT, Bird, 0.1, fit, True, 3)

pipes = []
birds = ga.indentical_population()

counter = 0
score = 0
best_score = 0
single_bird = False
passed_pipe = None
n = 1
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                n -= 1
                if n < 0:
                    n = 0
            if event.key == pygame.K_RIGHT:
                n += 1
            if event.key == pygame.K_SPACE:
                single_bird = not single_bird


    display.fill((0, 0, 0))

    for j in range(n):
        if counter % PIPE_INTERVAL == 0:
            bot_y = random.randint(PIPE_GAP, HEIGHT)
            pipes.append([Pipe(WIDTH, bot_y, PIPE_WIDTH, HEIGHT - bot_y),Pipe(WIDTH, 0, PIPE_WIDTH, bot_y - PIPE_GAP)])
            counter = 0
        counter += 1

        for pipe_pair in pipes:
            for pipe in pipe_pair:
                pipe.update()
                if pipe.x < -PIPE_WIDTH:
                    pipes.remove(pipe_pair)
                    break
        
        if birds[0].x > pipes[0][0].x + PIPE_WIDTH and pipes[0] != passed_pipe:
            score += 1
            passed_pipe = pipes[0]
            

        for bird in birds:

            y = remap(bird.y, 0, HEIGHT, 0, 1)

            closest = None
            closest_dist = None
            for pipe_pair in pipes:
                pipe = pipe_pair[0]
                dist = pipe.x + pipe.width - bird.x
                if (closest_dist == None or dist < closest_dist) and dist > 0:
                    closest = pipe_pair
                    closest_dist = dist

            top_y = remap(closest[1].height, 0, HEIGHT-PIPE_GAP, 0, 1)
            bot_y = remap(closest[0].y, PIPE_GAP, HEIGHT, 0, 1)
            dist = remap(closest[0].x + closest[0].width, bird.x, WIDTH + closest[0].width, 0, 1)
            vel = remap(bird.velocity, -MAX_VELOCITY, MAX_VELOCITY, 0, 1)
            inputs = np.array([[y, dist, top_y, bot_y, vel]])

            prediction = bird.predict(inputs)[0]

            if prediction[0] > prediction[1]:
                bird.jump()

            bird.update()
            if bird.collide(pipes) or bird.y >= HEIGHT or bird.y <= 0:
                birds.remove(bird)
        
        if len(birds) == 0:
            counter = 0
            if score > best_score:
                best_score = score
            score = 0
            pipes = []
            ga.next_generation()
            birds = ga.indentical_population()

    if single_bird:
        birds[0].draw(display)
    else:
        for bird in birds:
            bird.draw(display)
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pipe.draw(display)

    text = font.render("Generation: " + str(ga.generation), 1, (255, 0, 0))
    display.blit(text, (10, 10))
    n_text = font.render("n: " + str(n), 1, (255, 0, 0))
    display.blit(n_text, (10, 50))
    score_text = font.render("Score: " + str(score), 1, (255, 0, 0))
    display.blit(score_text, (10, 90))
    best_score_text = font.render("Best Score: " + str(best_score), 1, (255, 0, 0))
    display.blit(best_score_text, (10, 130))
    
    pygame.display.update()
    clock.tick(FPS)