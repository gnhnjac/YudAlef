import numpy as np

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
        self.weights_ho = np.random.rand(self.hidden_nodes, self.output_nodes)

        self.bias_h = np.random.rand(1, self.hidden_nodes)
        self.bias_o = np.random.rand(1, self.output_nodes)

        self.learning_rate = 0.1

    def predict(self, inputs):

        hidden = np.dot(inputs, self.weights_ih)
        hidden = np.add(hidden, self.bias_h)
        hidden = sigmoid(hidden)

        output = np.dot(hidden, self.weights_ho)
        output = np.add(output, self.bias_o)
        output = sigmoid(output)

        return output

    def train(self, inputs, targets):

        inputs = np.array(inputs)

        hidden = np.dot(inputs, self.weights_ih)
        hidden = np.add(hidden, self.bias_h)
        hidden = sigmoid(hidden)

        output = np.dot(hidden, self.weights_ho)
        output = np.add(output, self.bias_o)
        output = sigmoid(output)

        output_error = (targets - output)

        hidden_error = np.dot(output_error * dsigmoid(output), self.weights_ho.T)

        ho_gradients = output_error * dsigmoid(output)
        ho_gradients *= self.learning_rate

        ho_deltas = np.dot(hidden.T, ho_gradients)
        self.weights_ho += ho_deltas

        ih_gradients = hidden_error * dsigmoid(hidden)
        ih_gradients *= self.learning_rate

        ih_deltas = np.dot(inputs[np.newaxis].T, ih_gradients)
        self.weights_ih += ih_deltas

        self.bias_h += ih_gradients
        self.bias_o += ho_gradients