from TensorTools import *
from cv2.cv2 import *
import keyboard

net = Network.load_network('network.pickle')
cam_port = 0
cam = VideoCapture(cam_port)
txt = ""
txt2 = ""
while True:

    # Capture the video frame
    # by frame
    ret, frame = cam.read()

    # font
    font = FONT_HERSHEY_SIMPLEX

    # fontScale
    fontScale = 0.5

    # Blue color in BGR
    color = (0, 0, 255)

    # Line thickness of 2 px
    thickness = 2

    frametxt = putText(frame, txt, (50, 50), font,
                        fontScale, color, thickness, LINE_AA)

    frametxt = putText(frametxt, txt2, (50, 100), font,
                        fontScale, color, thickness, LINE_AA)

    # Display the resulting frame
    imshow('frame', frametxt)

    if keyboard.is_pressed('space'):
        scale_percent = 15  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        frame = resize(frame, dim)

        if keyboard.is_pressed('space') :
            (B, G, R) = split(frame)
            inp_img = np.array([R, G, B])
            pred = net.forward_propagate(inp_img)
            txt = "Not Smiling: " + format((pred[1]*100),".2f") + "%"
            txt2 = "Smiling: " + format((pred[0]*100),".2f") + "%"
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cam.release()
# Destroy all the windows
destroyAllWindows()

