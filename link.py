
from functions import gematria
from ziruph import Ziruphtable
import string
import math

class Link:
    def __init__(self, link):
        self.link = link

    def ziruph(self, other):
        p = string.ascii_letters
        if abs(self) > len(p):
            p = " "*(abs(self) - len(p)) + p
        else:
            p = p[:abs(self)]
        z = Ziruphtable(p)

        output = ""
        n = min(len(self.link), len(other.link))
        for i in range(n):
            output += z[self.link[i], other.link[i]]
        self.link = output

    def antiziruph(self, other):
        p = string.ascii_letters
        if abs(self) > len(p):
            p = " "*(abs(self) - len(p)) + p
        else:
            p = p[:abs(self)]
        z = Ziruphtable(p)

        n = min(len(self.link), len(other.link))
        outputs = [""]
        for i in range(n):
            tmp = []
            for r in z.reverse((self.link[i], other.link[i])):
                for o in outputs:
                    tmp.append(o+r)
            if len(tmp) > 0:
                outputs = tmp[:]
        return [Link(o) for o in outputs]

    def __str__(self):
        return "Link[*{0}*] | ngem = {1}".format(self.link, self.ngem())

    def __abs__(self):
        return gematria(self.link)

    def ngem(self):
        return math.log10(abs(self)/len(self.link))
