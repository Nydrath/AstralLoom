from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import floor, ceil
import string

IMAGE_SIZE = (300, 300)
FONT_SIZE = 100

link = "ABC"
base_image = Image.new("L", IMAGE_SIZE)
font = ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE)
base_draw = ImageDraw.Draw(base_image)
for idx,letter in enumerate(link):
    tmp_image = Image.new("L", IMAGE_SIZE)
    tmp_draw = ImageDraw.Draw(tmp_image)
    tmp_draw.text((IMAGE_SIZE[0]/2, IMAGE_SIZE[1]/2), letter, fill=255, font=font)
    tmp_image = tmp_image.crop(tmp_image.getbbox())
    w, h = tmp_image.size
    base_data = np.asarray(base_image).T
    tmp_data = np.asarray(tmp_image).T
    ideal_x, ideal_y = (0, 0)
    ideal_value = 0
    if idx == 0:
        ideal_x, ideal_y = (IMAGE_SIZE[0]-w)/2, (IMAGE_SIZE[1]-h)/2
    else:
        for x in range(0, floor(IMAGE_SIZE[0]-w)):
            print("Letter #{0}: {1}%".format(idx, int(100*x/floor(IMAGE_SIZE[0]-w))))
            for y in range(0, floor(IMAGE_SIZE[1]-h)):
                placement = np.pad(np.copy(tmp_data), ((x, IMAGE_SIZE[0]-w-x), (y, IMAGE_SIZE[1]-h-y)), "constant", constant_values=0)
                s = np.sum(base_data*placement)
                if s > ideal_value:
                    ideal_value = s
                    ideal_x, ideal_y = x, y
    base_draw.text((ideal_x, ideal_y), letter, fill=255, font=font)
base_image.save("output.png")
