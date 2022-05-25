from genetic import *
from NN import *
import random
from copy import deepcopy
from tensorflow import keras
import numpy as np
import time
import os

mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255.0

def remap( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

class Guesser:

    def __init__(self, model=None):
        if model is not None:
            self.model = copy.deepcopy(model)
        else:
            self.model = NeuralNetwork(784, 32, 10)
        
        self.score = 0

    def predict(self, inputs):
        return self.model.predict(inputs)
    
    def mutate(self, rate):
        self.model.mutate(rate)

    def crossover(self, other):
        return Guesser(self.model.crossover(other.model))

    def copy(self):
        return Guesser(self.model)

def fit(guessers):

    s = 0

    for guesser in guessers:
        guesser.score = guesser.score**2

    for guesser in guessers:
        s += guesser.score

    for guesser in guessers:
        guesser.score /= s

ga = GeneticAlgorithm(500, Guesser, 0.1, fit, True, 20)

guessers = ga.indentical_population()

best_gueser = None
best_score = 0
while True:
    # print("Generation: " + str(ga.generation))
    
    for guesser, i in zip(guessers, range(len(guessers))):
        os.system('cls')
        print(f"Generation: {ga.generation}, Best score: {best_score*100/len(x_train)}%, % done: {i*100/len(guessers)}%")
        nostreak = 0
        for image, answer in zip(x_train, y_train):
            guess = np.argmax(guesser.predict(image.reshape(1,784)))
            if guess == answer:
                nostreak = 0
            nostreak += guess != answer
            if nostreak > int(remap(best_score, 0, len(x_train), 50, 5)):
                break
            guesser.score += guess == answer
        if guesser.score > best_score:
            best_score = guesser.score
            best_gueser = guesser
            # print("New best score: " + str(best_score) + " numbers correct out of " + str(len(x_train)) + ", " + str(best_score * 100 / len(x_train)) + "%")

    ga.next_generation()

    guessers = ga.indentical_population()

    time.sleep(5)