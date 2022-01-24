import pygame
from random import uniform
from time import sleep

pygame.init()

width = 500
height = 500

window = pygame.display.set_mode((width, height))

functionm = -0.3

functionb = 0.2

def f(x):

    return functionm * x + functionb

def map(OldValue, OldMin , OldMax, NewMin, NewMax):

    OldRange = (OldMax - OldMin)
    NewRange = (NewMax - NewMin)

    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

    return NewValue

def sign(n):

    if n >= 0:
        return 1
    else:
        return -1

class Perceptron:

    def __init__(self, n):

        self.weights = [0] * n

        for i in range(0, len(self.weights)):
            self.weights[i] = uniform(-1, 1)

        self.lr = 0.1


    def guess(self, inputs):

        sum = 0
        for i in range(0, len(self.weights)):
            sum += self.weights[i]*inputs[i]

        return sign(sum)

    def train(self, inputs, label):

        error = label - self.guess(inputs)

        for i in range(0, len(self.weights)):

            self.weights[i] += error*inputs[i]*self.lr

    def guessY(self, x):

        return -(self.weights[2]/self.weights[1]) - (self.weights[0]/self.weights[1]) * x



class Point:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.bias = 1

        self.label = 0

        if f(self.x) < self.y:
            self.label = 1
        else:
            self.label = -1

    def pixelX(self):

        return map(self.x, -1, 1, 0, width)

    def pixelY(self):

        return map(self.y, -1, 1, height, 0)

    def show(self):

        px = self.pixelX()
        py = self.pixelY()

        if f(self.x) > self.y:
            pygame.draw.circle(window, [0, 0, 0], (int(px), int(py)), 10)
        else:
            pygame.draw.circle(window, [255, 255, 255], (int(px), int(py)), 10)


points = []

for i in range(0, 100):

    points.append(Point(uniform(-1,1), uniform(-1,1)))


inputs = [1.5 , 2]

pointindex = 0

nn = Perceptron(3)

run = True
while run:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.draw.rect(window, (200,200,200), (0,0, width, height))

    p1 = Point(-1, f(-1))
    p2 = Point(1, f(1))

    pygame.draw.line(window, [0,0,0], (p1.pixelX(),p1.pixelY()), (p2.pixelX(),p2.pixelY()), 5)

    p3 = Point(-1, nn.guessY(-1))
    p4 = Point(1, nn.guessY(1))

    pygame.draw.line(window, [255, 0, 0], (p3.pixelX(), p3.pixelY()), (p4.pixelX(), p4.pixelY()), 5)

    nn.train([points[pointindex].x, points[pointindex].y, points[pointindex].bias], points[pointindex].label)

    for i in range(0, len(points)):

        points[i].show()

        guess = nn.guess([points[i].x, points[i].y, points[i].bias])

        if guess == points[i].label:
            pygame.draw.circle(window, [0, 255, 0], (int(points[i].pixelX()), int(points[i].pixelY())), 5)
        else:
            pygame.draw.circle(window, [255, 0, 0], (int(points[i].pixelX()), int(points[i].pixelY())), 5)

    pygame.display.update()

    pointindex+=1

    if pointindex == len(points):
        pointindex = 0


pygame.quit()