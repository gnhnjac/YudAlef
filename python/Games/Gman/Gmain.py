wimport pygame
import random
import time
import threading

pygame.init()

screen = pygame.display.set_mode((1000, 500))

screenw = screen.get_rect().size[0]
screenh = screen.get_rect().size[1]

class plat:

    def __init__(self, parv, w, h, x, y, color):

        self.parve = parv

        self.w = w
        self.h = h

        self.x = x
        self.y = y

        self.color = color

    def render(self):

        self.x -= self.parve

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

class player:

    def __init__(self, imagep, x, y, g, iscollision, name):

        self.image = pygame.transform.scale(pygame.image.load(imagep), (40, 40))
        self.name = name

        self.w = self.image.get_rect().size[0]
        self.h = self.image.get_rect().size[1]

        self.x = x
        self.y = y

        self.g = g
        self.iscollision = iscollision

        self.upflip = False
        self.powerclock = 5000

    def render(self):

        if not self.iscollision:
            if self.g == "d":
                if self.upflip:
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.upflip = False
                self.y += 0.15
            if self.g == "u":

                if not self.upflip:
                    self.image = pygame.transform.flip(self.image, False, True)
                    self.upflip = True
                self.y -= 0.15

        screen.blit(self.image, (self.x, self.y))

    def collision(self, x, y, w, h):

        if self.y+self.h >= screenh-40 or self.y <= 40:
            return True
        if ((self.y+self.h >= y and self.y+self.h <= y+h) or (self.y <= y+h and self.y >= y)) and (self.x+self.w >= x and self.x <= x+w):
            return 10
        else:
            return False

    def tinify(self):

        self.image = pygame.transform.scale(self.image, (20, 20))
        self.w = self.image.get_rect().size[0]
        self.h = self.image.get_rect().size[1]

    def biggify(self):

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.w = self.image.get_rect().size[0]
        self.h = self.image.get_rect().size[1]


powers = []
players = []
platforms = []

players.append(player("p1.png", 50, screenh/2, "d", False, "Player 1"))
players.append(player("p2.png", 5, screenh/2, "d", False, "Player 2"))

platforms.append(plat(0, screenw, 10, 0, screenh-40, [0,0,0]))

platforms.append(plat(0, screenw, 10, 0, 30, [0,0,0]))

startg = False

powerclock = 0

def plat_gen():

    if startg:
        threading.Timer(3.0, plat_gen).start()

        x = 0
        while x < 4:
            rw = random.randint(100, 500)
            ry = random.randint(30, screenh-50)

            platforms.append(plat(0.2, rw, 10, screenw, ry, [255, 0, 0]))
            x+=1

        ispowersummon = random.randint(2,2)

        if ispowersummon == 2:

            ry = random.randint(30, screenh - 50)

            powers.append(plat(0.3, 10, 10, screenw, ry, [0, 255, 0]))

doitonce = False
fullscreen = False
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    if key[pygame.K_F11] and not fullscreen:

        fullscreen = True

        screen = pygame.display.set_mode((1000,500), pygame.FULLSCREEN)
        time.sleep(3)


    elif key[pygame.K_F11] and fullscreen:

        fullscreen = False

        screen = pygame.display.set_mode((1000, 500))
        time.sleep(3)

    if key[pygame.K_h]:
        startg = True

    if startg:

        if not doitonce:
            plat_gen()
            doitonce = True

        # p1

        # up
        if key[pygame.K_w]:

            # if stuck in down
            if players[0].iscollision and players[0].g == "d":

                # free from position
                players[0].y -= 10
                players[0].iscollision = False

            players[0].g = "u"

        # down
        if key[pygame.K_s]:

            # if stuck in up
            if players[0].iscollision and players[0].g == "u":

                # free from position
                players[0].y += 10
                players[0].iscollision = False

            players[0].g = "d"

        # p2

        # up
        if key[pygame.K_UP]:

            # if stuck in down
            if players[1].iscollision and players[1].g == "d":
                # free from position
                players[1].y -= 10
                players[1].iscollision = False

            players[1].g = "u"

        # down
        if key[pygame.K_DOWN]:

            # if stuck in up
            if players[1].iscollision and players[1].g == "u":
                # free from position
                players[1].y += 10
                players[1].iscollision = False

            players[1].g = "d"

        screen.fill([255, 255, 255])

        for platform in platforms:

            for player in players:

                if player.collision(platform.x, platform.y, platform.w, platform.h) == 10:
                    players.remove(player)
                    print(players[0].name + " Won")
                    run = False
                elif player.collision(platform.x, platform.y, platform.w, platform.h):
                    player.iscollision = True
                else:
                    player.iscollision = False

            if platform.x+platform.w < 0:
                platforms.remove(platform)

            platform.render()

        for power in powers:

            for player in players:
                if player.collision(power.x, power.y, power.w, power.h) == 10:

                    player.tinify()
                    powers.remove(power)

                    player.powerclock = 0

            power.render()

        for player in players:

            player.powerclock += 1

            if player.powerclock >= 5000:
                player.biggify()
            else:
                pygame.draw.rect(screen, [0, 0, 0], (player.x, player.y - 10, player.powerclock/250, 5))

            player.render()

        pygame.display.update()

pygame.quit()