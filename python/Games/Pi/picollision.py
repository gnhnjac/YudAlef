import pygame
from random import uniform
from math import sqrt

pygame.init()

width = 500
height = 300

window = pygame.display.set_mode((width, height))

digits = 1

class Square:

    def __init__(self, x, w, m, v, color):

        self.x = x
        self.y = height-w

        self.w = w

        self.m = m

        self.v = v

        self.color = color


    def show(self):

        self.x += self.v

        pygame.draw.rect(window, self.color, (self.x, self.y, self.w, self.w))

    def collide(self, other):

        return not (self.x > other.x+other.w or self.x+self.w < other.x)

    def bounce(self, other):

        sumM = self.m + other.m
        newV = (self.m - other.m)/sumM * self.v + (2 * other.m)/sumM * other.v

        return newV

    def hitWall(self):
        if (self.x <= 0):
            return True

    def reverse(self):

        self.v *= -1

A = Square(300, 100, 100 ** digits, -0.01, [255, 0, 0])

B = Square(100, 20, 1, 0, [0, 255, 0])

Collision = 0

run = True
while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    pygame.draw.rect(window, [0,0,0], (0,0,width,height))

    if (B.collide(A)):

        v1 = A.bounce(B)
        v2 = B.bounce(A)

        A.v = v1
        B.v = v2

        Collision += 1

    if (B.hitWall()):

        B.reverse()

        Collision += 1

    print(Collision*2)

    A.show()
    B.show()

    pygame.display.flip()

pygame.quit()

