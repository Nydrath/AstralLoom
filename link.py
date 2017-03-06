
from functions import gematria
from ziruph import Ziruphtable
import string

class Link:
    def __init__(self, link):
        self.link = link

    def ziruph(self, other):
        p = string.ascii_lowercase
        if abs(self) > len(string.ascii_lowercase):
            p = " "*(abs(self) - len(string.ascii_lowercase)) + p
        else:
            p = p[:abs(self)]
        z = Ziruphtable(p)
        print(z)

        output = ""
        n = min(len(self.link), len(other.link))
        for i in range(n):
            output += z[self.link[i], other.link[i]]
        self.link = output

    def __str__(self):
        return "Link[*{0}*]".format(self.link)

    def __abs__(self):
        return gematria(self.link)
