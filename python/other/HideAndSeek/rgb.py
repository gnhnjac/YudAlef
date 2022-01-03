from PIL import Image, ImageDraw
from sys import argv, exit
import numpy as np
import os.path

if len(argv) != 3:

    print("Usage: rgb.py [Environment image path] [Hide and seek player path]")
    exit(1)

bg_path = argv[1]

if not os.path.isfile(bg_path):
    print("Background file not found")
    exit(1)

player_path = argv[2]

if not os.path.isfile(player_path):
    print("Player file not found")
    exit(1)

# rgb.py trees.jpg reptile.png

bg = Image.open(bg_path)
bwidth, bheight = bg.size

player = Image.open(player_path)
pwidth, pheight = player.size

player_color_avg_rgb = [0, 0, 0]

for x in range(pwidth):

    for y in range(pheight):

        player_color_avg_rgb[0] += player.getpixel((x, y))[0]
        player_color_avg_rgb[1] += player.getpixel((x, y))[1]
        player_color_avg_rgb[2] += player.getpixel((x, y))[2]

player_color_avg_rgb[0] /= pwidth*pheight
player_color_avg_rgb[1] /= pwidth*pheight
player_color_avg_rgb[2] /= pwidth*pheight

best_avg_index = [0, 0]

best_avg_rgb_difference = [255, 255, 255]

for x in range(int(bwidth/pwidth)):

    for y in range(int(bheight/pheight)):

        current_average_rgb = [0, 0, 0]

        for i in range(pwidth):

            for j in range(pheight):

                x_ = x*pwidth+i
                y_ = y*pheight+j

                current_average_rgb[0] += bg.getpixel((x_, y_))[0]
                current_average_rgb[1] += bg.getpixel((x_, y_))[1]
                current_average_rgb[2] += bg.getpixel((x_, y_))[2]

        current_average_rgb[0] /= pwidth*pheight
        current_average_rgb[1] /= pwidth*pheight
        current_average_rgb[2] /= pwidth*pheight

        current_average_rgb_diff = [0, 0, 0]

        current_average_rgb_diff[0] = abs(current_average_rgb[0] - player_color_avg_rgb[0])
        current_average_rgb_diff[1] = abs(current_average_rgb[1] - player_color_avg_rgb[1])
        current_average_rgb_diff[2] = abs(current_average_rgb[2] - player_color_avg_rgb[2])

        if sum(current_average_rgb_diff)/len(current_average_rgb_diff) < sum(best_avg_rgb_difference)/len(best_avg_rgb_difference):

            best_avg_rgb_difference = current_average_rgb_diff
            best_avg_index = [x*pwidth, y*pheight]

hidden = bg.copy()

hidden.paste(player, (best_avg_index[0], best_avg_index[1]), player)

hidden.save(os.path.dirname(__file__) + 'output.png')
hidden.show()