import numpy as np
import timeit
from tensorflow import keras
import random
import sys
from tqdm import tqdm
from matplotlib import pyplot as plt
from numba import jit, njit, cuda
from scipy import signal
import skimage.measure


def relu(x):
    return x * (x > 0)


def d_relu(x):
    return 1 * (x > 0)


def softmax(z):
    """Computes softmax function.
    z: array of input values.
    Returns an array of outputs with the same shape as z."""
    # For numerical stability: make the maximum of z's to be 0.
    exps = np.exp(z - np.max(z))
    return exps / np.sum(exps)


def d_softmax(z):
    """Computes the gradient of the softmax function.
    z: (T, 1) array of input values where the gradient is computed. T is the
       number of output classes.
    Returns D (T, T) the Jacobian matrix of softmax(z) at the given z. D[i, j]
    is DjSi - the partial derivative of Si w.r.t. input j.
    """
    # -SjSi can be computed using an outer product between Sz and itself. Then
    # we add back Si for the i=j cases by adding a diagonal matrix with the
    # values of Si on its diagonal.
    D = -np.outer(z, z) + np.diag(z.flatten())
    return D[0]


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return x * (1 - x)


def binary_cross_entropy_prime(y_pred, y_true):
    return ((1 - y_true) / (1 - y_pred) - y_true / y_pred) / np.size(y_true)


def squared_error_derivative(x, y):
    """
    x: predicted value
    y: actual value
    """
    return 2 * (x - y)

class Layer:

    def __init__(self):
        self.input = None
        self.activation_gradient = None

class Flatten:

    def __init__(self, inp_shape):
        self.inp_shape = inp_shape

    def propagate(self, inp):
        if inp.shape != self.inp_shape:
            raise Exception(f"Input shape {inp.shape} doesn't match shape {self.inp_shape}")

        return inp.flatten()

    def back_propagate(self, output_grad):
        return np.reshape(output_grad, self.inp_shape)


class Dense(Layer):
    """
    Layer with fully connected neurons
    """

    def __init__(self, amount, input_amount, activation, d_activation):
        super().__init__()
        self.activation = activation
        self.d_activation = d_activation
        self.weight_matrix = np.random.rand(amount, input_amount)
        self.weight_matrix = self.weight_matrix * 2 - 1
        self.bias_vector = np.random.rand(amount)
        self.bias_vector = self.bias_vector * 2 - 1

    def __str__(self):
        return str(self.weight_matrix) + "\n" + str(self.bias_vector)

    def propagate(self, inp):
        self.input = inp
        output = self.activation(self.weight_matrix.dot(inp) + self.bias_vector)
        self.activation_gradient = self.d_activation(output)
        return output



class Convolutional(Layer):
    """
    Layer with convolutional neurons
    """

    def __init__(self, kernel_amount, kernel_size, input_shape, activation, d_activation):
        self.input_amount, self.input_width, self.input_height = input_shape
        self.kernel_amount = kernel_amount
        self.kernel_size = kernel_size
        self.weight_matrix = np.random.rand(kernel_amount, self.input_amount, kernel_size, kernel_size)
        self.weight_matrix = self.weight_matrix * 2 - 1
        self.bias_vector = np.random.rand(kernel_amount, self.input_width - self.kernel_size + 1, self.input_height - self.kernel_size + 1)
        self.bias_vector = self.bias_vector * 2 - 1

        self.activation = activation
        self.d_activation = d_activation
    
    def __str__(self):
        return str(self.weight_matrix) + "\n" + str(self.bias_vector)
    
    def propagate(self, inp):
        if inp.shape != (self.input_amount, self.input_width, self.input_height):
            raise Exception(f"Got input shape {inp.shape}, expected {(self.input_amount, self.input_width, self.input_height)}")
        self.input = inp
        output = np.copy(self.bias_vector)

        # for i in range(self.kernel_amount):
        #     for j in range(inp.shape[1] - self.kernel_size + 1):
        #         for k in range(inp.shape[2] - self.kernel_size + 1):
        #             output += np.sum(inp[:, j:j+self.kernel_size, k:k+self.kernel_size] * self.weight_matrix[i])

        for i in range(self.kernel_amount):
            for j in range(inp.shape[0]):
                output[i] += signal.correlate2d(inp[j], self.weight_matrix[i, j], "valid")

        activated_output = self.activation(output)

        self.activation_gradient = self.d_activation(activated_output)

        return activated_output

class MaxPooling(Layer):

    def __init__(self, kernel_size):
        super().__init__()
        self.kernel_size = kernel_size

    def propagate(self, inp):

        self.input = inp

        output = np.zeros((inp.shape[0], inp.shape[1]//self.kernel_size, inp.shape[2]//self.kernel_size))

        # for i in range(inp.shape[0]):
        #     for j in range(inp.shape[1]//self.kernel_size):
        #         for k in range(inp.shape[2]//self.kernel_size):
        #             output[i, j, k] = np.max(inp[i, j:j+self.kernel_size, k:k+self.kernel_size].flatten())
        #
        # for i in range(len(inp)):
        #     output[i] = skimage.measure.block_reduce(inp[i], (self.kernel_size, self.kernel_size), np.max)

        for i in range(len(inp)):
            M, N = inp[i].shape
            K = 2
            L = 2

            MK = M // K
            NL = N // L

            output[i] = inp[i, :MK * K, :NL * L].reshape(MK, K, NL, L).max(axis=(1, 3))

        return output

    def back_propagate(self, inp):

        output = self.input

        for i in range(inp.shape[0]):
            for j in range(inp.shape[1]):
                for k in range(inp.shape[2]):

                    block = output[i, j:j+self.kernel_size, k:k+self.kernel_size]
                    block_max = np.max(block)

                    for m in range(block.shape[0]):
                        for n in range(block.shape[1]):
                            block[m, n] = 0 if block[m, n] != block_max else inp[i,j,k]

                    output[i, j:j+self.kernel_size, k:k+self.kernel_size] = block
        return output

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

    def stochastic_gradient_descent(self, inputs, targets, learning_rate, epochs=1, verbose=False,
                                    eval_function=lambda x, y: np.argmax(x) == np.argmax(y), xtest=None, ytest=None):
        """
        Back propagation with stochastic gradient descent.
        """

        if verbose:
            print("Training...")
            success_rate_cache = []
            success_rate_train_cache = []

        real_layers = self.get_real_layers()

        for epoch in range(epochs):
            inpoutpairs = list(zip(inputs, targets))
            np.random.shuffle(inpoutpairs)
            for inp, target in tqdm(inpoutpairs, desc=f"Epoch {epoch}", disable=not verbose):
                for layer in self.layers:
                    inp = layer.propagate(inp)

                L = len(real_layers) - 1  # layer index

                output_gradient = inp - target

                # backpropagate error recursively
                while L >= 0:

                    layer = real_layers[L]

                    if isinstance(layer, Flatten):# or isinstance(layer, MaxPooling):
                        output_gradient = layer.back_propagate(output_gradient)
                        L -= 1
                        continue
                    gB = layer.activation_gradient * output_gradient * learning_rate  # bias gradient calculation

                    if isinstance(layer, Dense):
                        gW = np.multiply(gB.reshape(-1, 1), layer.input)  # gradient of weight

                        output_gradient = layer.weight_matrix.T @ output_gradient
                    elif isinstance(layer, Convolutional):
                        # in this case gW is the kernel gradient
                        gW = np.zeros(layer.weight_matrix.shape)
                        inp_grad = np.zeros((layer.input_amount, layer.input_width, layer.input_height)) # (soon to be output gradient)
                        for i in range(layer.kernel_amount):
                            for j in range(layer.input_amount):
                                gW[i, j] = signal.correlate2d(layer.input[j], output_gradient[i], "valid")
                                inp_grad[j] = signal.convolve2d(output_gradient[i], layer.weight_matrix[i, j], "full")

                        output_gradient = inp_grad

                    # update weights and biases 
                    layer.weight_matrix -= gW  # adjust weights
                    layer.bias_vector -= gB  # adjust biases

                    L -= 1

            if epoch % 10 == 0:
                learning_rate /= 2

            if verbose:
                success_rate_train_cache.append(self.evaluate(inputs, targets, eval_function))
                success_rate_cache.append(self.evaluate(xtest, ytest, eval_function))

        if verbose:
            print(f"Success rate: {success_rate_cache[-1]}")
            print(f"Training success rate: {success_rate_train_cache[-1]}")
            plt.plot(success_rate_cache, label="Test")
            plt.plot(success_rate_train_cache, label="Train")
            plt.show()

    def evaluate(self, inputs, targets, eval_function, verbose=False):
        """
        Evaluate the network on the given inputs and targets.
        """

        if verbose:
            print("Evaluating...")
        total = 0
        correct = 0
        for inp, target in zip(inputs, targets):
            inp = self.forward_propagate(inp)
            if eval_function(inp, target):
                correct += 1
            total += 1
        return correct / total

    def get_real_layers(self):
        real = []
        for layer in self.layers:
            if isinstance(layer, Dense) or isinstance(layer, Convolutional) or isinstance(layer, Flatten): #or isinstance(layer, MaxPooling):
                real.append(layer)
        return real


def mnist_test():
    net = Network([
        Convolutional(5, 3, (1, 28, 28), sigmoid, d_sigmoid),
        Flatten((5,26,26)),
        Dense(128, 5*26*26, relu, d_relu),
        Dense(2, 128, softmax, d_softmax),
    ])

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train / 255
    x_test = x_test / 255
    x_train = x_train[:, np.newaxis, ...]
    x_test = x_test[:, np.newaxis, ...]

    zero_index = np.where(y_test == 0)[0][:10000]
    one_index = np.where(y_test == 1)[0][:10000]
    all_indices = np.hstack((zero_index, one_index))
    all_indices = np.random.permutation(all_indices)
    x_test, y_test = x_test[all_indices], y_test[all_indices]

    zero_index = np.where(y_train == 0)[0][:10000]
    one_index = np.where(y_train == 1)[0][:10000]
    all_indices = np.hstack((zero_index, one_index))
    all_indices = np.random.permutation(all_indices)
    x_train, y_train = x_train[all_indices], y_train[all_indices]

    y_train = keras.utils.to_categorical(y_train, 2)
    y_test = keras.utils.to_categorical(y_test, 2)
    net.stochastic_gradient_descent(x_train, y_train, 0.01, 10, verbose=True, eval_function=lambda x, y: np.argmax(x) == np.argmax(y), xtest=x_test, ytest=y_test)


mnist_test()
