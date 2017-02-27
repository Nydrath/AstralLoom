
from ziruph import Ziruphtable

class BaseLink:
    def __init__(self, link):
        self.link = link

    def __add__(self, other):
        # Send the smaller link to the big one
        origin = max(self, other, key=lambda x: len(x.link)).link
        addon = min(self, other, key=lambda x: len(x.link)).link

        multiplexer = Ziruphtable([c for c in addon])
        result = ""
        for idx, c in enumerate(origin):
            result += multiplexer[c, addon[idx%len(addon)]]

        return BaseLink(result)

    def __str__(self):
        return "Link[*{0}*]".format(self.link)
