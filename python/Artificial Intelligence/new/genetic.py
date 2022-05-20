import random


class GeneticAlgorithm:

    def __init__(self, population_size, population_type, mutation_rate, fitness_function, crossover=True, elitists=3):
        self.population_size = population_size
        self.population_type = population_type
        self.mutation_rate = mutation_rate
        self.elitists = elitists
        self.cross_over = crossover
        self.population = []
        self.best_score = 0
        self.best_brain = None
        self.generation = 0
        self.create_population()

        self.fitness_function = fitness_function

    def indentical_population(self):
        pop = []
        for brain in self.population:
            pop.append(brain)
        return pop
        
    def create_brain(self):
        return self.population_type()

    def create_population(self):
        for i in range(self.population_size):
            self.population.append(self.create_brain())
        
    def clear_population(self):
        self.population = []
    
    def next_generation(self):

        self.fit_population(self.fitness_function)

        for brain in self.population:
            if brain.score > self.best_score:
                self.best_score = brain.score
                self.best_brain = brain.model

        self.generation += 1
        elites = self.select_elites()
        new_population = elites
        for i in range(self.population_size - self.elitists):
            if self.cross_over:
                parent1 = self.choose_probable_parent()
                parent2 = self.choose_probable_parent()
                child = parent1.crossover(parent2)
            else:
                child = self.choose_probable_parent().copy()
            child.mutate(self.mutation_rate)
            new_population.append(child)
        self.population = new_population

    def choose_probable_parent(self):
        ind = 0
        r = random.random()
        while r > 0:
            r -= self.population[ind].score
            ind += 1
        ind-=1

        return self.population[ind]
    
    def fit_population(self, fitness_function):
        fitness_function(self.population)
    
    def select_elites(self):
        elites = []
        elitist_sort = sorted(self.population, key=lambda x: x.score, reverse=True)
        for i in range(self.elitists):
            elites.append(elitist_sort[i])
        return elites
    
