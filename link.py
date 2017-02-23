
from ziruph import Ziruphtable

class MagicalLink:
    def __init__(self, link):
        self.link = link

    def __add__(self, other):
        # Send the smaller link to the big one
        origin = max(self, other, key=lambda x: len(x.link)).link
        addon = min(self, other, key=lambda x: len(x.link)).link

        multiplexer = Ziruphtable([c for c in addon])
        result = ""
        for idx, c in enumerate(origin):
            result += multiplexer[c.lower(), addon[idx%len(addon)]]

        return MagicalLink(result)

    def __str__(self):
        return "Link[{0}]".format(self.link)

    def sendto(self, target):
        runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar".split())
        carrier = MagicalLink(runes[runes[runes[self.link, "Rit"], "Vor"], "Dorn"])
        return carrier+target

    def freeze(self):
        runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar".split())
        self.link = runes[runes[runes[self.link, "Is"], "Jera"], "Ka"]

    def heal(self):
        runes = Ziruphtable("Fa Ur Dorn Os Rit Ka Ken Hagal Not Is Jera Ar Sig Tyr Bar Man Yr Eh Vor Gar".split())
        self.link = runes[runes[runes[self.link, "Ur"], "Tyr"], "Ar"]
