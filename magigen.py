from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import numpy as np
from math import floor, ceil
import string
import random

IMAGE_WIDTH = 600
IMAGE_HEIGHT = IMAGE_WIDTH
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
FONT_SIZE = 300

LINE_LENGTH = 7
BORDER_WIDTH = int(0.6 * FONT_SIZE)
LINE_SPACING = int(1.5 * FONT_SIZE)

linksize = 3
full_link = "".join(["".join(random.sample(string.ascii_uppercase, linksize)) for i in range(49)])
links = [full_link[i:i+linksize] for i in range(0, len(full_link), linksize)]
fonts = [
    ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE),
    ImageFont.truetype("fonts/malachim.ttf", size=FONT_SIZE),
    ImageFont.truetype("fonts/enochian.ttf", size=FONT_SIZE)
]

nrotations = 8
rotations = [int(i*360/nrotations) for i in range(nrotations)]
sigils = [[] for i in range(LINE_LENGTH)]
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
    t = im.filter(ImageFilter.MaxFilter(int(5 * FONT_SIZE / 100)))
    t = t.filter(ImageFilter.MinFilter(int(5 * FONT_SIZE / 100)))
    t = Image.eval(t, lambda x: 255*(x==255))
    im = ImageChops.lighter(im, t)
    sigils[int(idx1/LINE_LENGTH)].append(im.crop(im.getbbox()))

maxwidth = 0
for line in sigils:
    for im in line:
        maxwidth = max(im.size[0], maxwidth)

baseim = Image.new("L", (maxwidth*LINE_LENGTH + 2*BORDER_WIDTH, len(sigils)*LINE_SPACING + 2*BORDER_WIDTH))
for idx1,line in enumerate(sigils):
    for idx2,im in enumerate(line):
        t = Image.new("L", baseim.size)
        t.paste(im, (BORDER_WIDTH + maxwidth*idx2, BORDER_WIDTH + LINE_SPACING*idx1))
        baseim = ImageChops.lighter(baseim, t)

baseim.save("out.png")
