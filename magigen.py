from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import math
import string
import random
import torch
import torchvision
import torch.multiprocessing
import time

from functions import gematria

def createsymbol(link):
    print("Creating symbol for {}..".format(link))
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = IMAGE_WIDTH
    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
    FONT_SIZE = 100

    fonts = [
        ImageFont.truetype("fonts/daedra.otf", size=FONT_SIZE),
        ImageFont.truetype("fonts/falmer.otf", size=FONT_SIZE),
        ImageFont.truetype("fonts/magi.ttf", size=FONT_SIZE),
        ImageFont.truetype("fonts/malachim.ttf", size=FONT_SIZE),
        ImageFont.truetype("fonts/enochian.ttf", size=FONT_SIZE)
    ]

    nrotations = 8
    rotations = [int(i*360/nrotations) for i in range(nrotations)]

    totensor = torchvision.transforms.ToTensor()
    random.seed(gematria(link))

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
        for x in range(0, math.floor(IMAGE_WIDTH-w)):
            for y in range(0, math.floor(IMAGE_HEIGHT-h)):
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

def create_circle():
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = IMAGE_WIDTH
    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
    FONT_SIZE = 100

    NSYMBOLS = 15
    BORDER_WIDTH = int(0.6 * FONT_SIZE)

    linksize = 3
    full_link = "".join(["".join(random.sample(string.ascii_uppercase, linksize)) for i in range(NSYMBOLS)])
    links = [full_link[i:i+linksize] for i in range(0, len(full_link), linksize)]

    nrotations = 8
    rotations = [int(i*360/nrotations) for i in range(nrotations)]
    sigils = []
    totensor = torchvision.transforms.ToTensor()

    pool = torch.multiprocessing.Pool(3)
    result = pool.map_async(lambda x:createsymbol(x, IMAGE_SIZE), links)
    while not result.ready():
        print("# Symbols not yet processed: {}".format(result._number_left))
        time.sleep(5)
    sigils = result.get()
    pool.close()
    pool.join()


    maxwidth = 0
    for im in sigils:
        maxwidth = max(im.size[0], maxwidth)

    # 0.18 for touching
    radius = 0.25 * maxwidth * math.ceil(NSYMBOLS / 4)
    baseim = Image.new("L", (int(2*radius + 2*BORDER_WIDTH), int(2*radius + 2*BORDER_WIDTH)))
    center = BORDER_WIDTH + radius
    for idx,im in enumerate(sigils):
        t = Image.new("L", baseim.size)
        x = center + radius*math.sin(2*math.pi*idx/NSYMBOLS) - im.size[0]/2
        y = center + radius*math.cos(2*math.pi*idx/NSYMBOLS) - im.size[1]/2
        t.paste(im, (int(x), int(y)))
        baseim = ImageChops.lighter(baseim, t)

    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = IMAGE_WIDTH
    IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
    FONT_SIZE = 150
    im = createsymbol("".join(random.sample(string.ascii_uppercase, 3)))
    t = Image.new("L", baseim.size)
    x = center - im.size[0]/2
    y = center - im.size[1]/2
    t.paste(im, (int(x), int(y)))
    baseim = ImageChops.lighter(baseim, t)

    baseim.save("out.png")


def fill_folder(folder, links):
    sigils = []

    pool = torch.multiprocessing.Pool(3)
    result = pool.map_async(createsymbol, [x[1] for x in links])
    sigils = result.get()
    pool.close()
    pool.join()

    for idx,im in enumerate(sigils):
        im.save(folder+links[idx][0]+".png")
