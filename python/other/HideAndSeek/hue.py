from PIL import Image, ImageDraw
from sys import argv, exit
import numpy as np
import os.path

if len(argv) != 3:

    print("Usage: hue.py [Environment image path] [Hide and seek player path]")
    exit(1)

bg_path = argv[1]

if not os.path.isfile(bg_path):
    print("Background file not found")
    exit(1)

player_path = argv[2]

if not os.path.isfile(player_path):
    print("Player file not found")
    exit(1)

bg = Image.open(bg_path).convert(mode='HSV')
bwidth, bheight = bg.size

oplayer = Image.open(player_path)
player = oplayer.copy().convert(mode='HSV')
pwidth, pheight = player.size

player_color_avg = 0

for x in range(pwidth):

    for y in range(pheight):

        player_color_avg += player.getpixel((x, y))[0]

player_color_avg /= pwidth*pheight

best_avg_index = [0, 0]

best_avg_diff = 255

for x in range(int(bwidth / pwidth)):

    for y in range(int(bheight / pheight)):

        current_avg = 0

        for i in range(pwidth):

            for j in range(pheight):

                x_ = x*pwidth+i
                y_ = y*pheight+j

                current_avg += bg.getpixel((x_, y_))[0]

        current_avg /= pwidth*pheight

        current_avg_diff = abs(current_avg - player_color_avg)

        if current_avg_diff < best_avg_diff:

            best_avg_diff = current_avg_diff
            best_avg_index = [x*pwidth, y*pheight]

hidden = bg.convert('RGBA').copy()

hidden.paste(oplayer, (best_avg_index[0], best_avg_index[1]), oplayer)

hidden.save(os.path.dirname(__file__) + 'output.png')
hidden.show()