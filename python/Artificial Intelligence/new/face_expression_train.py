import cv2.cv2

from TensorTools import *
from os import listdir
import pathlib
from cv2 import cv2


# net = Network([
#     Convolutional(20, 3, (3, 72, 96), pad=True),
#     Sigmoid(),
#     MaxPooling(),
#     Convolutional(10, 3, (20, 36, 48), pad=True),
#     Sigmoid(),
#     MaxPooling(),
#     Flatten((10, 18, 24)),
#     Dense(128, 10 * 18 * 24),
#     Sigmoid(),
#     #Dropout(0.2),
#     Dense(2, 128),
#     Sigmoid(),
# ])
net = Network.load_network('network.pickle')
print(net)
x_train = np.zeros((1000, 3, 72, 96))
y_train = np.zeros((1000, 2))

x_test = np.zeros((1000, 3, 72, 96))
y_test = np.zeros((1000, 2))

folder_dir = str(pathlib.Path(__file__).parent.resolve()) + f'\\smiling\\'
for image, index in zip(listdir(folder_dir), range(500)):
    img = cv2.imread(folder_dir + image, cv2.IMREAD_COLOR)
    (B, G, R) = cv2.split(img)

    x_train[index] = np.array([R, G, B])
    y_train[index] = [1, 0]

folder_dir = str(pathlib.Path(__file__).parent.resolve()) + f'\\not_smiling\\'
for image, index in zip(listdir(folder_dir), range(500)):
    img = cv2.imread(folder_dir + image, cv2.IMREAD_COLOR)
    (B, G, R) = cv2.split(img)

    x_train[500+index] = np.array([R, G, B])
    y_train[500+index] = [0, 1]


folder_dir = str(pathlib.Path(__file__).parent.resolve()) + f'\\smiling_test\\'
for image, index in zip(listdir(folder_dir), range(500)):
    img = cv2.imread(folder_dir + image, cv2.IMREAD_COLOR)
    (B, G, R) = cv2.split(img)

    x_test[index] = np.array([R,G,B])
    y_test[index] = [1, 0]

folder_dir = str(pathlib.Path(__file__).parent.resolve()) + f'\\not_smiling_test\\'
for image, index in zip(listdir(folder_dir), range(500)):
    img = cv2.imread(folder_dir + image, cv2.IMREAD_COLOR)
    (B, G, R) = cv2.split(img)

    x_test[500+index] = np.array([R, G, B])
    y_test[500+index] = [0, 1]

x_train /= 255
x_test /= 255

net.stochastic_gradient_descent(x_train, y_train, 0.01, binary_cross_entropy, binary_cross_entropy_prime, 1, graph=True, verbose=True, eval_function=lambda x, y: np.argmax(x) == np.argmax(y), xtest=x_test, ytest=y_test)

net.save_network()

