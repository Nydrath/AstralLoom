from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
from math import floor, ceil
import string
import random
import torch
import torchvision
import torch.multiprocessing
import time

FONT_SIZE = 100

LINE_LENGTH = 7
NLINES = 7
BORDER_WIDTH = int(0.6 * FONT_SIZE)
LINE_SPACING = int(1.5 * FONT_SIZE)

linksize = 3
full_link = "".join(["".join(random.sample(string.ascii_uppercase, linksize)) for i in range(NLINES * LINE_LENGTH)])
links = [full_link[i:i+linksize] for i in range(0, len(full_link), linksize)]

nrotations = 8
rotations = [int(i*360/nrotations) for i in range(nrotations)]
sigils = [[] for i in range(LINE_LENGTH)]
totensor = torchvision.transforms.ToTensor()

def createsymbol(link):
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = IMAGE_WIDTH
    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

    fonts = [
        ImageFont.truetype("fonts/daedra.otf", size=FONT_SIZE),
        ImageFont.truetype("fonts/falmer.otf", size=FONT_SIZE),
        ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE),
        ImageFont.truetype("fonts/malachim.ttf", size=FONT_SIZE),
        ImageFont.truetype("fonts/enochian.ttf", size=FONT_SIZE)
    ]

    im = Image.new("L", IMAGE_SIZE)
    imdraw = ImageDraw.Draw(im)
    font = random.choice(fonts)
    w, h = font.getsize(link[0])
    imdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), link[0], fill=255, font=font)
    im = im.rotate(random.choice(rotations))
    imdata = totensor(im).squeeze().cuda().t()
    for idx2,letter in enumerate(link[1:]):
        letterim = Image.new("L", IMAGE_SIZE)
        letterdraw = ImageDraw.Draw(letterim)
        font = random.choice(fonts)
        w, h = font.getsize(letter)
        letterdraw.text(((IMAGE_WIDTH-w)/2, (IMAGE_HEIGHT-h)/2), letter, fill=255, font=font)
        letterim = letterim.rotate(random.choice(rotations))
        letterim = letterim.crop(letterim.getbbox())
        letterdata = totensor(letterim).squeeze().cuda().t()
        w, h = letterim.size
        xoptimal, yoptimal = (0, 0)
        voptimal = 0
        for x in range(0, floor(IMAGE_WIDTH-w)):
            for y in range(0, floor(IMAGE_HEIGHT-h)):
                test = torch.zeros(imdata.size()).cuda()
                # Pad letterdata with zeros with the correct offset
                tmp = test.narrow(0, x, letterdata.size()[0]).narrow(1, y, letterdata.size()[1])
                tmp.add_(letterdata)
                s = torch.sum(test.mul(imdata))
                if s > voptimal:
                    voptimal = s
                    xoptimal, yoptimal = x, y
        t = Image.new("L", IMAGE_SIZE)
        t.paste(letterim, (xoptimal, yoptimal))
        im = ImageChops.lighter(im, t)
    t = im.filter(ImageFilter.MaxFilter(int(5 * FONT_SIZE / 100)))
    t = t.filter(ImageFilter.MinFilter(int(5 * FONT_SIZE / 100)))
    t = Image.eval(t, lambda x: 255*(x==255))
    im = ImageChops.lighter(im, t)
    return im

pool = torch.multiprocessing.Pool()
result = pool.map_async(createsymbol, links)
while not result.ready():
    print("# Symbols not yet processed: {}".format(result._number_left))
    time.sleep(10)
sigils = result.get()
pool.close()
pool.join()

maxwidth = 0
for im in sigils:
    maxwidth = max(im.size[0], maxwidth)

baseim = Image.new("L", (maxwidth*LINE_LENGTH + 2*BORDER_WIDTH, int(len(sigils)/LINE_LENGTH)*LINE_SPACING + 2*BORDER_WIDTH))
for idx,im in enumerate(sigils):
        t = Image.new("L", baseim.size)
        t.paste(im, (BORDER_WIDTH + maxwidth*(idx%LINE_LENGTH), BORDER_WIDTH + LINE_SPACING*int(idx/LINE_LENGTH)))
        baseim = ImageChops.lighter(baseim, t)

baseim.save("out.png")
