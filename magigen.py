from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import floor, ceil
import string

IMAGE_WIDTH = 300
IMAGE_HEIGHT = IMAGE_WIDTH
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
FONT_SIZE = 100

full_link = "ED"
links = [full_link[i:i+2] for i in range(0, len(full_link), 2)]
sigils = []
for idx1,link in enumerate(links):
    font = ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE)
    im = Image.new("L", IMAGE_SIZE)
    imdraw = ImageDraw.Draw(im)
    w, h = font.getsize(link[0])
    imdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), link[0], fill=255, font=font)
    im.save("testbase.png")
    for idx2,letter in enumerate(link[1:]):
        imdata = np.asarray(im).T
        tmp = Image.new("L", IMAGE_SIZE)
        tmpdraw = ImageDraw.Draw(tmp)
        w, h = font.getsize(letter)
        tmpdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), letter, fill=255, font=font)
        tmp = tmp.crop(tmp.getbbox())
        tmp.save("testtmp.png")
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
        #w, h = font.getsize(letter)
        #imdraw.text((xoptimal-w/2, yoptimal-h/2), letter, fill=255, font=font)
        t = Image.new("L", IMAGE_SIZE)
        t.paste(tmp, (xoptimal, yoptimal))
        im = Image.alpha_composite(im, t)
        #im = Image.blend(im, t, 0.5)
        #im.paste(tmp, (xoptimal, yoptimal))
    sigils.append(im)#.crop(im.getbbox()))

for idx,sigil in enumerate(sigils):
    sigil.save(str(idx)+".png")
