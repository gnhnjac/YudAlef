import random

class Individual:

    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def __str__(self):
        return str(self.genes)

    def __repr__(self):
        return str(self.genes)

    def predict(self, inputs):
        return self.genes.predict(inputs)
    
    def crossover(self, other):
        return self.genes.crossover(other.genes)

    def mutate(self, rate):
        self.genes.mutate(rate)

    def copy(self):
        return self.genes.copy()

class GeneticAlgorithm:

    def __init__(self, population_size, population_type, mutation_rate, fitness_function, crossover=True, elitists=3):
        self.population_size = population_size
        self.population_type = population_type
        self.mutation_rate = mutation_rate
        self.elitists = elitists
        self.cross_over = crossover
        self.population = []
        self.best_fitness = 0
        self.best_brain = None
        self.generation = 0
        self.create_population()

        self.fitness_function = fitness_function

        self.best_of_generation = []

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

        self.fitness_modifier()
        self.normalize_fitness()

        local_best_fitness = 0
        local_best_brain = None
        for brain in self.population:
            if brain.fitness > self.best_fitness:
                self.best_fitness = brain.fitness
                self.best_brain = brain
            if brain.fitness > local_best_fitness:
                local_best_fitness = brain.fitness
                local_best_brain = brain
        
        self.best_of_generation.append(local_best_brain)

        self.generation += 1
        elites = self.select_elites()
        new_population = elites
        for i in range(self.population_size - self.elitists):
            if self.cross_over:
                # make it so parents can't be the same
                parent1 = self.choose_probable_parent()
                parent2 = self.choose_probable_parent()
                child = parent1.crossover(parent2)
            else:
                child = self.choose_probable_parent().copy()
            child = self.population_type(child)
            child.mutate(self.mutation_rate)
            new_population.append(child)
        self.population = new_population

    def choose_probable_parent(self):
        ind = 0
        r = random.random()
        while r > 0:
            r -= self.population[ind].fitness
            ind += 1
        ind-=1
        return self.population[ind]
    
    def fitness_modifier(self):
        self.fitness_function(self.population)
    
    def select_elites(self):
        elites = []
        elitist_sort = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        for i in range(self.elitists):
            elites.append(self.population_type(elitist_sort[i].copy()))
        return elites
    
    def normalize_fitness(self):
        total = 0
        for brain in self.population:
            total += brain.fitness
        for brain in self.population:
            brain.fitness /= total

    def get_best_brain(self, gen):
        return self.best_of_generation[gen]