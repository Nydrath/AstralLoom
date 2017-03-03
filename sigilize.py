from PIL import Image, ImageDraw
import random

from functions import gematria
from squares import MagicalSquare
from link import Link

def with_square(sigil):
    if isinstance(sigil, Link):
        sigil = sigil.link
    sq = MagicalSquare(49)
    im = Image.new("L", (490, 490))
    pts = []
    for c in sigil:
        if c.isalnum():
            pts.append(tuple(10*i for i in sq[gematria(c)]))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 0), im.size], fill=255)
    draw.line(pts, fill=0)
    im.save(sigil+".png")

def with_coords(sigil, color=(0, 0, 0)):
    if isinstance(sigil, Link):
        sigil = sigil.link
    border = 40
    distance = 20
    im = Image.new("RGB", (distance*26+border*2, distance*26+border*2))
    pts = []
    pairs = [sigil[i:i+2] for i in range(0, len(sigil), 2)]
    for pair in pairs:
        if pair.isalpha() and len(pair) == 2:
            pts.append(tuple(border+distance*(ord(c.lower())-ord('a')) for c in pair))
    draw = ImageDraw.Draw(im)
    draw.rectangle([(0, 0), im.size], fill=(255, 255, 255))
    draw.line(pts, fill=color, width=5)
    im.save(sigil+".png")

def add_background(sigil, background, transparency=1.0):
    if isinstance(sigil, Link):
        sigil = sigil.link
    sig = Image.open(sigil+".png")
    bg = Image.open(background)
    im = Image.new("RGBA", sig.size)
    coords = tuple(-random.randint(0, bg.size[i]-sig.size[i]) for i in range(2))
    im.paste(bg, coords)
    for x in range(sig.size[0]):
        for y in range(sig.size[1]):
            if sig.getpixel((x, y)) != (255, 255, 255):
                im.putpixel((x, y), sig.getpixel((x, y))+(int(transparency*255),))
    im.save(sigil+".png")
