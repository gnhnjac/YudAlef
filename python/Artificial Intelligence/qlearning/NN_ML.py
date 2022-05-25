import numpy as np
import copy

def sigmoid(x):

    return 1 / (1 + np.exp(-x))

def dsigmoid(y):

    return y * (1 - y)

class NeuralNetwork:

    def __init__(self, numI, hiddens, numO, network=None, hbiases=None, weights_ho=None, bias_o=None):

        self.input_nodes = numI
        self.hiddens = hiddens
        self.output_nodes = numO

        if network is None:
            self.network = []
            self.network.append(np.random.rand(self.input_nodes, hiddens[0]))
            self.network[0] = self.network[0] * 2 - 1
            
            for i in range(1, len(hiddens)):
                self.network.append(np.random.rand(hiddens[i-1], hiddens[i]))
                self.network[i] = self.network[i] * 2 - 1
            
            self.hbiases = []

            for i in range(len(hiddens)):
                self.hbiases.append(np.random.rand(1, hiddens[i]))
                self.hbiases[i] = self.hbiases[i] * 2 - 1

            self.weights_ho = np.random.rand(hiddens[-1], self.output_nodes)
            self.weights_ho = self.weights_ho * 2 - 1
            self.bias_o = np.random.rand(1, self.output_nodes)
            self.bias_o = self.bias_o * 2 - 1
        else:
            self.network = copy.deepcopy(network)
            self.hbiases = copy.deepcopy(hbiases)
            self.weights_ho = copy.deepcopy(weights_ho)
            self.bias_o = copy.deepcopy(bias_o)
        self.mutation_rate = 1

    
    def copy(self):
        return NeuralNetwork(self.input_nodes, self.hiddens, self.output_nodes, self.network, self.hbiases, self.weights_ho, self.bias_o)
    
    def mutate(self, rate):
        
        for grp in [self.network, self.hbiases]:
            for weight_grp in grp:
                for weight in weight_grp:
                    if np.random.random() < rate:
                        weight += np.random.normal() * self.mutation_rate
        
        for weight_grp in [self.weights_ho, self.bias_o]:
            for weight in weight_grp:
                if np.random.random() < rate:
                    weight += np.random.normal() * self.mutation_rate

    def crossover(self, other):
            
        n = NeuralNetwork(self.input_nodes, self.hiddens, self.output_nodes)

        for i in range(len(self.network)):
            for j in range(len(self.network[i])):
                for k in range(len(self.network[i][j])):
                    if np.random.rand() < 0.5:
                        n.network[i][j][k] = copy.deepcopy(self.network[i][j][k])
                    else:
                        n.network[i][j][k] = copy.deepcopy(other.network[i][j][k])

        for i in range(len(self.hbiases)):
            for j in range(len(self.hbiases[i])):
                if np.random.rand() < 0.5:
                    n.hbiases[i][j] = copy.deepcopy(self.hbiases[i][j])
                else:
                    n.hbiases[i][j] = copy.deepcopy(other.hbiases[i][j])

        if np.random.rand() < 0.5:
            n.weights_ho = copy.deepcopy(self.weights_ho)
            n.bias_o = copy.deepcopy(self.bias_o)
        else:
            n.weights_ho = copy.deepcopy(other.weights_ho)
            n.bias_o = copy.deepcopy(other.bias_o)
        return n

    def predict(self, inputs):
        
        layer = inputs

        for i in range(len(self.network)):
            layer = np.dot(layer, self.network[i])
            layer = np.add(layer, self.hbiases[i])
            layer = sigmoid(layer)

        output = np.dot(layer, self.weights_ho)
        output = np.add(output, self.bias_o)
        output = sigmoid(output)

        return output