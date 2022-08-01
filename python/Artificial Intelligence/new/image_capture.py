from cv2.cv2 import *
import keyboard
import time
import pathlib

# program to capture single image from webcam in python

# importing OpenCV library

# initialize the camera
# If you have multiple camera connected with
# current device, assign a value in cam_port
# variable according to that
cam_port = 0
cam = VideoCapture(cam_port)

num = 0

while True:

    # Capture the video frame
    # by frame
    ret, frame = cam.read()

    # Display the resulting frame
    imshow('frame', frame)

    if keyboard.is_pressed('space'):
        scale_percent = 15  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        frame = resize(frame, dim)
        imwrite(str(pathlib.Path(__file__).parent.resolve()) + f'\\smiling_test\\img_{num}.jpg', frame)
        num += 1
        print(num)
        time.sleep(0.01)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cam.release()
# Destroy all the windows
destroyAllWindows()
