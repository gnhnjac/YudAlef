import numpy as np
from tensorflow import keras
from tqdm import tqdm
from matplotlib import pyplot as plt
from scipy import signal
from numba import njit
import pickle
from cv2 import cv2


@njit(cache=True, fastmath=True)
def relu(x):
    return x * (x > 0)


@njit(cache=True, fastmath=True)
def d_relu(x):
    return 1 * (x > 0)


@njit(cache=True, fastmath=True)
def softmax(z):
    """Computes softmax function.
    z: array of input values.
    Returns an array of outputs with the same shape as z."""
    # For numerical stability: make the maximum of z's to be 0.
    exps = np.exp(z - np.max(z))
    return exps / np.sum(exps)


@njit(cache=True, fastmath=True)
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


@njit(cache=True, fastmath=True)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


@njit(cache=True, fastmath=True)
def d_sigmoid(x):
    return x * (1 - x)


@njit(cache=True, fastmath=True)
def mse(y_pred, y_true):
    return np.mean(np.power(y_true - y_pred, 2))


@njit(cache=True, fastmath=True)
def mse_prime(y_pred, y_true):
    return 2 * (y_pred - y_true) / len(y_true)  # np.size(y_true)


@njit(cache=True, fastmath=True)
def binary_cross_entropy_prime(y_pred, y_true):
    return ((1 - y_true) / (1 - y_pred) - y_true / y_pred) / len(y_true)  # np.size(y_true)


@njit(cache=True, fastmath=True)
def binary_cross_entropy(y_pred, y_true):
    return np.mean(-y_true * np.log(y_pred) - (1 - y_true) * np.log(1 - y_pred))


class Layer:

    def __init__(self):
        self.input = None
        self.activation_gradient = None

    def propagate(self, inp):
        pass

    def back_propagate(self, output_grad, lr):
        pass


class Activation(Layer):

    def __init__(self, activation, d_activation):
        super().__init__()
        self.activation = activation
        self.d_activation = d_activation

    def propagate(self, inp):
        out = self.activation(inp)
        self.activation_gradient = self.d_activation(out)
        return out

    def back_propagate(self, output_gradient, learning_rate):
        return self.activation_gradient * output_gradient

    def __str__(self):
        return f"Activation\n=============\nType: {type(self)}"


class Sigmoid(Activation):

    def __init__(self):
        super().__init__(sigmoid, d_sigmoid)


class Softmax(Activation):

    def __init__(self):
        super().__init__(softmax, d_softmax)


class Relu(Activation):

    def __init__(self):
        super().__init__(relu, d_relu)


class Flatten:

    def __init__(self, inp_shape):
        self.inp_shape = inp_shape

    def propagate(self, inp):
        if inp.shape != self.inp_shape:
            raise Exception(f"Input shape {inp.shape} doesn't match shape {self.inp_shape}")

        return inp.flatten()

    def back_propagate(self, output_grad, lr):
        return np.reshape(output_grad, self.inp_shape)

    def __str__(self):
        return f"Flatten\n=============\nShape: {self.inp_shape}"


class Dense(Layer):
    """
    Layer with fully connected neurons
    """

    def __init__(self, amount, input_amount):
        super().__init__()
        self.weight_matrix = np.random.rand(amount, input_amount)
        self.weight_matrix = self.weight_matrix * 2 - 1
        self.bias_vector = np.random.rand(amount)
        self.bias_vector = self.bias_vector * 2 - 1

    def propagate(self, inp):
        self.input = inp
        return self.weight_matrix.dot(inp) + self.bias_vector

    def back_propagate(self, output_grad, lr):
        weight_deltas = np.multiply(output_grad.reshape(-1, 1), self.input)  # gradient of weight

        self.bias_vector -= output_grad * lr

        output_grad = self.weight_matrix.T @ output_grad

        self.weight_matrix -= weight_deltas * lr

        return output_grad

    def __str__(self):
        return f"Dense\n=============\nParameters: {len(self.weight_matrix.flatten()) + len(self.bias_vector)}"


class Convolutional(Layer):
    """
    Layer with convolutional neurons
    """

    def __init__(self, kernel_amount, kernel_size, input_shape, pad=False):
        super().__init__()
        self.input_amount, self.input_width, self.input_height = input_shape

        self.pad = pad

        if pad:
            self.input_width += 2
            self.input_height += 2

        self.kernel_amount = kernel_amount
        self.kernel_size = kernel_size
        self.weight_matrix = np.random.rand(kernel_amount, self.input_amount, kernel_size, kernel_size)
        self.weight_matrix = self.weight_matrix * 2 - 1
        self.bias_vector = np.random.rand(kernel_amount, self.input_width - self.kernel_size + 1,
                                          self.input_height - self.kernel_size + 1)
        self.bias_vector = self.bias_vector * 2 - 1

    def propagate(self, inp):
        if self.pad:
            inp = np.pad(inp, pad_width=((0, 0), (1, 1), (1, 1)), mode='constant')
        if inp.shape != (self.input_amount, self.input_width, self.input_height):
            raise Exception(
                f"Got input shape {inp.shape}, expected {(self.input_amount, self.input_width, self.input_height)}")

        self.input = inp
        output = np.copy(self.bias_vector)

        # for i in range(self.kernel_amount):
        #     for j in range(inp.shape[1] - self.kernel_size + 1):
        #         for k in range(inp.shape[2] - self.kernel_size + 1):
        #             output += np.sum(inp[:, j:j+self.kernel_size, k:k+self.kernel_size] * self.weight_matrix[i])

        for i in range(self.kernel_amount):
            for j in range(inp.shape[0]):
                output[i] += signal.correlate2d(inp[j], self.weight_matrix[i, j], "valid")

        return output

    def back_propagate(self, output_grad, lr):
        # in this case gW is the kernel gradient
        kernel_deltas = np.zeros(self.weight_matrix.shape)
        inp_grad = np.zeros(self.input.shape)  # (soon to be output gradient)
        for i in range(self.kernel_amount):
            for j in range(self.input_amount):
                kernel_deltas[i, j] = signal.correlate2d(self.input[j], output_grad[i], "valid")
                inp_grad[j] = signal.convolve2d(output_grad[i], self.weight_matrix[i, j], "full")

        # update weights and biases
        self.weight_matrix -= kernel_deltas * lr  # adjust kernel weights
        self.bias_vector -= output_grad * lr  # adjust biases

        return inp_grad

    def __str__(self):
        return f"Convolutional\n=============\nParameters: {len(self.weight_matrix.flatten()) + len(self.bias_vector)}"


class MaxPooling(Layer):

    def __init__(self):
        super().__init__()

    def propagate(self, inp):

        self.input = inp

        output = np.zeros((inp.shape[0], inp.shape[1] // 2, inp.shape[2] // 2))

        for i in range(len(inp)):
            M, N = inp[i].shape
            K = 2
            L = 2

            MK = M // K
            NL = N // L

            output[i] = inp[i, :MK * K, :NL * L].reshape(MK, K, NL, L).max(axis=(1, 3))

        return output

    @staticmethod
    @njit(fastmath=True, cache=True)
    def solve_window(inp, out_grad, new_grad, stride, kernel_size):
        for i in range(new_grad.shape[0]):
            for j in range(new_grad.shape[1] // stride):
                for k in range(new_grad.shape[2] // stride):
                    x = j * stride
                    y = k * stride
                    window = inp[i, x:x + kernel_size, y:y + kernel_size]
                    mask = window == np.max(window)
                    new_grad[i, x:x + kernel_size, y:y + kernel_size] += np.multiply(mask, out_grad[i, j, k])

    def back_propagate(self, output_grad, lr):

        new_grad = np.zeros(self.input.shape)

        # do it with jit for much faster processing
        self.solve_window(self.input, output_grad, new_grad, 2, 2)

        return new_grad

    def __str__(self):
        return "Maxpooling\n============="


class Dropout:

    def __init__(self, precent):
        self.percent = precent

    def propagate(self, inp):
        mask = np.random.rand(inp.shape[0]) > self.percent

        return np.multiply(inp, mask) / (1 - self.percent)

    def back_propagate(self, output_grad, lr):
        return output_grad

    def __str__(self):
        return f"Dropout\n=============\nPercent: {self.percent}"


class Network:

    def __init__(self, layers):

        self.layers = layers

    def forward_propagate(self, data):

        for layer in self.layers:
            if isinstance(layer, Dropout):
                continue
            data = layer.propagate(data)

        return data

    def stochastic_gradient_descent(self, inputs, targets, learning_rate, loss_function, loss_function_derivative,
                                    epochs=1, graph=False, verbose=False,
                                    eval_function=lambda x, y: np.argmax(x) == np.argmax(y), xtest=None, ytest=None):
        """
        Back propagation with stochastic gradient descent.
        """

        if graph:
            success_rate_cache = []
            success_rate_train_cache = []
            error_cache = []

        for epoch in range(epochs):
            inpoutpairs = list(zip(inputs, targets))
            np.random.shuffle(inpoutpairs)
            error = 0
            for inp, target in tqdm(inpoutpairs, desc=f"Epoch {epoch + 1}/{epochs}", disable=not verbose):
                for layer in self.layers:
                    inp = layer.propagate(inp)

                if graph:
                    error += loss_function(inp, target)

                output_gradient = loss_function_derivative(inp, target)  # inp - target

                # backpropagate error recursively
                for layer in reversed(self.layers):
                    output_gradient = layer.back_propagate(output_gradient, learning_rate)

            # if epoch % 10 == 0:
            #     learning_rate /= 2

            if verbose or graph:

                train_eval = self.evaluate(inputs, targets, eval_function)
                test_eval = None
                if xtest is not None and ytest is not None:
                    test_eval = self.evaluate(xtest, ytest, eval_function)

                if graph:

                    error_cache.append(error / len(inpoutpairs))
                    success_rate_train_cache.append(train_eval)
                    if test_eval:
                        success_rate_cache.append(test_eval)
                if verbose:
                    print(f"Training success rate: {format(train_eval, '.3f')}")
                    if test_eval:
                        print(f"Success rate: {format(test_eval, '.3f')}")

        if graph:
            if xtest is not None and ytest is not None:
                plt.plot(success_rate_cache, label="Testing success")
            plt.plot(success_rate_train_cache, label="Training success")
            plt.title("Success rate")
            plt.legend()
            plt.show()
            plt.plot(error_cache)
            plt.title("Loss")
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

    def save_network(self):
        with open('network.pickle', 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_network(file):
        with open(file, 'rb') as f:
            b = pickle.load(f)
        return b

    def __str__(self):
        txt = ""

        for layer in self.layers:
            txt += str(layer) + "\n=============\n\n"

        total_params = 0

        for layer in self.layers:
            if isinstance(layer, Convolutional) or isinstance(layer, Dense):
                total_params += len(layer.weight_matrix.flatten()) + len(layer.bias_vector)

        txt += f"\nTotal Parameters: {total_params}"

        return txt

    def visualize_convolution(self, img):

        for layer in self.layers:
            if isinstance(layer, Dropout):
                continue
            if isinstance(layer, Convolutional):
                cv2.imshow("Before convolution", self.get_conv_image(img))
            img = layer.propagate(img)
            if isinstance(layer, Convolutional):
                cv2.imshow("After convolution", self.get_conv_image(img))
                cv2.waitKey()

    @staticmethod
    def get_conv_image(img_block):
        w = img_block.shape[1]
        h = img_block.shape[2]
        img_full = np.zeros((1920, 1080))
        k = 0
        for i in range(1920 // w):
            for j in range(1080 // h):
                x = i * w
                y = j * h
                img_full[x:x + w, y:y + h] = img_block[k]
                k += 1
                if k == len(img_block):
                    break
            if k == len(img_block):
                break

        img_full = img_full[~np.all(img_full == 0, axis=1)]
        img_full = img_full[:, ~np.all(img_full == 0, axis=0)]
        img_full /= np.max(img_full)

        return img_full


def __mnist_test():
    net = Network([
        Convolutional(10, 3, (1, 28, 28), pad=True),
        Relu(),
        MaxPooling(),
        Convolutional(10, 3, (10, 14, 14), pad=True),
        Relu(),
        MaxPooling(),
        Flatten((10, 7, 7)),
        Dense(128, 10 * 7 * 7),
        Sigmoid(),
        Dense(10, 128),
        Sigmoid()
    ])
    print(net)
    #
    # net = Network([
    #     Flatten((28, 28)),
    #     Dense(128, 28 * 28),
    #     Sigmoid(),
    #     Dense(10, 128),
    #     Sigmoid()
    # ])

    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    x_train = x_train / 255
    x_test = x_test / 255
    x_train = x_train[:, np.newaxis, ...]
    x_test = x_test[:, np.newaxis, ...]
    x_train = x_train[:5000]
    x_test = x_test[:5000]
    y_train = y_train[:5000]
    y_test = y_test[:5000]

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)
    net.stochastic_gradient_descent(x_train, y_train, 0.01, binary_cross_entropy, binary_cross_entropy_prime, 20,
                                    graph=True, verbose=True,
                                    eval_function=lambda x, y: np.argmax(x) == np.argmax(y), xtest=x_test, ytest=y_test)
    net.visualize_convolution(x_test[0])


if __name__ == "__main__":
    __mnist_test()
