import pygame

# pygame config

pygame.init()

wwidth = 500

wheight = 500

win = pygame.display.set_mode((wwidth, wheight))

tiles = [pygame.image.load('1010/1block.png')]

tile_list = []

grid_list = []

game = []

class Tile(object):

    def __init__(self, image, x, y):

        global win
        self.win = win

        self.img = image

        self.x = x

        self.y = y

        self.Dx = x

        self.Dy = y

        self.rect = self.img.get_rect()

        self.rect.x = self.x

        self.rect.y = self.y

        self.in_grid = False

    def render(self):
        try:

            self.win.blit(self.img, [self.x, self.y])

        except:
            print('An error has occurred while the game was rendering the image.')

    def setpos(self, x, y):

        self.x = x

        self.y = y

        self.rect.x = self.x

        self.rect.y = self.y

    def checkclick(self, x, y):

        if self.rect.collidepoint(x, y) and mouse_keys[0] == 1:
            return True


class Grid(object):

    def __init__(self, x, y):

        global win
        self.win = win

        self.x = x
        self.y = y

        self.img = pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 55, 55), 1)

        self.img.x = self.x
        self.img.y = self.y

        self.tile_init = False
        self.tile = False

    def render(self):

        self.img = pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 55, 55), 1)

    def checkinsert(self, tile):

        if self.img.collidepoint(tile.x, tile.y) and not self.tile_init:
            return True

# create grid


y = 0
while y <= 4:

    y_pos = wheight - 500 + 55 * y
    game.append(list())
    grid_list.append(list())

    x = 1
    while x <= 5:
        x_pos = wwidth/9.4 * x + 50

        grid_list[y].append(Grid(x_pos, y_pos))

        game[y].append(0)

        x += 1

    y += 1

def reload_win():

    for overgame in game:
        if not 0 in overgame:
            for subgame in overgame:

                for overgrid in grid_list:
                    for grid in overgrid:
                        if grid.tile == subgame:
                            grid.tile = False
                            grid.tile_init = False
                tile_list.remove(subgame)

            index = game.index(overgame)

            game[index] = list()

            x = 0
            while x <= 4:
                game[index].append(0)
                x += 1


    for overgrid in grid_list:
        for grid in overgrid:
            grid.render()

    x = 0
    for tile in tile_list:
        tile.render()
        tile_list[x] = tile
        x += 1

    pygame.display.update()
    win.fill((0, 0, 0))


create_tiles = True
run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

    # game setup

    if create_tiles:
        _, _, width, height = tiles[0].get_rect()

        x = 1
        while x <= 3:

            xpos = wwidth - (wwidth/3 * x) + width
            ypos = wheight - 100

            newtile = Tile(tiles[0], xpos, ypos)

            tile_list.append(newtile)

            x += 1

        create_tiles = False

    mouse_keys = pygame.mouse.get_pressed()

    NoneLeft = len(tile_list)
    for tile in tile_list:

        mousex, mousey = pygame.mouse.get_pos()

        isTrue = tile.checkclick(mousex, mousey)

        if isTrue and not tile.in_grid:
            tile.setpos(mousex - 22, mousey - 22)

        elif not isTrue and not tile.in_grid:
            for overgrid in grid_list:
                for grid in overgrid:
                    if grid.checkinsert(tile):
                        tile.setpos(grid.x, grid.y)
                        tile.in_grid = True
                        grid.tile_init = True
                        grid.tile = tile
                        for ovv in grid_list:
                            if grid in ovv:
                                dot = ovv.index(grid)
                                line = grid_list.index(ovv)
                        game[line][dot] = tile

            if not tile.in_grid and not isTrue:
                tile.setpos(tile.Dx, tile.Dy)


        if tile.in_grid:
            NoneLeft -= 1

        if NoneLeft == 0:
            create_tiles = True

    reload_win()

pygame.quit()

