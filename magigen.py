from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np
from math import floor, ceil
import string
import random

IMAGE_WIDTH = 300
IMAGE_HEIGHT = IMAGE_WIDTH
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
FONT_SIZE = 100

full_link = "AJSNRK"
links = [full_link[i:i+3] for i in range(0, len(full_link), 3)]
fonts = [ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE), ImageFont.truetype("fonts/malachim.ttf", size=FONT_SIZE), ImageFont.truetype("fonts/enochian.ttf", size=FONT_SIZE)]
nrotations = 8
rotations = [int(i*360/nrotations) for i in range(nrotations)]
sigils = []
for idx1,link in enumerate(links):
    im = Image.new("L", IMAGE_SIZE)
    imdraw = ImageDraw.Draw(im)
    font = random.choice(fonts)
    w, h = font.getsize(link[0])
    imdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), link[0], fill=255, font=font)
    im = im.rotate(random.choice(rotations))
    for idx2,letter in enumerate(link[1:]):
        imdata = np.asarray(im).T
        tmp = Image.new("L", IMAGE_SIZE)
        tmpdraw = ImageDraw.Draw(tmp)
        font = random.choice(fonts)
        w, h = font.getsize(letter)
        tmpdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), letter, fill=255, font=font)
        tmp = tmp.rotate(random.choice(rotations))
        tmp = tmp.crop(tmp.getbbox())
        tmpdata = np.asarray(tmp).T
        w, h = tmp.size
        xoptimal, yoptimal = (0, 0)
        voptimal = IMAGE_WIDTH * IMAGE_HEIGHT * 255
        for x in range(0, floor(IMAGE_WIDTH-w)):
            print("{0}%".format(100*(x + floor(IMAGE_WIDTH-w)*idx2 + (len(link)-1)*floor(IMAGE_WIDTH-w)*idx1) / (floor(IMAGE_WIDTH-w) * (len(link)-1) * len(links))))
            for y in range(0, floor(IMAGE_HEIGHT-h)):
                test = np.pad(np.copy(tmpdata), ((x, IMAGE_WIDTH-w-x), (y, IMAGE_HEIGHT-h-y)), "constant", constant_values=0)
                s = np.sum(imdata-test)
                if s < voptimal:
                    voptimal = s
                    xoptimal, yoptimal = x, y
        t = Image.new("L", IMAGE_SIZE)
        t.paste(tmp, (xoptimal, yoptimal))
        im = ImageChops.lighter(im, t)
    im.save(str(idx1)+".png")

'''
    sigils.append(im.crop(im.getbbox()))

for idx,sigil in enumerate(sigils):
    sigil.save(str(idx)+".png")'''
