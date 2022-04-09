import tensorflow as tf
from emnist import extract_training_samples, extract_test_samples
from PIL import Image
import pygame
import numpy as np
from threading import Thread
import cv2

CV_2_THRESHHOLD_MIN = 170#127

x_train, y_train = extract_training_samples('digits')
x_test, y_test = extract_test_samples('digits')

# # thin out image lines with opencv
# for i in range(len(x_train)):
#     x_train[i] = cv2.threshold(x_train[i], CV_2_THRESHHOLD_MIN, 255, cv2.THRESH_BINARY)[1]

# for i in range(len(x_test)):
#     x_test[i] = cv2.threshold(x_test[i], CV_2_THRESHHOLD_MIN, 255, cv2.THRESH_BINARY)[1]

x_train, x_test = x_train / 255.0, x_test / 255.0 # convert color range from 0-255 to 0-1 (normalization)
# save all x_train and y_train to a folder called "mnist"

# for i in range(5):
#     img = x_train[i] * 255.0
#     img = Image.fromarray(img).convert('L')
#     img.save("mnist/{}.png".format(y_train[i]))

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=9, verbose=2, validation_data=(x_test, y_test))

# use pygame to make the user draw a digit and save it to a file then load it and predict what digit it is

pygame.init()

display = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Draw a digit')

font = pygame.font.SysFont('Arial', 30)

clock = pygame.time.Clock()
counter = 0

run = True

def predict():
    global display, counter
    # make our model predict the digit
    #img = pygame.image.tostring(display, 'RGB')
    # img = Image.frombytes('RGB', (400, 400), img)
    # img = img.resize((28, 28))
    # img = img.convert('L')
    # img = np.array(img) / 255.0
    # img = img.reshape((1, 28, 28))

    # thin down image lines with opencv
    src = np.array(pygame.surfarray.array3d(pygame.Surface.subsurface(display, (0, 0, 400, 400))))
    img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, CV_2_THRESHHOLD_MIN, 255, cv2.THRESH_BINARY)[1]
    img = cv2.resize(img, (28, 28))

    resized_back = cv2.resize(img, (400, 400))
    resized_back = cv2.cvtColor(resized_back, cv2.COLOR_GRAY2BGR)
    pygame_img = pygame.surfarray.make_surface(resized_back)
    display.blit(pygame_img, (400, 0))

    # rotate right and flip
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)

    img = img.reshape((1, 28, 28))


    prediction = model.predict(img)
    prediction = np.argmax(prediction)
    
    # display the prediction
    text = font.render("Prediction: " + str(prediction), True, (255, 255, 255))
    display.blit(text, (400, 0))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            pygame.draw.rect(display, (0, 0, 0), (0, 0, 400, 400))

    mouse_keys = pygame.mouse.get_pressed()

    if mouse_keys[0]:
        pos = pygame.mouse.get_pos()
        if pos[0] < 400-10 and pos[1] < 400-10:
            pygame.draw.circle(display, (255, 255, 255), pos, 10)

    pygame.display.update()
    counter += 1
    if counter % 5000 == 0:
        t = Thread(target=predict, daemon=True, args=())
        t.start()

pygame.quit()