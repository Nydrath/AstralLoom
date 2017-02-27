import pyimgur
import json
import os
import random

from link import BaseLink

def gematria(s):
    output = 0
    for c in s.lower():
        if c.isalpha():
            output += ((ord(c)-ord('a'))%9+1) * 10**int((ord(c)-ord('a'))/9)
        else:
            # If there's a character that isn't a letter, I'm assuming it's a number
            # So I'm going to just interpret it literally to the gematria
            output += int(c)
    return output

class ImageLink(BaseLink):
    def __init__(self, path):
        with open("client_data.json", "r") as f:
            clientdata = json.load(f)

        imgurclient = pyimgur.Imgur(clientdata["imgurid"])
        upload = imgurclient.upload_image(path)

        linkgematria = gematria(upload.id)

        sigil = ""
        while gematria(sigil) != linkgematria:
            addon = chr(random.randint(ord('a'), ord('z')))
            addon = random.choice([addon, addon.upper()])
            if gematria(sigil+addon) <= linkgematria:
                sigil += addon

        super(ImageLink, self).__init__(sigil)
