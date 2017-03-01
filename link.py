
from ziruph import Ziruphtable

class Link:
    def __init__(self, link):
        self.link = link

    def __add__(self, other):
        # Send the smaller link to the big one
        origin = max(self, other, key=lambda x: len(x.link))
        addon = min(self, other, key=lambda x: len(x.link))
        return Link(origin.mixwith(addon).link)

    def mixwith(self, other):
        multiplexer = Ziruphtable([c for c in other.link])
        result = ""
        for idx, c in enumerate(self.link):
            result += multiplexer[c, other.link[idx%len(other.link)]]
        return Link(result)

    def __str__(self):
        return "Link[*{0}*]".format(self.link)
