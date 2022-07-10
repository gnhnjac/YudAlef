from grpc import alts_channel_credentials
import numpy as np
import timeit
from tensorflow import keras
import random
import sys

def relu(x):
    return x * (x > 0)

def d_relu(x):
    return 1 * (x > 0)

def softmax(x):
    ex = np.exp(x - np.max(x))
    if np.isnan(ex).any():
        d = net.get_dense_layers()
        for subnet in d:
            if isinstance(subnet, Dense):
                print(subnet.weight_matrix)
        sys.quit()
    return ex/np.sum(ex)

def d_softmax(z):
    Sz = softmax(z)
    D = -np.outer(Sz, Sz) + np.diag(Sz.flatten())
    return D

    # deprecated
    # s = softmax(z)
    # jacobian = np.diag(s)
    # for i in range(jacobian.shape[0]):
    #     for j in range(jacobian.shape[1]):
    #         if j == i:
    #             jacobian[i, j] = s[i] * (1 - s[i])
    #         else:
    #             jacobian[i, j] = -s[i] * s[j]
    # return jacobian

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))

def mse(inp, target):
    return (inp - target)**2

def d_mse(inp, target):
    return 2 * (inp - target) / inp.shape[0]

def categorical_cross_entropy(A, Y):
    return -(1.0/A.shape[1]) * np.sum(np.dot(np.log(A), Y.T) + np.dot(np.log(1-A), (1-Y).T))

class Flatten:

    def __init__(self, shape):

        self.shape = shape

    def propagate(self, inp):
        
        if inp.shape != self.shape:
            raise Exception(f"Input shape {inp.shape} doesn't match shape {self.shape}")

        return inp.flatten()

class Dense:
    """
    Layer with fully connected neurons
    """

    def __init__(self, amount, input_amount, activation, d_activation):
        
        self.activation = activation
        self.d_activation = d_activation
        self.weight_matrix = np.random.rand(amount, input_amount)
        self.weight_matrix = self.weight_matrix*2 - 1
        self.bias_vector = np.random.rand(amount)
        self.bias_vector = self.bias_vector*2 - 1

    def __str__(self):

        return str(self.weight_matrix)

    def propagate(self, inp):

        return self.activation(self.weight_matrix.dot(inp) + self.bias_vector)
    
    def no_activation_propagate(self, inp):

        return self.weight_matrix.dot(inp) + self.bias_vector

class Dropout:

    def __init__(self, precent):
        self.precent = precent

    def propagate(self, inp):
        
        mask = np.random.rand(inp.shape[0])
        mask = mask > self.precent

        return np.multiply(inp, mask)

class Network:

    def __init__(self, layers):

        self.layers = layers

    def forward_propagate(self, data):

        for layer in self.layers:
            if isinstance(layer, Dropout):
                continue
            data = layer.propagate(data)
        
        return data
    
    def back_propagate_stoch(self, inputs, targets, loss_function, learning_rate):
        """
        Back propagation with stochastic gradient descent
        """

        for inp, target in np.array(list(zip(inputs, targets))):
            
            inp_cache = []
            zL_cache = []
            for layer in self.layers:
                if isinstance(layer, Dense):
                    inp_cache.append(inp)
                    inp = layer.no_activation_propagate(inp)
                    zL_cache.append(inp) # zL
                    inp = layer.activation(inp)
                else:
                    inp = layer.propagate(inp)


            L = len(zL_cache) - 1 # layer index
            E = loss_function(inp, target) # layer error
            gB = zL_cache[L] * E * learning_rate # gradient of bias
            gW = gB.reshape((-1, 1)) * inp_cache[L] # gradient of weight

            dense = self.get_dense_layers()

            # update weights and biases
            dense[L].weight_matrix +=  gW # adjust weights
            dense[L].bias_vector += gB # adjust biases

            L -= 1

            # backpropagate error recursively
            while L >= 0:
                # error needs to be -
                E = np.matmul(dense[L+1].weight_matrix.T, E)# error of next layer 

                # other option: zL_cache[L] * E.T
                gB = zL_cache[L] * E * learning_rate # gradient of bias
                gW = gB.reshape((-1, 1)) * inp_cache[L] # gradient of weight
                # update weights and biases 
                dense[L].weight_matrix +=  gW # adjust weights
                dense[L].bias_vector += gB # adjust biases

                L -= 1

    def get_dense_layers(self):
        dense = []
        for layer in self.layers:
            if isinstance(layer, Dense):
                dense.append(layer)
        return dense        




net = Network([
    Flatten((28,28)),
    Dense(16, 28*28, relu, d_relu),
    Dropout(0.4),
    Dense(10, 16, softmax, d_softmax),
])


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = x_train/255
x_test = x_test/255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

net.back_propagate_stoch(x_train, y_train, mse, 0.01)
total = 0
right = 0
for sample, label in zip(x_test, y_test):
    prediction = np.argmax(net.forward_propagate(sample))
    if prediction == np.argmax(label):
        right += 1
    total += 1
print(right/total)

# xxor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# yxor = np.array([[0], [1], [1], [0]])

# x = []
# y = []

# for i in range(10000):

#     randind = np.random.randint(0, 4)
#     x.append(xxor[randind])
#     y.append(yxor[randind])

# x = np.array(x)
# y = np.array(y)

# net.back_propagate_stoch(x, y, mse, d_mse, 0.1)

# print(net.forward_propagate(np.array([0, 0])))
# print(net.forward_propagate(np.array([0, 1])))
# print(net.forward_propagate(np.array([1, 0])))
# print(net.forward_propagate(np.array([1, 1])))

    