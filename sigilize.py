from PIL import Image, ImageDraw

from functions import gematria
from squares import MagicalSquare

def with_square(sigil):
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
