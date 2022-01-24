import pygame
import random

# setup pygame

screen_w = 500

screen_h = 500

pygame.init()

win = pygame.display.set_mode((screen_w, screen_h))

# game variables

tile_list = []

grid_list = []

game = []

score = 0

tile_images = [pygame.image.load('1010/1block.png'), pygame.image.load('1010/2block.png'), pygame.image.load('1010/3block.png')]


# classes

class Tile:

    def __init__(self, x, y, type):

        self.image = tile_images[type]

        self.x = x
        self.y = y

        self.Dx = x
        self.Dy = y

        self.type = type

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.width = self.rect.width
        self.height = self.rect.height

        self.in_grid = False

    def render(self):

        win.blit(self.image, [self.x, self.y])

    def setpos(self, x, y):

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y

    def CheckClick(self, x, y):

        if not self.in_grid and self.rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0] == 1:

            return True


class Grid:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.image = pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 25, 25), 1)

        self.image.x = self.x
        self.image.y = self.y

        self.tile_init = False

    def render(self):

        self.image = pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 25, 25), 1)

    def CheckInsert(self, tile):

        if self.image.collidepoint(tile.x, tile.y) and not self.tile_init:
            return True


class Text:

    def __init__(self, x, y, text):

        self.x = x
        self.y = y

        self.font = pygame.font.SysFont("comicsansms", 32)

        self.text = text

    def render(self, text):

        self.text = text

        image = self.font.render(self.text, True, (255, 255, 255))

        win.blit(image, (self.x, self.y))

# game generation functions


def generate_tiles():

    x = 1
    while x <= 3:

        x_pos = screen_w/3.9 * x - 20
        y_pos = screen_h - 100

        image_index = random.randint(0, len(tile_images)-1)
        tile_list.append(Tile(x_pos, y_pos, image_index))

        x += 1

def generate_grid():
    y = 0
    while y <= 9:

        y_pos = screen_h - 490 + 25 * y
        grid_list.append(list())
        game.append(list())

        x = 1
        while x <= 10:
            x_pos = screen_w / 20 * x + 100

            grid_list[y].append(Grid(x_pos, y_pos))
            game[y].append(0)

            x += 1

        y += 1

    font = pygame.font.SysFont("comicsansms", 32)

    global score_text
    score_text = Text(50, 50, str(score))

# game functions


def WinReload():

    win.fill((0, 0, 0))

    score_text.render(str(score))

    for tile in tile_list:
        tile.render()

    for overgrid in grid_list:
        for grid in overgrid:
            grid.render()

    pygame.display.update()

def CheckIllegal(overgrid, grid, tile):

    if tile.type == 1:

        if overgrid.index(grid) == 9:
            return True

        else:
            if overgrid[overgrid.index(grid) + 1].tile_init:
                tile.setpos(tile.Dx, tile.Dy)
                return True

    elif tile.type == 2:

        if grid_list.index(overgrid) == 9:
            return True

        else:

            if grid_list[grid_list.index(overgrid) + 1][overgrid.index(grid)].tile_init:
                return True

def CheckMatches():

    global matches_index
    matches_index = 0
    for line in game:

        if 0 not in line:

            global score
            score += 10

            x = 0
            for dot in line:

                try:
                    if dot.type == 2:

                        newtile = Tile(dot.x, dot.y+dot.height/2, 0)
                        newtile.image = pygame.image.load('1010/3block_single.png')
                        newtile.in_grid = True

                        game[game.index(line) + 1][line.index(dot)] = newtile
                        tile_list.append(newtile)

                    tile_list.remove(dot)

                except:

                    if dot == 'part_two_special':
                        print(game[game.index(line) - 1][x])
                        game[game.index(line) - 1][x].image = pygame.image.load('1010/3block_single.png')
                        game[game.index(line) - 1][x].type = 0

                x += 1

            line_index = game.index(line)

            for overgrid in grid_list:

                    if grid_list.index(overgrid) == game.index(line):

                        for grid in overgrid:
                            grid.tile_init = False

            game[line_index].clear()

            x = 1

            while x <= 10:
                game[line_index].append(0)

                x += 1
    #CheckMatchesVertical()

"""def CheckMatchesVertical():
    matching = 1
    Stop = False
    for line in game:

        global matches_index
        if matches_index == 9:
            Stop = True

        if game[game.index(line)][matches_index] is not 0 and game[game.index(line) + 1][matches_index] is not 0:
            matching += 1

        if matching == 10:

            for line in game:
                try:
                    tile_list.remove(line[matches_index])

                except:
                    continue

            matches_index = 0
            Stop = True

    if not Stop:
        matching = 1
        matches_index += 1
        CheckMatchesVertical()"""





# main loop


generate_grid()

generate_tiles_once = 3
run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    if generate_tiles_once == 3:

        generate_tiles()
        generate_tiles_once = 0

    mx, my = pygame.mouse.get_pos()

    for tile in tile_list:

        illegal = False

        if tile.CheckClick(mx, my):

            tile.setpos(mx - tile.width/2, my - tile.height/2)

        else:

            for overgrid in grid_list:
                for grid in overgrid:
                    if grid.CheckInsert(tile) and not tile.in_grid:

                        illegal = CheckIllegal(overgrid, grid, tile)

                        if not illegal:
                            tile.setpos(grid.x, grid.y)

                            line_index = grid_list.index(overgrid)
                            dot_index = overgrid.index(grid)

                            game[line_index][dot_index] = tile

                            tile.in_grid = True
                            grid.tile_init = True

                            if tile.type == 0:

                                score += 1

                            if tile.type == 1:

                                score += 2

                                overgrid[dot_index + 1].tile_init = True
                                game[line_index][dot_index + 1] = 'part_two'

                            elif tile.type == 2:

                                score += 2

                                grid_list[line_index + 1][dot_index].tile_init = True
                                game[line_index + 1][dot_index] = 'part_two_special'

                            generate_tiles_once += 1

            if not tile.in_grid:
                tile.setpos(tile.Dx, tile.Dy)

            CheckMatches()

    WinReload()

pygame.quit()