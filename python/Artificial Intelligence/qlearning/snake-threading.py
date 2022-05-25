import pygame
from NN import *
from genetic import *
import random
import math
import numpy as np
import threading

POPULATION_SIZE = 500
BLOCK_SIZE = 12
WIDTH = 20*BLOCK_SIZE
HEIGHT = 20*BLOCK_SIZE
MAX_MOVES = 200
SNAKES_TO_SHOW = 3
FPS = 60
LOCK = threading.Lock()

def remap( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

class Snake(Individual):

    def __init__(self, brain=None):
        if brain is None:
            super().__init__(NeuralNetwork(24,18, 4))
        else:
            super().__init__(brain)

        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.size = BLOCK_SIZE
        self.length = 4
        self.color = (255, 255, 255)
        self.history = []
        self.board_history = []
        self.board = [[0 for x in range(WIDTH//BLOCK_SIZE)] for y in range(HEIGHT//BLOCK_SIZE)]
        self.board[self.get_boardx()][self.get_boardy()] = -1
        self.history.append((self.x, self.y))
        self.cherry_x = 0
        self.cherry_y = 0
        self.place_cherry()
        self.board_history.append(copy.deepcopy(self.board))
        self.direction = 1
        self.moves_left = MAX_MOVES

    def move(self):
        if self.direction == 0:
            self.y -= self.size
        elif self.direction == 2:
            self.y += self.size
        elif self.direction == 3:
            self.x -= self.size
        elif self.direction == 1:
            self.x += self.size

        if self.get_boardx() == self.cherry_x and self.get_boardy() == self.cherry_y:
            self.eat()

        if self.get_boardx() >= 0 and self.get_boardx() < WIDTH//self.size and self.get_boardy() >= 0 and self.get_boardy() < HEIGHT//self.size:
            self.board[self.get_boardx()][self.get_boardy()] = -1
            self.history.append((self.x, self.y))

        if len(self.history) > self.length:
            x, y = self.history.pop(0)
            self.board[x//self.size][y//self.size] = 0
            
        self.board_history.append(copy.deepcopy(self.board))
    
    def eat(self):
        self.length += 1
        self.moves_left += MAX_MOVES//2
        if self.moves_left > 500:
            self.moves_left = 500
        self.place_cherry()

    def change_direction(self, direction):
        if direction == 0 and self.direction != 2:
            self.direction = 0
        elif direction == 2 and self.direction != 0:
            self.direction = 2
        elif direction == 3 and self.direction != 1:
            self.direction = 3
        elif direction == 1 and self.direction != 3:
            self.direction = 1
        
    def update(self):
        self.moves_left -= 1
        self.fitness += 1

    def draw(self, screen, xoff=0, yoff=0):
        for x, y in self.history:
            pygame.draw.rect(screen, self.color, (x + xoff, y + yoff, self.size, self.size))

    def collide(self):
        if self.hit_wall(self.get_boardx(), self.get_boardy()):
            return True
        for x, y in self.history[:-1]:
            if self.x == x and self.y == y:
                return True
        return False
    
    def hit_wall(self, x, y):
        if x < 0 or x > WIDTH//self.size-1 or y < 0 or y > HEIGHT//self.size-1:
            return True
    
    def hit_self(self, x, y):
        if self.board[x][y] == -1:
            return True
        return False

    def collide_coords(self, x_coor, y_coor):
        return self.hit_wall(x_coor, y_coor) or self.hit_self(x_coor, y_coor)

    def get_boardx(self):
        return self.x//self.size
    
    def get_boardy(self):
        return self.y//self.size

    def get_board_item(self, x, y):
        return self.board[x][y]

    def place_cherry(self):
        while True:
            x = random.randint(0, WIDTH//self.size-1)
            y = random.randint(0, HEIGHT//self.size-1)
            if self.get_board_item(x, y) == 0:
                self.board[x][y] = 1
                self.cherry_x = x
                self.cherry_y = y
                break

    def block_dist_from_cherry(self, x, y):
        return math.sqrt(pow(x-self.cherry_x, 2) + pow(y-self.cherry_y, 2))

    def look_in_direction(self, direction):
        vec = [self.get_boardx(), self.get_boardy()]
        vec[0] += direction[0]
        vec[1] += direction[1]
        tensor = [0,0,0]
        dist_from_wall = 0
        while not self.hit_wall(vec[0], vec[1]):

            if self.hit_self(vec[0], vec[1]):
                tensor[0] = 1
            if self.get_board_item(vec[0], vec[1]) == 1:
                tensor[1] = 1#/self.block_dist_from_cherry(self.get_boardx(), self.get_boardy())
            dist_from_wall += 1
            vec[0] += direction[0]
            vec[1] += direction[1]

        if dist_from_wall == 0:
            tensor[2] = 1
        else:
            tensor[2] = 1/dist_from_wall
        return tensor

    def get_vision_tensor(self):
        tensor = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                for k in self.look_in_direction([i,j]):
                    tensor.append(k)
        return tensor
        

    def reset(self):
        self.__init__(self.genes)
    
def fit(brains):
    for brain in brains:
        brain.fitness = (brain.fitness**2) * (2**brain.length)
        if brain.length >= 10:
            brain.fitness *= brain.length-9

def update(snake):
    global snakes
    inputs = snake.get_vision_tensor()
    guess = np.argmax(snake.predict(inputs))

    snake.change_direction(guess)
    snake.move()
    snake.update()

    if snake.collide() or snake.moves_left <= 0:
        LOCK.acquire()
        snakes.remove(snake)
        LOCK.release()

pygame.init()
display = pygame.display.set_mode((WIDTH*SNAKES_TO_SHOW, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

ga = GeneticAlgorithm(POPULATION_SIZE, Snake, 0.1, fit, True, 3)
snakes = ga.indentical_population()
moves_per_cycle = 1
longest_record = 0
view = 0
best_snake = None
longest_snake = None
history_index = 0
keep_training = True

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moves_per_cycle -= 1
            elif event.key == pygame.K_RIGHT:
                moves_per_cycle += 1
            elif event.key == pygame.K_a:
                if FPS <= 10:
                    FPS -= 1
                else:
                    FPS -= 10
            elif event.key == pygame.K_d:
                if FPS < 10:
                    FPS += 1
                else:
                    FPS += 10
            elif event.key == pygame.K_SPACE:
                view = (view + 1) % 4
                history_index = 0
            elif event.key == pygame.K_s:
                keep_training = not keep_training


    if view == 0 or view == 1 or keep_training:
        for n in range(moves_per_cycle):
            
            threads = []

            for snake in snakes:
                t = threading.Thread(target=update, args=(snake,))

                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()

                
            if len(snakes) == 0:
                ga.next_generation()
                snakes = ga.indentical_population()
                best_snake = ga.get_best_brain(ga.generation-1)
        
            
            longest = 0
            longest_snk = None
            for snake in snakes:
                if snake.length > longest:
                    longest = snake.length
                    longest_snk = snake
            if longest > longest_record:
                longest_record = longest
                longest_snake = longest_snk

    display.fill((0, 0, 0))

    if view == 0 or view == 1:
        for k in range(SNAKES_TO_SHOW):
            if len(snakes) > k:
                for i in range(WIDTH//BLOCK_SIZE):
                    for j in range(HEIGHT//BLOCK_SIZE):
                        val = snakes[k].get_board_item(i, j)
                        
                        if val == 1:
                            col = [255, 0, 0]
                        elif val == -1:
                            col = [255, 255, 255]
                        else:
                            col = [0, 0, 0]

                        # found = False
                        # for n in range(-1, 2):
                        #     for m in range(-1, 2):
                        #         vec = [snakes[k].get_boardx()+n, snakes[k].get_boardy()+m]
                        #         while not snakes[k].collide_coords(vec[0],vec[1]):
                        #             if vec[0] == i and vec[1] == j:
                        #                 col[0] += 20
                        #                 col[1] += 20
                        #                 col[2] += 20
                        #                 if col[0] > 255:
                        #                     col[0] = 255
                        #                 if col[1] > 255:
                        #                     col[1] = 255
                        #                 if col[2] > 255:
                        #                     col[2] = 255
                        #                 found = True
                        #                 break
                        #             vec[0] += n
                        #             vec[1] += m
                        #         if found:
                        #             break
                        #     if found:
                        #         break
                        pygame.draw.rect(display, col, (i*BLOCK_SIZE + k*WIDTH, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

                if view == 1:
                    for snake in snakes:
                        snake.draw(display, k*WIDTH)

    elif view == 2 or view == 3:
        if best_snake == None:
            pass
        else:
            if view == 2:
                snk = best_snake
            else:
                snk = longest_snake

            if len(snk.board_history) == 0:
                pass
            else:
                board_hist = snk.board_history[history_index]

                for i in range(len(board_hist)):
                    for j in range(len(board_hist[i])):
                        if board_hist[i][j] == 1:
                            pygame.draw.rect(display, (255, 0, 0), (i*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        elif board_hist[i][j] == -1:
                            pygame.draw.rect(display, (255, 255, 255), (i*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        else:
                            pygame.draw.rect(display, (0, 0, 0), (i*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                history_index = (history_index + 1) % len(snk.board_history)


    gen_text = font.render("Generation: " + str(ga.generation), True, (255, 255, 255))
    display.blit(gen_text, (0, 0))
    cycle_text = font.render("MPC: " + str(moves_per_cycle), True, (255, 255, 255))
    display.blit(cycle_text, (0, 20))
    fps_text = font.render("FPS: " + str(FPS), True, (255, 255, 255))
    display.blit(fps_text, (0, 40))
    longest_txt = font.render("Longest: " + str(longest_record), True, (255, 255, 255))
    display.blit(longest_txt, (0, 60))
    snakes_left_txt = font.render("Snakes left: " + str(len(snakes)), True, (255, 255, 255))
    display.blit(snakes_left_txt, (0, 80))
    v_txt = "Normal" if view == 0 else "All" if view == 1 else "Top of prev" if view == 2 else "Longest"
    view_txt = font.render("View: " + v_txt, True, (255, 255, 255))
    display.blit(view_txt, (0, 100))

    pygame.display.flip()
    clock.tick(FPS)