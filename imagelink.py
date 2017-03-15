import pyimgur
import json
import os
import random

from link import Link
from functions import gematria

class ImageLink(Link):
    def load_from_image(self, path):
        with open("client_data.json", "r") as f:
            clientdata = json.load(f)

        imgurclient = pyimgur.Imgur(clientdata["imgurid"])
        upload = imgurclient.upload_image(path)
        self.load_from_http(upload.link)

    def load_from_http(self, http):
        linkgematria = gematria(http)
        sigil = ""
        while gematria(sigil) != linkgematria:
            addon = chr(random.randint(ord('a'), ord('z')))
            addon = random.choice([addon, addon.upper()])
            if gematria(sigil+addon) <= linkgematria:
                sigil += addon

        self.link = sigil
