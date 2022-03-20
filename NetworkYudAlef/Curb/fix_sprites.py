from PIL import Image
from os import walk

desired_width = 32
current_width = 48

for (dirpath, dirnames, filenames) in walk("resources\\sprites\\Biker"):
    for filename in filenames:
        img = Image.open(dirpath + "\\" + filename)
        w, h = img.size
        new_img = Image.new("RGBA", (desired_width * int(w / current_width), h))
        for i in range(0, int(w / current_width)):
            section = img.crop((i * current_width, 0, i * current_width+desired_width, h))
            new_img.paste(section, (i * desired_width, 0, (i + 1) * desired_width, h))
        new_img.save("resources\\sprites\\Biker_Thin\\" + filename)
    break