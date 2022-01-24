import pygame
import pygame.math
import random

# pygame config

pygame.init()

# game config & variables

ACTUALSIZE = 800

BOARDSIZE = ACTUALSIZE - 300

window = pygame.display.set_mode((BOARDSIZE, ACTUALSIZE))

NumberOfTiles = 10

TileSize = BOARDSIZE / NumberOfTiles

Board = []

Tiles = []

for y in range (0,NumberOfTiles):

    Board.append([])

    for x in range(0,NumberOfTiles):
        Board[y].append(0)

# classes

class Tile:

    def __init__(self, x, y, w, h, type, blocks):

        self.pos = pygame.math.Vector2()
        self.pos.x = x
        self.pos.y = y

        self.w = w
        self.h = h

        self.blocks = blocks
        self.blockBundle = []

        if type == 0:

            self.blockBundle.append(pygame.Rect(self.pos.x-self.w/2, self.pos.y-self.h/2, self.w, self.h))

    def render(self):

        for i in range (0, self.blocks):

            pygame.draw.rect(window, (0,0,0), (self.blockBundle[i].x, self.blockBundle[i].y, self.blockBundle[i].w, self.blockBundle[i].h))

    def checkCol(self, coords, click):
        for i in range (0, self.blocks):
            if self.blockBundle[i].collidepoint(coords[0], coords[1]) and click:
                print(self.blockBundle[i].x)
                return True

# functions

def drawBoard():

    for y in range(0, NumberOfTiles):

        for x in range(0, NumberOfTiles):

            pygame.draw.rect(window, (0,0,0), (x * TileSize, y * TileSize, TileSize, TileSize), 1)

# main

for i in range(1,4):
    Tiles.append(Tile(BOARDSIZE/4*i, BOARDSIZE+150, TileSize, TileSize, 0, 1))


run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    mousepos = pygame.mouse.get_pos()
    mouseclick = pygame.mouse.get_pressed()[0]

    window.fill((255,255,255))

    drawBoard()

    for tile in Tiles:
        tile.render()
        if tile.checkCol(mousepos, mouseclick):

            tile.x =

    pygame.display.update()

pygame.quit()