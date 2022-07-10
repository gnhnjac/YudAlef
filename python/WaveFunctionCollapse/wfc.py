import pygame
from PIL import Image

CHUNK_SIZE = 10
TOP = 0
RIGHT = 1
BOT = 2
LEFT = 3

class Tile:

    def __init__(self, img, size):
        self.img = img
        self.size = size

        self.top_socket = []
        self.left_socket = []
        self.right_socket = []
        self.bot_socket = []

        for i in range(self.size):
            self.top_socket.append(self.img[i, 0])
            self.bot_socket.append(self.img[i,self.size-1])
            self.left_socket.append(self.image[0, i ])
            self.right_socket.append(self.image[self.size-1,i])
    
    def check_match(self, tile, side):

        if side == TOP and self.top_socket == other.bot_socekt



def generate_tileset(image_path):
    
    img = Image.open(image_path)

    pix = img.load()

    for i in range(pix.size[0]//CHUNK_SIZE):
        for j in range(pix.size[1]//CHUNK_SIZE):





class Cell:

    def __init__(self, x, y, size):

        self.collapsed = False
        self.tile = None
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):

        if self.tile is None:
            pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.size, self.size))
            pygame.draw.rect(screen, (255,255,255), (self.x, self.y, self.size, self.size), 1)
        else:
            screen.blit(self.tile, (self.x, self.y, self.size, self.size))

class WFC:
    def __init__(self, screen_width, screen_height, cell_size, tiles):
        self.width = screen_width//cell_size
        self.height = screen_height//cell_size
        self.cell_size = cell_size
        self.tiles = tiles

        self.grid = [[Cell(i*cell_size, j*cell_size, cell_size) for j in range(self.height)] for i in range(self.width)]

    def draw(self, screen):

        for i in range(self.width):
            for j in range(self.height):
                self.grid[i][j].draw(screen)

        


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((800, 600))

wfc = WFC(WIDTH, HEIGHT, 50, [])

pygame.display.set_caption("WFC")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    wfc.draw(screen)

    pygame.display.update()