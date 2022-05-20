import numpy as np
import copy

def sigmoid(x):

    return 1 / (1 + np.exp(-x))

def dsigmoid(y):

    return y * (1 - y)

class NeuralNetwork:

    def __init__(self, numI, numH, numO):

        self.input_nodes = numI
        self.hidden_nodes = numH
        self.output_nodes = numO

        self.weights_ih = np.random.rand(self.input_nodes, self.hidden_nodes)
        self.weights_ih = self.weights_ih * 2 - 1
        self.weights_ho = np.random.rand(self.hidden_nodes, self.output_nodes)
        self.weights_ho = self.weights_ho * 2 - 1

        self.bias_h = np.random.rand(1, self.hidden_nodes)
        self.bias_h = self.bias_h * 2 - 1
        self.bias_o = np.random.rand(1, self.output_nodes)
        self.bias_o = self.bias_o * 2 - 1

        self.learning_rate = 0.1
    
    def copy(self):
        n = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        n.weights_ih = copy.deepcopy(self.weights_ih)
        n.weights_ho = copy.deepcopy(self.weights_ho)
        n.bias_h = copy.deepcopy(self.bias_h)
        n.bias_o = copy.deepcopy(self.bias_o)
        return n
    
    def mutate(self, rate):
        
        # mutate rate% of weights

        for weight_grp in [self.weights_ih, self.weights_ho, self.bias_h, self.bias_o]:
            for weight in weight_grp:
                if np.random.rand() < rate:
                    weight += np.random.rand() * 2 - 1

        # mutate entire weights

        # if np.random.rand() < rate:
        #     self.weights_ih += np.random.rand() * 2 - 1
            
        #     self.weights_ho += np.random.rand() * 2 - 1

        #     self.bias_h += np.random.rand() * 2 - 1
            
        #     self.bias_o += np.random.rand() * 2 - 1

    def crossover(self, other):
            
        n = NeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
    
        crossover_point = np.random.randint(0, self.weights_ih.shape[0])
        n.weights_ih = np.concatenate((copy.deepcopy(self.weights_ih)[:crossover_point], copy.deepcopy(other.weights_ih)[crossover_point:]))
        crossover_point2 = np.random.randint(0, self.weights_ho.shape[0])
        n.weights_ho = np.concatenate((copy.deepcopy(self.weights_ho[:crossover_point2]), copy.deepcopy(other.weights_ho[crossover_point2:])))
        crossover_point3 = np.random.randint(0, self.bias_h.shape[0])
        n.bias_h = np.concatenate((copy.deepcopy(self.bias_h[:crossover_point3]), copy.deepcopy(other.bias_h[crossover_point3:])))
        crossover_point4 = np.random.randint(0, self.bias_o.shape[0])
        n.bias_o = np.concatenate((copy.deepcopy(self.bias_o[:crossover_point4]), copy.deepcopy(other.bias_o[crossover_point4:])))

        return n

    def predict(self, inputs):

        hidden = np.dot(inputs, self.weights_ih)
        hidden = np.add(hidden, self.bias_h)
        hidden = sigmoid(hidden)

        output = np.dot(hidden, self.weights_ho)
        output = np.add(output, self.bias_o)
        output = sigmoid(output)

        return output