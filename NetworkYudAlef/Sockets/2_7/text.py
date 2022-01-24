from PIL import ImageGrab
import numpy as np
import cv2
import os
import time

start = time.time()
seconds = 5
frames = []
while int(time.time() - start) < seconds:
    start_take = time.time()
    printscreen_pil = ImageGrab.grab()
    printscreen_numpy = np.array(printscreen_pil, dtype='uint8')
    frames.append(printscreen_numpy[...,:3])

out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 19, (1920, 1080))
for i in range(len(frames)):
    out.write(frames[i])
out.release()

os.system('ffmpeg -i output.mp4 -vcodec h264 -crf 28 -an -filter:v fps=fps=19 output_c.mp4')
os.remove('output.mp4')